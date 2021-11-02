import json
import os
import math

metadata = {
    'protocolName': 'Olink Target 96 Part 3/3: Detection',
    'author': 'Nick <ndiehl@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    num_samples, p300_mount, m20_mount = get_values(  # noqa: F821
        'num_samples', 'p300_mount', 'm20_mount')

    if not 1 <= num_samples <= 96:
        raise Exception('Invalid number of samples (1-96)')

    det_mix = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '7',
        'tuberack for detection mix (A3)').wells_by_name()['A3']
    inc_plate = ctx.load_labware('generic_96_aluminumblock_350ul', '5',
                                 'incubation plate')
    sample_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '1', 'sample plate')
    strip = ctx.load_labware(
        'genericstrips_96_wellplate_200ul', '4',
        'strip for distribution (column 7)').columns_by_name()['7']
    primer_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '3', 'primer plate')
    fluidigm = ctx.load_labware('fluidigm_192_wellplate_96x10ul_96x10ul', '2',
                                'Fluidigm 96.96 Dynamic Array')
    tipracks300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '10')]
    tipracks20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                  for slot in ['8', '9', '11']]
    stationary_rack = ctx.load_labware('opentrons_96_filtertiprack_20ul', '6')

    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks300)
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tipracks20)
    num_cols = math.ceil(num_samples/8)
    tip_track = True
    tip_count = 0

    folder_path = '/data/olink'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                if 'm20' in data:
                    tip_count = data['m20']

    def m20_pick_up():
        nonlocal tip_count
        if tip_count == 12:
            ctx.pause('Please refill 20ul filter tiprack on slot 6 before \
resuming.')
        m20.pick_up_tip(stationary_rack.rows()[0][tip_count])
        tip_count += 1

    p300.default_speed = 100
    m20.default_speed = 100
    ctx.home()
    ctx.comment('Prepare and prime a 96.96 Dynamic ArrayTM Integrated Fluidic \
Circuit (IFC) according to the manufacturer’s instructions. Briefly, inject \
one control line fluid syringe into each accumulator on the chip, and then \
prime the chip on the IFC Controller for approximately 20 minutes.')
    ctx.comment('Thaw the Primer Plate, vortex and spin briefly.')
    ctx.pause(f'P20 multi transfer will begin at column {tip_count+1} of \
tiprack on slot 6.')

    # transfer incubation mix to strip with reverse pipetting
    p300.pick_up_tip()
    p300.aspirate(5, det_mix)
    for well in strip:
        p300.aspirate(95, det_mix)
        p300.dispense(95, well)
    p300.dispense(p300.current_volume, det_mix)
    p300.drop_tip()

    # transfer from strip to plate
    m20_pick_up()
    m20.aspirate(5, strip[0])
    for col in sample_plate.rows()[0][:num_cols]:
        m20.aspirate(7.2, strip[0])
        m20.dispense(7.2, col)
    m20.drop_tip()

    # transfer samples
    for s, d in zip(inc_plate.rows()[0][:num_cols],
                    sample_plate.rows()[0][:num_cols]):
        m20.pick_up_tip()
        m20.transfer(2.8, s, d, new_tip='never')
        m20.drop_tip()

    ctx.pause('Seal the plate with an adhesive plastic film, vortex and spin \
at 400 x g, 1 min at room temperature.')

    # transfer primer and sample to fluidigm plate
    sample_destinations = [
        well for row in fluidigm.rows()[:2] for well in row[:6]]
    primer_destinations = [
        well for col in fluidigm.rows()[:2] for well in col[6:]]

    for source, dest in zip(
            primer_plate.rows()[0] + sample_plate.rows()[0][:num_cols],
            primer_destinations + sample_destinations[:num_cols]):
        m20.pick_up_tip()
        m20.aspirate(7, source.bottom(0.5))
        m20.dispense(5, dest.bottom(1))
        m20.drop_tip()

    # track final used tip
    if tip_track and not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {'m20': tip_count}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
