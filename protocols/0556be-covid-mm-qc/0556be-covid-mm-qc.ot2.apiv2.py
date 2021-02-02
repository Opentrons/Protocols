import math

metadata = {
    'protocolName': 'COVID MM-QC Protocol',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [p300_mount, p20_mount, temperature, component_1_volume,
        component_2_volume, component_1_height, component_2_height] = get_values(  # noqa: F821
        "p300_mount", "p20_mount", "temperature", "component_1_volume",
        "component_2_volume", "component_1_height", "component_2_height")

    component_1_volume = float(component_1_volume)
    component_2_volume = float(component_2_volume)

    # Load Labware
    tuberack = ctx.load_labware(
        'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 8)
    temp_mod = ctx.load_module('temperature module gen2', 10)
    dest_tubes = temp_mod.load_labware(
        'opentrons_24_aluminumblock_generic_2ml_screwcap')
    component_3 = ctx.load_labware(
        'opentrons_24_aluminumblock_generic_2ml_screwcap', 9).wells()[0]
    pcr_plate = ctx.load_labware(
        'opentrons_96_aluminumblock_generic_pcr_strip_200ul', 6)
    tiprack_200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 1)
    tiprack_20ul = ctx.load_labware('opentrons_96_filtertiprack_20ul', 4)

    # Load Instruments
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=[tiprack_200ul])
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=[tiprack_20ul])

    # Liquid Level Tracking
    min_height = 1  # depth at which the pipette tip will stop descending into the tube
    compensation_coeff = 1.1  # ensures tip is below liquid level even with theoretical volume loss
    component_1_height = float(component_1_height)  # heights that the tubes will be filled to initially
    component_2_height = float(component_2_height)  # heights that the tubes will be filled to initially
    heights = dict(zip(tuberack.wells()[:2], [component_1_height, component_2_height]))

    def h_track(vol, tube):
        nonlocal heights
        
        # calculate height decrement based on volume
        dh = ((math.pi*((tube.diameter/2)**2))/vol)*compensation_coeff
        
        # make sure height decrement will not crash into the bottom of the tube
        h = heights[tube] - dh if heights[tube] - dh > min_height else min_height
        heights[tube] = h
        return h

    # Set Temperature to 8C
    temp_mod.set_temperature(temperature)

    # Transfer Component 1 to 24 Well Block Tubes
    for d_tubes in dest_tubes.wells()[:24]:
        h = h_track(component_1_volume, tuberack['A1'])
        p300.transfer(component_1_volume, tuberack['A1'].bottom(h),
                    d_tubes, new_tip='always')

    # Transfer Component 2 to 24 Well Block Tubes
    for d_tubes in dest_tubes.wells()[:24]:
        h = h_track(component_2_volume, tuberack['B1'])
        p300.transfer(component_2_volume,
                    tuberack['B1'].bottom(h),
                    d_tubes, new_tip='always')

    # Get Select PCR Tube Wells
    pcr_wells = [pcr_plate[well] for well in ['A1', 'A2', 'A3', 'A6', 'A7',
                                              'A8', 'C1', 'C2', 'C3']]

    # Transfer from Tube 1 to Select PCR Tubes
    p300.transfer(22, dest_tubes['A1'], pcr_wells, new_tip='always')
    
    # Mix Component 3, 5 times
    p300.pick_up_tip()
    p300.mix(5, 200, component_3)
    p300.drop_tip()

    # Transfer Component 3 to Select PCR Tube Wells
    p20.transfer(18, component_3, pcr_wells[-3:], mix_after=(5, 9), new_tip='always')

    # Deactivate Temperature Module
    temp_mod.deactivate()
