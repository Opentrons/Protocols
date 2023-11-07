import math

metadata = {
    'protocolName': 'Normalization Using .csv File',
    'author': 'Parrish Payne <parrish.payne@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}


def run(ctx):

    [input_csv, init_vol_buff, labware_pcr_plate, dna_plate_lname,
        temp_mod_lname, temperature, p20_mount, p300_mount] = get_values(  # noqa: F821
        "input_csv", "init_vol_buff", "labware_pcr_plate", "dna_plate_lname",
        "temp_mod_lname", "temperature","p20_mount", "p300_mount")

    if not 4 <= temperature <= 95:
        raise Exception(
            "Temperature module range is between 4 and 95ºC")

    # modules
    temp_mod = None
    if temp_mod_lname:
        temp_mod = ctx.load_module("temperature module gen2", '3')
    
    # labware
    tiprack20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot,
                         '20ul tiprack')
        for slot in ['1', '8']]
    tiprack300 = [
        ctx.load_labware(
            'opentrons_96_filtertiprack_200ul', slot, '200ul tiprack')
        for slot in ['2', '9']]
    
    dna_plate = None
    if temp_mod:
        dna_plate = temp_mod.load_labware(dna_plate_lname, 'sample plate')
    else:
        dna_plate = ctx.load_labware(dna_plate_lname, '3', 'sample plate')
    
    
    tube_rack = ctx.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '5')
    dest_plate = ctx.load_labware(labware_pcr_plate, '6', 'end-point-plate')  # noqa: E501

    # pipettes
    p20 = ctx.load_instrument(
        'p20_single_gen2', p20_mount, tip_racks=tiprack20)
    p300 = ctx.load_instrument(
        'p300_single_gen2', p300_mount, tip_racks=tiprack300)

    # Helper Functions
    # liquid height tracking
    v_naught_buff = init_vol_buff*1000

    radius_sds = tube_rack.wells_by_name()['A3'].diameter/2

    h_naught_buff = 0.85*v_naught_buff/(math.pi*radius_sds**2)

    h_buff = h_naught_buff

    def adjust_height(volume_from_loop):
        nonlocal h_buff

        radius = radius_sds

        dh = (volume_from_loop/(math.pi*radius**2))*1.33

        h_buff -= dh

        if h_buff < 12:
            h_buff = 1

    def slow_withdraw(pip, well, delay_seconds=2.0):
        pip.default_speed /= 16
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top())
        pip.default_speed *= 16

    # Set temperature module temperature
    if temp_mod:
        ctx.comment("\n\nSetting temperature module to {} ºC\n".
                    format(temperature))
        temp_mod.set_temperature(temperature)

    # mapping
    buffer = tube_rack.wells_by_name()['A3']

    # parse
    all_rows = [[val.strip() for val in line.split(',')]
                for line in input_csv.splitlines()
                if line.split(',')[0].strip()][1:]

    # Adding buffer to the wells
    for row in all_rows:
        well = row[0]
        dest_well = dest_plate.wells_by_name()[well]
        volume = float(row[7])

        if volume > 0:
            if volume > 20:
                if not p300.has_tip:
                    p300.pick_up_tip()
                p300.aspirate(volume, buffer.bottom(h_buff))
                p300.dispense(volume, dest_well)

            else:
                if not p20.has_tip:
                    p20.pick_up_tip()
                p20.aspirate(volume, buffer.bottom(h_buff))
                p20.dispense(volume, dest_well)

        adjust_height(volume)

    if p20.has_tip:
        p20.drop_tip()
    if p300.has_tip:
        p300.drop_tip()

    # Adding sample to the wells
    for row in all_rows:

        well = row[0]
        source_well = dna_plate.wells_by_name()[well]
        dest_well = dest_plate.wells_by_name()[well]

        volume = float(row[6])
        mix_reps = 2
        tip_height = 0.5

        if volume > 0:
            if volume > 20:
                p300.pick_up_tip()
                p300.aspirate(volume, source_well.bottom(tip_height))
                p300.dispense(volume, dest_well)
                p300.mix(mix_reps, 20)
                p300.blow_out()
                p300.drop_tip()

            else:
                p20.pick_up_tip()
                p20.aspirate(volume, source_well.bottom(tip_height))
                p20.dispense(volume, dest_well)
                p20.mix(mix_reps, 10)
                p20.blow_out()
                p20.drop_tip()
