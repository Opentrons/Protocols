"""OPENTRONS."""
import math
from opentrons.types import Point


metadata = {
    'protocolName': 'Agriseq Library Prep Part 3 - Barcoding (96)',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(protocol):
    """PROTOCOL."""
    [num_samp, m20_mount, overage_percent] = get_values(  # noqa: F821
     "num_samp", "m20_mount", "overage_percent")

    if not 1 <= num_samp <= 288:
        raise Exception("Enter a sample number between 1-288")

    num_col = math.ceil(num_samp/8)
    tip_counter = 0

    # load labware
    barcode_plate = [protocol.load_labware('customendura_96_wellplate_200ul',
                                           str(slot),
                                           label='Ion Barcode Plate')
                     for slot in [1, 2, 3]]
    reaction_plates = [protocol.load_labware('customendura_96_wellplate_200ul',
                       str(slot), label='Reaction Plate')
                       for slot in [4, 5, 6]]
    mmx_plate = protocol.load_labware('customendura_96_wellplate_200ul', '7',
                                      label='MMX Plate')
    tiprack20 = [protocol.load_labware('opentrons_96_filtertiprack_20ul',
                 str(slot))
                 for slot in [8, 9, 10, 11]]
    # load instruments
    m20 = protocol.load_instrument('p20_multi_gen2', m20_mount,
                                   tip_racks=tiprack20)
    tips = [col for tipbox in tiprack20 for col in tipbox.rows()[0]]

    # liquid height tracking
    overage_percent = (overage_percent/100)+1
    v_naught = 3*num_samp*overage_percent/8
    h_naught = 3.77*(v_naught)**(1/3)
    h = h_naught

    def adjust_height(vol):
        nonlocal h
        dh = 3.77*(vol)**(1/3)
        h -= dh
        if h < 3:
            h = 1

    def pick_up():
        nonlocal tip_counter
        if tip_counter == 48:
            protocol.home()
            protocol.pause('Replace 20 ul tip racks on Slots 8, 9, 10, and 11')
            m20.reset_tipracks()
            tip_counter = 0
            pick_up()
        else:
            m20.pick_up_tip(tips[tip_counter])
            tip_counter += 1

    def touchtip(pip, well):
        knock_loc = well.top(z=-1).move(
                    Point(x=-(well.diameter/2.25)))
        knock_loc2 = well.top(z=-1).move(
                    Point(x=(well.diameter/2.25)))
        center = well.center()
        pip.move_to(knock_loc)
        pip.move_to(knock_loc2)
        pip.move_to(center)

    # load reagents
    # 30% overage
    barcode_rxn_mix = mmx_plate.rows()[0][2]
    reaction_plate_cols = [col for plate in reaction_plates
                           for col in plate.rows()[0]][:num_col]
    barcode_plate_cols = [col for plate in barcode_plate
                          for col in plate.rows()[0]]
    # add barcode adapter
    airgap = 2
    for s, d in zip(barcode_plate_cols, reaction_plate_cols):
        pick_up()
        m20.aspirate(1, s)
        m20.air_gap(airgap)
        m20.dispense(airgap, d.top())
        m20.dispense(1, d)
        m20.mix(2, 8, d)
        m20.blow_out()
        m20.return_tip()

    # add barcode reaction mix
    for col in reaction_plate_cols:
        m20.flow_rate.aspirate = 1.5
        m20.flow_rate.dispense = 1.5
        m20.flow_rate.blow_out = 1.5
        pick_up()
        m20.aspirate(3, barcode_rxn_mix.bottom(h))
        m20.move_to(barcode_rxn_mix.top(-1))
        protocol.delay(seconds=2)
        m20.touch_tip()
        m20.move_to(barcode_rxn_mix.top(-1))
        m20.aspirate(airgap, barcode_rxn_mix.top(-1))
        m20.dispense(airgap, col.top())
        m20.dispense(3, col)
        m20.flow_rate.aspirate = 3
        m20.flow_rate.dispense = 3
        m20.mix(2, 8, col)
        m20.blow_out(col.top(z=-1))
        m20.touch_tip()
        m20.move_to(col.top(z=-1))
        m20.return_tip()
        adjust_height(3)

    for c in protocol.commands():
        print(c)
    protocol.comment('''Barcoding sample libraries complete. Store at -20C after
                   centrifuge and PCR steps if needed as a break point''')
