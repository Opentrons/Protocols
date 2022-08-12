import math
from opentrons.types import Point

metadata = {
    'protocolName': 'Agriseq Library Prep Part 1 - DNA transfer',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(protocol):

    [num_samp, m20_mount, overage_percent] = get_values(  # noqa: F821
        "num_samp", "m20_mount", "overage_percent")

    if not 1 <= num_samp <= 384:
        raise Exception("Enter a sample number between 1-384")

    num_col = math.ceil(num_samp/8)

    tip_counter = 0

    # load labware
    sample_plates = [protocol.load_labware(
                    'fisherscientific_96_wellplate_200ul',
                     str(slot), label='Sample Plate') for slot in [1, 2, 3, 4]]
    reaction_plate = protocol.load_labware(
                    'microamp_384_wellplate_100ul', '5',
                    label='Reaction Plate')
    mmx_plate = protocol.load_labware('customendura_96_wellplate_200ul', '6',
                                      label='MMX Plate')
    tiprack20 = [protocol.load_labware('opentrons_96_filtertiprack_20ul',
                                       str(slot))
                 for slot in [7, 8, 9, 10, 11]]

    # load instruments
    m20 = protocol.load_instrument('p20_multi_gen2', m20_mount,
                                   tip_racks=tiprack20)

    tips = [col for tipbox in tiprack20 for col in tipbox.rows()[0]]

    overage_coef = (overage_percent/100)+1
    v_naught = 7*num_col*overage_coef
    # starting height minus 2.5mm, using % isn't enough
    h_naught = (1.92*(v_naught)**(1/3))-2.5
    h = h_naught

    def adjust_height(vol):
        nonlocal v_naught
        nonlocal h
        # below if/else needed to avoid complex number error
        if v_naught - vol > 0:
            v_naught = v_naught - vol
        else:
            v_naught = 0
        h = (1.92*(v_naught)**(1/3))-2.5
        if h < 3:
            h = 1

    def touchtip(pip, well):
        knock_loc = well.top(z=-2).move(
                    Point(x=-(well.diameter/2.5)))
        knock_loc2 = well.top(z=-2).move(
                Point(x=(well.diameter/2.5)))
        pip.move_to(knock_loc)
        pip.move_to(knock_loc2)

    def pick_up():
        nonlocal tip_counter
        if tip_counter == 60:
            protocol.home()
            protocol.pause('Replace 20 ul tip racks')
            m20.reset_tipracks()
            tip_counter = 0
            pick_up()
        else:
            m20.pick_up_tip(tips[tip_counter])
            tip_counter += 1

    sample_plate_cols = [col for plate in sample_plates
                         for col in plate.rows()[0]][:num_col]
    reaction_plate_cols = [col for j in range(2) for i in range(2)
                           for col in reaction_plate.rows()[i][j::2]][:num_col]

    # load reagents
    amplify_mix = mmx_plate.rows()[0][:2]

    # add amplification mix
    airgap = 2
    num = 0
    m20.flow_rate.aspirate = 1.5
    m20.flow_rate.dispense = 1.5
    m20.flow_rate.blow_out = 1.5
    pick_up()
    for col in reaction_plate_cols:
        if num > 192:
            amplify_mix_well = amplify_mix[1]
        else:
            amplify_mix_well = amplify_mix[0]
        m20.aspirate(7, amplify_mix_well.bottom(h))
        m20.move_to(amplify_mix_well.top(-2))
        protocol.delay(seconds=2)
        m20.touch_tip(v_offset=-2)
        m20.move_to(amplify_mix_well.top(-2))
        m20.aspirate(airgap, amplify_mix_well.top())
        m20.dispense(airgap, col.top())
        protocol.delay(seconds=2)
        m20.dispense(7, col)
        m20.blow_out(col.top(z=-2))
        m20.touch_tip(v_offset=-2)
        m20.move_to(col.top(-2))
        adjust_height(7)
        num += 8
    m20.return_tip()
    protocol.comment('\n\n\n\n')

    # add DNA
    m20.flow_rate.aspirate = 7.6
    m20.flow_rate.dispense = 7.6
    m20.flow_rate.blow_out = 7.6
    for s, d in zip(sample_plate_cols, reaction_plate_cols):
        pick_up()
        m20.aspirate(3, s)
        m20.aspirate(airgap, s.top(-1))
        touchtip(m20, s)
        m20.dispense(airgap, d.top())
        m20.dispense(3, d)
        m20.mix(2, 5, d)
        m20.blow_out()
        touchtip(m20, d)
        m20.return_tip()

    protocol.home()
    protocol.pause('''Protocol method complete. Please remove reaction plates
                   from deck and proceed with PCR and centrifuge steps.
                   Return reaction plates back to deck and continue to
                   Part 2 - Pre-ligation.''')
