from opentrons import types

metadata = {
    'protocolName': 'Illumina COVIDSeq Test: Amplify cDNA',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [m20_mount] = get_values(  # noqa: F821
        "m20_mount")

    # Labware
    tips200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 10)
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 7,
                                 "Master Mix Reservoir")
    plate_1 = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 11,
                               "Plate CPP1")
    plate_2 = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 8,
                               "Plate CPP2")

    # Pipettes
    m20 = ctx.load_instrument('p300_multi_gen2', m20_mount,
                              tip_racks=[tips200ul])

    # Wells
    plate_1_wells = plate_1.rows()[0]
    plate_2_wells = plate_2.rows()[0]

    # Helper Functions
    def distribute(pipette, vol, source, dest, disposal_vol, asp_height,
                   disp_height):

        use_vol = 200 - disposal_vol
        num_distribute = use_vol // vol

        def well_lists(wells, n):
            for i in range(0, len(wells), n):
                yield wells[i:i + n]

        asp_vols = []

        def calc_vol(wells, vol):

            for wells in dest_wells:
                aspirate_vol = vol*len(wells) + disposal_vol
                asp_vols.append(aspirate_vol)

        dest_wells = list(well_lists(dest, int(num_distribute)))
        calc_vol(dest_wells, vol)

        # Aspirate from source
        pipette.pick_up_tip()
        for wells, asp_vol in zip(dest_wells, asp_vols):
            pipette.aspirate(asp_vol, source.bottom(z=asp_height))

            # Add Movement Path Code Here
            pipette.move_to(ctx.deck.position_for('4').move(types.Point(z=50)))

            for well in wells:
                pipette.dispense(vol, well.bottom(z=disp_height))
            pipette.dispense(disposal_vol, source.bottom(z=asp_height))
        pipette.drop_tip()

    # Protocol Steps
    distribute(m20, 20, reservoir['A1'], plate_1_wells, 0, 1, 1)
    distribute(m20, 20, reservoir['A12'], plate_2_wells, 0, 1, 1)
