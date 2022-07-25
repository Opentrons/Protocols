import math

metadata = {
    'protocolName': '''mRNA Encapsulation''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.11'
}


def run(ctx):

    # get parameter values from json above
    [count_samples_rowa, count_samples_rowb, count_samples_rowc,
     count_samples_rowd] = get_values(  # noqa: F821
      'count_samples_rowa', 'count_samples_rowb', 'count_samples_rowc',
      'count_samples_rowd')

    ctx.set_rail_lights(True)

    num_samplerows = 0

    tot_count = 0

    for count in [count_samples_rowa, count_samples_rowb, count_samples_rowc,
                  count_samples_rowd]:

        if not 0 <= count <= 5:
            raise Exception('Invalid sample count (must be 1-5).')

        if count:
            num_samplerows += 1

        tot_count += count

    # helper functions

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

    # yield list chunks of size n
    def create_chunks(list_name, n):
        for i in range(0, len(list_name), n):
            yield list_name[i:i+n]

    # 300 and 1000 uL tips, p300 single, p1000 single

    tips1000 = [ctx.load_labware(
     "opentrons_96_tiprack_1000ul", str(slot)) for slot in [1]]

    p1000s = ctx.load_instrument(
        "p1000_single_gen2", 'left', tip_racks=tips1000)

    tips300 = [
     ctx.load_labware(
      "opentrons_96_tiprack_300ul", str(slot)) for slot in [2]]

    p300s = ctx.load_instrument(
        "p300_single_gen2", 'right', tip_racks=tips300)

    # tube rack for samples and mRNA stock
    tuberack = ctx.load_labware(
     'opentrons_24_tuberack_nest_1.5ml_snapcap', '7',
     '25 ug/mL Sample Stock and mRNA Stock')

    samps = [
     row[:count] for row, count in zip(tuberack.rows(), [
         count_samples_rowa, count_samples_rowb,
         count_samples_rowc, count_samples_rowd])]

    mrna = [row[-1] for row in tuberack.rows()]

    sample_plate = ctx.load_labware(
     'corning_96_wellplate_360ul_flat', '4', 'Sample Plate')

    tworows = []
    for index, row in enumerate(sample_plate.rows()):
        if not index % 2:
            new = row
            new.extend(sample_plate.rows()[index+1])
            tworows.append(new)

    test_plates = [
     ctx.load_labware('corning_96_wellplate_360ul_flat', str(slot),
                      'Test Plate {}'.format(
                      index+1)) for index, slot in enumerate([3, 6, 9, 5])]

    buffer_reservoir = ctx.load_labware(
     'usascientific_12_reservoir_22ml', '8', 'Buffer Reservoir')
    te, te_triton, pbs = [
     buffer_reservoir.wells_by_name()[name] for name in ['A1', 'A2', 'A3']]
    deadvol_res = 3000

    pbs.liq_vol = 13000*(tot_count / 20) + deadvol_res
    te.liq_vol = 10400 + 6000*(tot_count / 20) + deadvol_res
    te_triton.liq_vol = 4000 + 6000*(tot_count / 20) + deadvol_res

    # alert user to reagent volumes needed
    ctx.comment("Ensure buffers in sufficient volume are present on deck.")
    for volume, units, reagent, location in zip(
     [math.ceil(rgnt.liq_vol) if rgnt.liq_vol < 1500 else math.ceil(
      rgnt.liq_vol / 1000) for rgnt in [te, te_triton, pbs]],
     ['mL', 'mL', 'mL'],
     ['TE', 'TE Triton', 'PBS'],
     [te, te_triton, pbs]):
        ctx.comment(
         "{0} {1} {2} in {3}".format(
          str(volume), units, reagent.upper(), location))

    for repeat in range(num_samplerows):

        ctx.comment('\nStarting {}\n'.format(test_plates[repeat]))

        num_samps = len(samps[repeat])

        ctx.comment(
         '\nDistributing PBS to Sample Plate for {} samples\n'.format(
          num_samps))

        p1000s.pick_up_tip()

        for chunk in [*create_chunks(tworows[repeat], 3)][:num_samps]:

            p1000s.move_to(pbs.top())
            for vol in [210, 220, 230]:

                ht = liq_height(pbs) - 3 if liq_height(pbs) - 3 > 1 else 1

                p1000s.air_gap(50)
                p1000s.aspirate(vol, pbs.bottom(ht))

                pbs.liq_vol -= vol

            for well, vol in zip(chunk, [230, 220, 210]):

                p1000s.dispense(vol + 50, well.top(2), rate=2)
                ctx.delay(seconds=0.5)

        p1000s.drop_tip()

        ctx.comment(
         '\nDistributing {} Samples to Sample Plate\n'.format(num_samps))

        for index, chunk in enumerate(
         [*create_chunks(tworows[repeat], 3)][:num_samps]):

            p300s.pick_up_tip()

            p300s.move_to(samps[repeat][index].top())
            for i, vol in zip([0, 1, 2], [40, 30, 20]):

                if not i:
                    p300s.air_gap(50)

                p300s.aspirate(vol, samps[repeat][index].bottom(1))
                p300s.air_gap(50)

            for i, well, vol in zip([0, 1, 2], chunk, [20, 30, 40]):

                v = vol + 50 if i != 2 else vol + 100

                p300s.dispense(v, well.top(5), rate=2)
                ctx.delay(seconds=0.5)

            p300s.drop_tip()

        ctx.comment('\nDistributing TE to Test Plate\n')

        p300s.pick_up_tip()

        for5thsample = [
         (well, well2) for well, well2 in zip(
          test_plates[repeat].rows()[4][8:11],
          test_plates[repeat].rows()[5][8:11])]

        for chunk in [*create_chunks(
            [(well, well2) for well, well2 in zip(
             test_plates[repeat].rows()[0],
             test_plates[repeat].rows()[1])] + for5thsample,
                3)][:num_samps]:

            for index in [0, 1]:

                p300s.move_to(te.top())
                for i, pair in zip([0, 1, 2], chunk):

                    ht = liq_height(te) - 3 if liq_height(te) - 3 > 1 else 1

                    if not i:
                        p300s.air_gap(20)

                    p300s.aspirate(50, te.bottom(ht))
                    p300s.air_gap(40)

                    te.liq_vol -= 50

                for pair in chunk:

                    v = 90 if i != 2 else 110

                    p300s.dispense(v, pair[index].top(7), rate=2)
                    ctx.delay(seconds=0.5)

        for chunk in [*create_chunks(
            [(well, well2) for i, well, well2 in zip(
             [*range(12)],
             test_plates[repeat].rows()[6],
             test_plates[repeat].rows()[7]) if (
             i and (not 8 <= i <= 10))], 2)]:

            for index in [0, 1]:

                p300s.move_to(te.top())
                for i, pair in zip([0, 1], chunk):

                    ht = liq_height(te) - 3 if liq_height(te) - 3 > 1 else 1

                    if not i:
                        p300s.air_gap(50)

                    p300s.aspirate(50, te.bottom(ht))
                    p300s.air_gap(50)

                    te.liq_vol -= 50

                for pair in chunk:

                    v = 100 if i != 1 else 150

                    p300s.dispense(v, pair[index].top(7), rate=2)
                    ctx.delay(seconds=0.5)

        p300s.drop_tip()

        p1000s.pick_up_tip()

        for chunk in [*create_chunks(
            [(well, well2) for well, well2 in zip(
             test_plates[repeat].rows()[4],
             test_plates[repeat].rows()[5]) if (
             well, well2) not in for5thsample], 6)]:

            for index in [0, 1]:

                p1000s.move_to(te.top())
                for pair in chunk:

                    ht = liq_height(te) - 3 if liq_height(te) - 3 > 1 else 1

                    p1000s.air_gap(50)
                    p1000s.aspirate(100, te.bottom(ht))

                    te.liq_vol -= 100

                for pair in chunk:

                    p1000s.dispense(150, pair[index].top(7), rate=2)
                    ctx.delay(seconds=0.5)

        ctx.comment('\nDistributing TE-Triton to Test Plate\n')

        p1000s.move_to(te_triton.top())

        ht = liq_height(te_triton) - 3 if liq_height(te_triton) - 3 > 1 else 1

        twowells = [
         test_plates[repeat].rows()[rowindex][0] for rowindex in [6, 7]]

        for well in twowells:
            p1000s.air_gap(50)
            p1000s.aspirate(100, te_triton.bottom(ht))

            te_triton.liq_vol -= 100

            p1000s.dispense(150, well.top(7), rate=2)
            ctx.delay(seconds=0.5)

        p1000s.drop_tip()

        p300s.pick_up_tip()

        for5thsample = [(well, well2) for well, well2 in zip(
         test_plates[repeat].rows()[6][8:11],
         test_plates[repeat].rows()[7][8:11])]

        for chunk in [*create_chunks(
            [(well, well2) for well, well2 in zip(
             test_plates[repeat].rows()[2],
             test_plates[repeat].rows()[3])] + for5thsample,
                3)][:num_samps]:

            for index in [0, 1]:

                p300s.move_to(te_triton.top())
                for i, pair in zip([0, 1, 2], chunk):

                    ht = liq_height(
                     te_triton) - 3 if liq_height(te_triton) - 3 > 1 else 1

                    if not i:
                        p300s.air_gap(20)

                    p300s.aspirate(50, te_triton.bottom(ht))
                    p300s.air_gap(40)

                    te_triton.liq_vol -= 50

                for pair in chunk:

                    v = 90 if i != 2 else 110

                    p300s.dispense(v, pair[index].top(7), rate=2)
                    ctx.delay(seconds=0.5)

        for chunk in [*create_chunks(
            [(well, well2) for i, well, well2 in zip(
             [*range(12)], test_plates[repeat].rows()[6],
             test_plates[repeat].rows()[7]) if (
             i and (not 8 <= i <= 10))], 2)]:

            for index in [0, 1]:

                p300s.move_to(te_triton.top())
                for i, pair in zip([0, 1], chunk):

                    ht = liq_height(
                     te_triton) - 3 if liq_height(te_triton) - 3 > 1 else 1

                    if not i:
                        p300s.air_gap(50)

                    p300s.aspirate(50, te_triton.bottom(ht))
                    p300s.air_gap(50)

                    te_triton.liq_vol -= 50

                for pair in chunk:

                    v = 100 if i != 1 else 150

                    p300s.dispense(v, pair[index].top(7), rate=2)
                    ctx.delay(seconds=0.5)

        p300s.drop_tip()

        ctx.comment('\nAdding Sample to Test Plate\n')

        for index, chunk in enumerate(
         [*create_chunks(tworows[repeat], 3)][:num_samps]):

            p300s.pick_up_tip()

            if index < 4:

                for well, column in zip(chunk, test_plates[repeat].columns()):

                    for indx in [0, 2]:
                        p300s.move_to(well.top())
                        for i, dest in zip([0, 1], column[0+indx:2+indx]):
                            if not i:
                                p300s.air_gap(50)
                            p300s.aspirate(50, well.bottom(1))
                            p300s.air_gap(50)

                        for i, dest in zip([0, 1], column[0+indx:2+indx]):

                            v = 100 if i != 1 else 150

                            p300s.dispense(v, dest.top(5), rate=2)
                            ctx.delay(seconds=0.5)

            else:

                for well, column in zip(
                 chunk, test_plates[repeat].columns()[8:11]):

                    for indx in [0, 2]:
                        p300s.move_to(well.top())
                        for i, dest in zip([0, 1], column[4+indx:6+indx]):
                            if not i:
                                p300s.air_gap(50)
                            p300s.aspirate(50, well.bottom(1))
                            p300s.air_gap(50)

                        for i, dest in zip([0, 1], column[4+indx:6+indx]):

                            v = 100 if i != 1 else 150

                            p300s.dispense(v, dest.top(5), rate=2)
                            ctx.delay(seconds=0.5)

            p300s.drop_tip()

        ctx.comment('\nSerial Dilution of mRNA in Test Plate\n')

        p1000s.pick_up_tip()

        p1000s.move_to(mrna[repeat].top())

        for row in test_plates[repeat].rows()[4:]:

            p1000s.air_gap(50)
            p1000s.aspirate(100, mrna[repeat].bottom(1))

        # add mRNA to 1st well of the row
        for row in test_plates[repeat].rows()[4:]:

            p1000s.dispense(150, row[0].top(5), rate=2)
            ctx.delay(seconds=0.5)

        p1000s.drop_tip()

        # mix and transfer to next well
        for row in test_plates[repeat].rows()[4:]:
            p300s.pick_up_tip()
            for index, well in enumerate(row[:8]):
                dest = row[
                 index+1] if index < 7 else ctx.fixed_trash.wells()[0].top(-5)
                p300s.transfer(
                 100, well, dest, mix_before=(3, 100), new_tip='never')
            p300s.drop_tip()

        ctx.comment(
         '''\nFinished {}. Pause the robot to remove it from the deck\n
        \nResume to continue with remaining test plates.\n'''.format(
          test_plates[repeat]))

    ctx.comment("""\nProcess complete for all test plates\n""")
