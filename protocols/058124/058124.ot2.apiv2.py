import math
import csv
from datetime import datetime
from opentrons.protocol_api.labware import OutOfTipsError

metadata = {
    'protocolName': '''Custom Serial Dilution for Protein Quantification''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.13'
}


def run(ctx):

    # get parameter values from json above
    [labware_reservoir, deadvol_reservoir,
     uploaded_csv] = get_values(  # noqa: F821
      'labware_reservoir', 'deadvol_reservoir', 'uploaded_csv')

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    # input csv - dilution scheme (1-6) assigned for 1-48 samples
    csvrows = [line for line in csv.DictReader(uploaded_csv.splitlines())]

    for index, sample in enumerate(csvrows):

        if not 1 <= int(sample['dilution scheme']) <= 6:
            raise Exception('Dilution scheme must be 1-6.')

        if not index:
            if not int(sample['sample number']) == 1:
                raise Exception(
                 'Sample numbers in input csv file must start with 1.')
        else:
            if not int(
             sample['sample number']) == int(
             csvrows[index-1]['sample number']) + 1:
                raise Exception(
                 'Invalid series of sample numbers in input csv file.')
            if not 2 <= int(sample['sample number']) <= 48:
                raise Exception(
                 'Sample number in input csv file must be 1-48.')

    # filter tips, p20 multi, p300 multi
    tips20 = [
     ctx.load_labware("opentrons_96_filtertiprack_20ul", str(
      slot)) for slot in [10]]
    tips300 = [
     ctx.load_labware("opentrons_96_filtertiprack_200ul", str(
      slot)) for slot in [11]]
    p20s = ctx.load_instrument(
        "p20_single_gen2", 'left', tip_racks=tips20)
    p300m = ctx.load_instrument(
        "p300_multi_gen2", 'right', tip_racks=tips300)

    # yield list chunks of size n
    def create_chunks(list_name, n):
        for i in range(0, len(list_name), n):
            yield list_name[i:i+n]

    # return liquid height in a well
    def liq_height(well, effective_diameter=None):
        if well.diameter:
            if effective_diameter:
                radius = effective_diameter / 2
            else:
                radius = well.diameter / 2
            csa = math.pi*(radius**2)
        else:
            csa = well.length*well.width
        return well.liq_vol / csa

    def slow_tip_withdrawal(pipette, well_location, to_center=False):
        if pipette.mount == 'right':
            axis = 'A'
        else:
            axis = 'Z'
        ctx.max_speeds[axis] = 10
        if to_center is False:
            pipette.move_to(well_location.top())
        else:
            pipette.move_to(well_location.center())
        ctx.max_speeds[axis] = None

    # notify user to replenish tips
    def pick_up_or_refill(pip):
        try:
            pip.pick_up_tip()
        except OutOfTipsError:
            ctx.pause(
             """Please Refill the {} Tip Boxes
             and Empty the Tip Waste""".format(pip))
            pip.reset_tipracks()
            pip.pick_up_tip()

    # list assigned samples for each scheme (chunks of 8, last one may be < 8)
    dilutions = {
     num+1: [*create_chunks([int(sample[
      'sample number']) for sample in csvrows if int(sample[
       'dilution scheme']) == num+1], 8)] for num in range(6)}

    # sample racks
    sample_racks = [
     ctx.load_labware(
      'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
      str(slot), 'sample rack') for slot in [
      1, 4][:math.ceil(len(csvrows) / 24)]]

    sample_positions = [
     well for rack in sample_racks for well in rack.wells()][:len(csvrows)]

    sample_cols_per_scheme = [len(dilutions[key+1]) for key in range(6)]

    for scheme in range(6):
        ctx.comment(
         "\nScheme {}, preparing dilutions for {} columns of samples\n".format(
          str(scheme+1), sample_cols_per_scheme[scheme]))

    diluent = ctx.load_labware(labware_reservoir, '8', 'diluent').wells()[0]

    sample_cols_total = sum(sample_cols_per_scheme)

    # up to 4 dilution plates (4 consecutive columns per chunk of 8 samples)
    dilution_plates = [
     ctx.load_labware(
      'nest_96_wellplate_2ml_deep', str(slot), 'dilution plate') for slot in [
      2, 3, 5, 6][:math.ceil(sample_cols_total / 3)]]

    # to yield 4-column chunk as next dilution destination
    def thirds():

        lst = [
         chunk for plate in dilution_plates for chunk in create_chunks(
          plate.columns(), 4)]

        yield from lst

    dest = thirds()

    # dilution scheme parameters
    params = {
     1: {"diluent vol": [990, 450, 150],
         "sample vol": 10,
         "mix count": 10,
         "serial vol": [50, 150]},
     2: {"diluent vol": [990, 150],
         "sample vol": 10,
         "mix count": 10,
         "serial vol": [150]},
     3: {"diluent vol": [490, 450, 150],
         "sample vol": 10,
         "mix count": 5,
         "serial vol": [50, 150]},
     4: {"diluent vol": [380, 450, 100],
         "sample vol": 20,
         "mix count": 3,
         "serial vol": [50, 100]},
     5: {"diluent vol": [990, 450, 450, 100],
         "sample vol": 10,
         "mix count": 10,
         "serial vol": [50, 50, 100]},
     6: {"diluent vol": [490, 450, 450, 100],
         "sample vol": 10,
         "mix count": 5,
         "serial vol": [50, 50, 100]}
         }

    # diluent reservoir fill volume - calculate and notify
    diluent.liq_vol = 0
    for key in params.keys():
        numsamps = 0
        for _ in dilutions[key]:
            numsamps += len(_)
        diluent.liq_vol += numsamps*sum(params[key]['diluent vol'])
    diluent.liq_vol += deadvol_reservoir
    ctx.pause(
     "\nEnsure reservoir is filled with {} mL diluent. Resume\n".format(
      diluent.liq_vol / 1000))

    output = []  # to collect destination location for each sample

    # for each dilution scheme and all of its assigned samples
    for i, (key, value) in enumerate(dilutions.items()):

        # for each column of 8 samples (last column may be < 8)
        for samplenums in value:

            # yield 4-column destination for dilutions
            destination = next(dest)

            # destination wells - set current vol to 0
            for column in destination:

                column[0].liq_vol = 0

            # notify user - current scheme, assigned samples, destination
            ctx.comment("\nCurrent Dilution Scheme: {}\n".format(key))
            ctx.comment("\nAssigned Samples: {}\n".format(value))
            ctx.comment("\nCurrent Samples: {}\n".format(samplenums))
            ctx.comment("\nCurrent Destination: {}\n".format(destination))

            # to pick up one tip for each sample (last column may be < 8)
            tipcolindex = abs(len(samplenums)-8)

            p300m.pick_up_tip(tips300[0].columns()[i][tipcolindex])

            # diluent transfer to destination columns
            for vol, column in zip(params[key]['diluent vol'], destination):

                diluent.liq_vol -= vol  # increment reservoir volume

                ht = liq_height(
                 diluent) - 3 if liq_height(
                 diluent) - 3 > 1 else 1

                reps = math.ceil(vol / 200)

                v = vol / reps

                for rep in range(reps):

                    p300m.aspirate(v, diluent.bottom(ht))
                    ctx.delay(seconds=1)
                    slow_tip_withdrawal(p300m, diluent)

                    p300m.dispense(v, column[0].bottom(1))
                    ctx.delay(seconds=1)
                    slow_tip_withdrawal(p300m, column[0])
                    p300m.touch_tip(radius=0.75, v_offset=-2, speed=10)
                    column[0].liq_vol += v  # increment current dest vol

            # sample to wells of 1st column of 4-column destination chunk
            for samplenum, d in zip(
             samplenums, [well for well in destination[0]]):

                p20s.pick_up_tip()

                sampvol = params[key]['sample vol']

                p20s.aspirate(sampvol, sample_positions[samplenum - 1])

                p20s.dispense(sampvol, d.bottom(1))
                p20s.mix(5, sampvol, d.bottom(1))
                ctx.delay(seconds=1)
                slow_tip_withdrawal(p20s, d)
                p20s.touch_tip(radius=0.75, v_offset=-2, speed=10)

                output.append(str(d))  # dest location - to write to output

                p20s.drop_tip()

            # serial transfer
            tfervols = params[key]['serial vol']

            tfercount = len(tfervols)

            for i, vol, column in zip(
             [*range(tfercount)], tfervols, destination):

                # tip height - 3/4 of the way down liquid column
                mixht = 0.25*liq_height(column[0])

                # premix
                for rep in range(params[key]['mix count']):
                    p300m.aspirate(100, column[0].bottom(mixht))
                    p300m.dispense(100, column[0].bottom(mixht))

                p300m.aspirate(vol, column[0].bottom(1))
                ctx.delay(seconds=1)
                slow_tip_withdrawal(p300m, column[0])
                p300m.touch_tip(radius=0.75, v_offset=-2, speed=10)

                disploc = destination[destination.index(column)+1][0]
                p300m.dispense(vol, disploc.bottom(1))

                if i == tfercount - 1:

                    # final postmix in last column
                    p300m.mix(4, 100, disploc.bottom(mixht))
                    ctx.delay(seconds=1)
                    slow_tip_withdrawal(p300m, disploc)
                    p300m.touch_tip(radius=0.75, v_offset=-2, speed=10)

            p300m.drop_tip()

    # output file - original csv content plus destination for each sample
    for row, dest in zip(csvrows, output):

        row['destination'] = dest

    """
    write output to jupyter notebook directory on OT-2 raspberry pi
    for file download via web browser [OT-2 IP address]:48888
    """

    # unique filename to avoid accidental over writing
    current = datetime.now()
    file = 'var/lib/jupyter/notebooks/outputfile{}.csv'.format(
     str(current.microsecond))

    if not ctx.is_simulating():
        with open(file, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=csvrows[0].keys())
            writer.writeheader()
            for row in csvrows:
                writer.writerow(row)

    ctx.comment("""\nfinished - use the Opentrons app (click jupyter link)
    to locate and download the output csv file\n""")
