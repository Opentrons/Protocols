metadata = {
    'protocolName': 'COVID MM-QC Protocol',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [p300_mount, p20_mount, temperature, component_1_volume, component_2_volume] = get_values(  # noqa: F821
    "p300_mount", "p20_mount", "temperature", "component_1_volume", "component_2_volume")

    # Load Labware
    tuberack = ctx.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 8)
    temp_mod = ctx.load_module('temperature module gen2', 9)
    dest_tubes = temp_mod.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap')
    component_3 = ctx.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap', 5)['A1']
    pcr_plate = ctx.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul', 6)
    tiprack_200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tiprack_20ul = ctx.load_labware('opentrons_96_filtertiprack_20ul', 1)

    # Load Instruments
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=[tiprack_200ul])
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=[tiprack_20ul])

    # Set Temperature to 8C
    temp_mod.set_temperature(temperature)

    # Transfer Component 1 to 24 Well Block Tubes
    p300.transfer(float(component_1_volume), tuberack['A1'], dest_tubes.wells()[:24], new_tip='once')

    # Transfer Component 2 to 24 Well Block Tubes
    p300.transfer(float(component_2_volume), tuberack['B1'], dest_tubes.wells()[:24], new_tip='always')

    # Get Select PCR Tube Wells
    pcr_wells = [pcr_plate[well] for well in ['A1','A2','A3','A6','A7','A8','C1','C2','C3']]

    # Transfer from Tube 1 to Select PCR Tubes
    p300.transfer(22, dest_tubes['A1'], pcr_wells, new_tip='once')

    # Transfer Component 3 to Select PCR Tube Wells
    p20.transfer(18, component_3, pcr_wells[-3:])

    # Deactivate Temperature Module
    temp_mod.deactivate()
