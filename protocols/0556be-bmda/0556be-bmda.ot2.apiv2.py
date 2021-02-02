metadata = {
    'protocolName': 'BMDA - Dengue Protocol',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [p300_mount, temperature, final_tubes] = get_values(  # noqa: F821
        "p300_mount", "temperature", "final_tubes")

    # Load Labware
    temp_mod = ctx.load_module('temperature module gen2', 10)
    reagents = temp_mod.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap')
    pcr_plate = ctx.load_labware(
        'opentrons_96_aluminumblock_generic_pcr_strip_200ul', 8)
    tiprack_200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 1)

    # Load Instruments
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=[tiprack_200ul])

    # Get Sample Wells
    mm = reagents.wells()[0]
    components = reagents.wells()[12:]
    volumes = [51, 85, 51, 119, 136, 34, 34, 34, 34, 34, 34, 34]
    final_tubes = int(final_tubes)

    # Set Temperature to 8C
    temp_mod.set_temperature(temperature)

    # Add Components to Master Mix
    p300.transfer(volumes, components, mm, new_tip='always')
    p300.pick_up_tip()
    p300.mix(5, 200, mm)
    p300.drop_tip()

    # Get well distribution for PCR plate
    pcr_plate_wells = [pcr_plate.columns()[i] for i in [0, 3, 6, 9]]
    pcr_plate_wells = [wells for well in pcr_plate_wells
                       for wells in well][:final_tubes]

    # Add Master Mix to 32 wells
    p300.transfer(20, mm, pcr_plate_wells, new_tip='once')

    # Deactivate Temp Mod
    temp_mod.deactivate()
