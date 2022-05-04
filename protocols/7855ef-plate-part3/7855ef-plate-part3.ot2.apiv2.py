"""OPENTRONS."""
import math
from opentrons.types import Point
from opentrons.protocol_api.labware import Well


metadata = {
    'protocolName': 'Agriseq Library Prep Part 3 - Barcoding (96)',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


class WellH(Well):
    def __init__(self, well, volume=0, min_height=1, comp_coeff=1.15,
                 current_volume=0):
        super().__init__(well._impl)
        self.well = well
        self.min_height = min_height
        self.comp_coeff = comp_coeff
        self.radius = self.well.diameter/2
        self.current_volume = current_volume
        self.theta = math.atan(self.radius/well.depth)
        self.height = (
            math.pi*((math.tan(self.theta))**2)*self.current_volume/3)**(1/3)

    def height_dec(self, vol):
        v2 = self.current_volume - vol*self.comp_coeff
        if v2 > 0:
            self.current_volume = v2
        else:
            self.current_volume = 0
        # calculate
        h2 = (
            self.current_volume*3/(math.pi*((math.tan(self.theta))**2)))**(
            1/3)
        if h2 > self.min_height:
            self.height = h2
        else:
            self.height = self.min_height
        return(self.well.bottom(self.height))

    def height_inc(self, vol):
        v2 = self.current_volume + vol*self.comp_coeff
        # calculate
        h2 = (math.pi*((math.tan(self.theta))**2)*v2/3)**(1/3)
        if h2 < self.depth:
            self.height = h2
        else:
            self.height = self.depth
        self.current_volume += vol
        return(self.well.bottom(self.height))


def run(protocol):
    """PROTOCOL."""
    [num_samp, m20_mount, start_vol] = get_values(  # noqa: F821
        "num_samp", "m20_mount", "start_vol")

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
        pip.move_to(knock_loc)
        pip.move_to(knock_loc2)

    # load reagents
    # 30% overage
    barcode_rxn_mix = WellH(mmx_plate.rows()[0][2],
                            current_volume=num_col*3*1.3)
    reaction_plate_cols = [col for plate in reaction_plates
                           for col in plate.rows()[0]][:num_col]
    barcode_plate_cols = [col for plate in barcode_plate
                          for col in plate.rows()[0]]
    # add barcode adapter
    airgap = 2
    for s, d in zip(barcode_plate_cols, reaction_plate_cols):
        pick_up()
        m20.aspirate(1, s)
        protocol.delay(seconds=3)
        m20.touch_tip(s, v_offset=-2, speed=20)
        m20.air_gap(airgap)
        m20.dispense(airgap, d.top())
        m20.dispense(1, d)
        m20.mix(2, 8, d)
        m20.blow_out()
        touchtip(m20, d)
        m20.return_tip()

    # add barcode reaction mix
    for col in reaction_plate_cols:
        m20.flow_rate.aspirate = 3
        m20.flow_rate.dispense = 3
        m20.flow_rate.blow_out = 3
        pick_up()
        # height_dec wants vol we will aspirate in (), this case 3 uL
        m20.aspirate(3, barcode_rxn_mix.height_dec(3))
        m20.air_gap(airgap)
        protocol.delay(seconds=3)
        m20.touch_tip(v_offset=-2, speed=20)
        m20.dispense(airgap, col.top())
        m20.dispense(1, col)
        m20.mix(2, 8, col)
        m20.move_to(col.top(-2))
        protocol.delay(seconds=3)
        m20.blow_out(col.top(z=-2))
        m20.touch_tip(v_offset=-2, speed=20)
        m20.return_tip()

    for c in protocol.commands():
        print(c)
    protocol.comment('''Barcoding sample libraries complete. Store at -20C after
                   centrifuge and PCR steps if needed as a break point''')
