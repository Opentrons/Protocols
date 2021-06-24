from opentrons import types

metadata = {
    'protocolName': 'Illumina COVIDSeq Test: Synthesize First Strand cDNA',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [m20_mount, reservoir_type] = get_values(  # noqa: F821
        "m20_mount", "reservoir_type")

    # Labware
    tips200ul = [ctx.load_labware('opentrons_96_filtertiprack_20ul',
                 slot) for slot in [10, 7]]
    reservoir = ctx.load_labware(reservoir_type, 4, "Master Mix Reservoir")
    plate_1 = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 11, "Plate 1")
    plate_2 = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 8, "Plate 2")

    # Pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tips200ul)

    # Wells
    plate_1_wells = plate_1.rows()[0]
    plate_2_wells = plate_2.rows()[0]
    mm = reservoir['A1']

    # Helper Functions
    def transfer(pipette, vol, src, dest):
        for well in dest:
            pipette.pick_up_tip()
            pipette.aspirate(vol, src)
            pipette.move_to(ctx.deck.position_for('1').move(types.Point(x=20,
                            y=31.5, z=100)))
            pipette.dispense(vol, well)
            pipette.drop_tip()

    # Protocol Steps
    transfer(m20, 8, mm, plate_1_wells)
    if reservoir_type == 'biorad_96_wellplate_200ul_pcr':
        ctx.pause('''Please refill the master mix before continuing to Plate 2.
                Click Resume when ready.''')
    transfer(m20, 8, mm, plate_2_wells)
