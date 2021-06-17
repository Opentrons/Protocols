from opentrons import protocol_api, types

metadata = {
    'protocolName': 'Illumina COVIDSeq Test: Post Tagmentation Clean Up',
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
    wb = reservoir['A2']
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

    # Pellet Beads
    mag_mod.engage()
    ctx.delay(minutes=3, msg="Waiting for 3 minutes for beads to pellet.")

    # Remove Supernatant
    for col in plate_1_wells:
        pick_up(m300)
        remove_supernatant(60, col, trash, -1)
        m300.drop_tip()

    # Wash Buffer
    for col in plate_1_wells:
        pick_up(m300)
        m300.transfer(100, wb, col, new_tip='never')
        m300.drop_tip()

    # Shake and Centrifuge
    mag_mod.disengage()
    ctx.pause('''Seal, Shake and Centrifuge. Then place back on the
              Magnetic Module and click Resume.''')
    mag_mod.engage()
    ctx.delay(minutes=3, msg="Waiting for 3 minutes for beads to pellet.")

    # Remove Supernatant
    for col in plate_1_wells:
        pick_up(m300)
        remove_supernatant(100, col, trash, -1)
        m300.drop_tip()

    # Wash Buffer
    for col in plate_1_wells:
        pick_up(m300)
        m300.transfer(100, wb, col, new_tip='never')
        m300.drop_tip()
