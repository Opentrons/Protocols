from opentrons import protocol_api, types

metadata = {
    'protocolName': 'Illumina COVIDSeq Test: Amplify Tagmented Amplicons',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [m300_mount] = get_values(  # noqa: F821
        "m300_mount")

    # Labware
    tips200ul = ctx.load_labware('opentrons_96_filtertiprack_200ul', 4)
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 1,
                                 "Master Mix Reservoir")
    mag_mod = ctx.load_module('magnetic module gen2', 3)
    plate_1 = mag_mod.load_labware('biorad_96_wellplate_200ul_pcr')

    # Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=[tips200ul])

    # Wells
    plate_1_wells = plate_1.rows()[0]
    mm = reservoir['A3']
    trash = ctx.loaded_labwares[12]['A1']

    # Helper Functions
    def remove_supernatant(vol, src, dest, side):
        m300.flow_rate.aspirate = 20
        m300.aspirate(10, src.top())
        while vol > 200:
            m300.aspirate(
                200, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
            m300.dispense(200, dest)
            m300.aspirate(10, dest)
            vol -= 200
        m300.aspirate(vol, src.bottom().move(types.Point(x=side, y=0, z=0.5)))
        m300.dispense(vol, dest)
        m300.dispense(10, dest)
        m300.flow_rate.aspirate = 50

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Please replace the tips and click Resume.")
            pip.reset_tipracks()
            pip.pick_up_tip()

    # Protocol Steps

    # Engage Mag Mod
    mag_mod.engage()

    # Remove Supernatant
    for col in plate_1_wells:
        pick_up(m300)
        remove_supernatant(120, col, trash, -1)
        m300.drop_tip()

    # Transfer AMP Master Mix
    for col in plate_1_wells:
        pick_up(m300)
        m300.transfer(40, mm, col, new_tip='never')
        m300.drop_tip()
