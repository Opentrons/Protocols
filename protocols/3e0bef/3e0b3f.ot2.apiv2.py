from opentrons import protocol_api
from opentrons import types
from opentrons.protocol_api.labware import Well
import math
from types import MethodType

metadata = {
    'protocolName': 'Omega Bio-Tek Mag-Bind Plant DNA DS Kit',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):
    [
     _m300_mount,
     _num_samps,
     _samp_labware,
     _elution_vol
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
         '_m300_mount',
         '_num_samps',
         '_samp_labware',
         '_elution_vol')

    if not 1 <= _num_samps <= 96:
        raise Exception("The 'Number of Samples' should be between 1 and 96")

    # define all custom variables above here with descriptions:
    m300_mount = _m300_mount  # mount for 8-channel p300 pipette
    num_cols = math.ceil(_num_samps/8)  # number of sample columns
    samp_labware = _samp_labware  # labware containing sample
    elution_vol = _elution_vol  # volume of elution buffer

    # load modules
    mag_deck = ctx.load_module('magnetic module gen2', 7)

    # load labware
    rsvr_12 = [ctx.load_labware('nest_12_reservoir_15ml', s) for s in [2, 3]]
    rsvr_1 = ctx.load_labware('nest_1_reservoir_195ml', 10)
    pcr_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 1)
    samp_plate = ctx.load_labware(samp_labware, 4)
    mag_plate = mag_deck.load_labware('nest_96_wellplate_2ml_deep')

    # load tipracks
    tips = [
        ctx.load_labware(
            'opentrons_96_filtertiprack_200ul', s) for s in [5, 6, 8, 9, 11]
            ]
    all_tips = [t for rack in tips for t in rack.rows()[0]]
    t_start = 0
    t_end = int(num_cols)

    # load instrument
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tips)

    # extend well objects for improved liquid handling
    class WellH(Well):
        def __init__(self, well, min_height=2, comp_coeff=1.15,
                     current_volume=0):
            super().__init__(well._impl)
            self.well = well
            # specified minimum well bottom clearance
            self.min_height = min_height
            self.comp_coeff = comp_coeff
            # specified starting volume in ul
            self.current_volume = current_volume
            # cross sectional area
            if self.diameter is not None:
                self.radius = self.diameter/2
                cse = math.pi*(self.radius**2)
            elif self.length is not None:
                cse = self.length*self.width
            else:
                cse = None
            self.cse = cse
            # initial liquid level in mm from start vol
            if cse:
                self.height = (current_volume/cse)
            else:
                raise Exception("""Labware definition must
                supply well radius or well length and width.""")
            if self.height < min_height:
                self.height = min_height
            elif self.height > well.parent.highest_z:
                raise Exception("""Specified liquid volume
                can not exceed the height of the labware.""")

        def height_dec(self, vol, ppt, bottom=False):
            # decrement height (mm)
            dh = (vol/self.cse)*self.comp_coeff
            # tip immersion (mm) as fraction of tip length
            mm_immersed = 0.05*ppt._tip_racks[0].wells()[0].depth
            # decrement til target reaches specified min clearance
            self.height = self.height - dh if (
             (self.height - dh - mm_immersed) > self.min_height
             ) else self.min_height + mm_immersed
            self.current_volume = self.current_volume - vol if (
             self.current_volume - vol > 0) else 0
            tip_ht = self.height - mm_immersed if bottom is False else bottom
            return(self.well.bottom(tip_ht))

        def height_inc(self, vol, top=False):
            # increment height (mm)
            ih = (vol/self.cse)*self.comp_coeff
            # keep calculated liquid ht between min clearance and well depth
            self.height = self.min_height if (
             self.height < self.min_height) else self.height
            self.height = (self.height + ih) if (
             (self.height + ih) < self.depth) else self.depth
            # increment
            self.current_volume += vol
            if top is False:
                tip_ht = self.height
                return(self.well.bottom(tip_ht))
            else:
                return(self.well.top())

    # pipette functions   # INCLUDE ANY BINDING TO CLASS
    def aspirate_h(self, vol, source, rate=1, bottom=False):
        self.aspirate(
         vol, source.height_dec(vol, self, bottom=bottom), rate=rate)

    def dispense_h(self, vol, dest, rate=1, top=False):
        self.dispense(vol, dest.height_inc(vol, top=top), rate=rate)

    def slow_tip_withdrawal(
     self, speed_limit, well_location, to_surface=False):
        if self.mount == 'right':
            axis = 'A'
        else:
            axis = 'Z'
        previous_limit = None
        if axis in ctx.max_speeds.keys():
            for key, value in ctx.max_speeds.items():
                if key == axis:
                    previous_limit = value
        ctx.max_speeds[axis] = speed_limit
        if to_surface is False:
            self.move_to(well_location.top())
        else:
            if isinstance(well_location, WellH):
                self.move_to(well_location.bottom().move(types.Point(
                 x=0, y=0, z=well_location.height+(
                  20*(self._tip_racks[0].wells()[0].depth / 88)))))
            else:
                self.move_to(well_location.center())
        ctx.max_speeds[axis] = previous_limit

    def custom_pick_up(self, loc=None):
        nonlocal t_start
        nonlocal t_end
        """`custom_pick_up` will pause the protocol when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the protocol will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.

        :param loc: User can manually specify location for tip pick up
        """
        if loc:
            self.pick_up_tip(loc)
        else:
            try:
                self.pick_up_tip()
            except protocol_api.labware.OutOfTipsError:
                flash_lights()
                ctx.pause("Replace empty tip racks")
                self.reset_tipracks()
                t_start = 0
                t_end = int(num_cols)
                ctx.set_rail_lights(True)
                self.pick_up_tip()

    # bind additional methods to pipettes
    for met in [aspirate_h, dispense_h, slow_tip_withdrawal, custom_pick_up]:
        setattr(
         m300, met.__name__,
         MethodType(met, m300))

    # reagents
    liquid_waste = rsvr_1.wells()[0].top()
    cspl = [WellH(well) for well in rsvr_12[0].wells()[:6]]
    for idx in range(num_cols):
        cspl[idx//2].height_inc(720*8*1.1)

    # helper functions
    def flash_lights():
        for _ in range(19):
            ctx.set_rail_lights(not ctx.rail_lights_on)
            ctx.delay(seconds=0.5)

    def flow_rate(asp=92.86, disp=92.86):
        """
        This function can be used to quickly modify the flow rates of the m300
        If no parameters are entered, the flow rates will be
        reset.

        :param asp: Aspiration flow rate, in uL/sec
        :param disp: Dispense flow rate, in uL/sec
        """
        m300.flow_rate.aspirate = asp
        m300.flow_rate.dispense = disp

    def remove_supernatant(vol, src):
        while vol > 180:
            m300.aspirate_h(180, src)
            m300.dispense(180, liquid_waste)
            vol -= 180
        m300.aspirate_h(vol, src)
        m300.dispense(vol, liquid_waste)

    def wash(srcs, msg):
        nonlocal t_start
        nonlocal t_end

        if mag_deck.status == 'engaged':
            mag_deck.disengage()
        ctx.comment(f'\nPerforming wash step: {msg}\n')
        flow_rate()
        for idx, col in enumerate(mag_samps_h):
            m300.custom_pick_up()
            src = srcs[idx//3]
            for _ in range(2):
                m300.aspirate_h(180, src)
                m300.slow_tip_withdrawal(10, src, to_surface=True)
                m300.dispense(180, col.top(-2))
            m300.aspirate_h(165, src)
            m300.slow_tip_withdrawal(10, src, to_surface=True)
            m300.dispense(165, col.top(-2))
            m300.mix(10, 100, col)
            m300.slow_tip_withdrawal(10, col, to_surface=True)
            m300.drop_tip()

        mag_deck.engage()
        mag_msg = '\nIncubating on Mag Deck for 3 minutes\n'
        ctx.delay(minutes=3, msg=mag_msg)

        # Discard Supernatant
        ctx.comment(f'\nRemoving supernatant for wash: {msg}\n')
        t_start += num_cols
        t_end += num_cols
        for src, t_d in zip(mag_samps_h, all_tips[t_start:t_end]):
            m300.custom_pick_up()
            remove_supernatant(1025, src)
            m300.drop_tip(t_d)

    # plate, tube rack maps
    init_samps = samp_plate.rows()[0][:num_cols]
    mag_samps = mag_plate.rows()[0][:num_cols]
    mag_samps_h = [WellH(well) for well in mag_samps]
    pcr_samps = pcr_plate.rows()[0][:num_cols]

    # protocol
    ctx.set_rail_lights(True)
    # Transfer 700µL CSPL Buffer + 20µL Prot K
    ctx.comment('\nTransferring 720uL of CSPL Buffer + Proteinase K\n')

    m300.custom_pick_up()
    for idx, col in enumerate(init_samps):
        src = cspl[idx//2]
        for _ in range(4):
            m300.aspirate_h(180, src)
            m300.slow_tip_withdrawal(10, src, to_surface=True)
            m300.dispense(180, col.top(-2))
    m300.drop_tip()

    flash_lights()
    ctx.pause('Please remove samples and incubate at 56C for 30 minutes, \
    then centrifuge at 4000g for 10 minutes. Once complete, please replace \
    samples on the deck and place ensure 12-well reservoirs are filled with \
    necessary reagents in deck slots 2 and 3. When ready, click RESUME.')
    ctx.set_rail_lights(True)
    # Creating reagent variables for second part of protocol
    rbb = [WellH(well, current_volume=0) for well in rsvr_12[0].wells()[:6]]
    cspw1 = [WellH(well) for well in rsvr_12[0].wells()[6:10]]
    cspw2 = [WellH(well) for well in rsvr_12[1].wells()[:4]]
    spm1 = [WellH(well) for well in rsvr_12[1].wells()[4:8]]
    spm2 = [WellH(well) for well in rsvr_12[1].wells()[8:]]
    elution_buffer = [WellH(well) for well in rsvr_12[0].wells()[10:]]

    for idx in range(num_cols):
        rbb[idx//2].height_inc(525*8*1.1)
        cspw1[idx//3].height_inc(500*8*1.1)
        cspw2[idx//3].height_inc(500*8*1.1)
        spm1[idx//3].height_inc(500*8*1.1)
        spm2[idx//3].height_inc(500*8*1.1)
        cspw1[idx//6].height_inc(elution_vol*8*1.1)

    ctx.comment('\nTransferring 500uL of sample to plate on MagDeck\n')

    flow_rate(asp=20)
    for src, dest in zip(init_samps, mag_samps_h):
        m300.custom_pick_up()
        for i in range(2):
            m300.aspirate(180, src.bottom(7-i))
            m300.slow_tip_withdrawal(10, src)
            m300.dispense_h(180, dest)
        m300.aspirate(140, src.bottom(4))
        m300.dispense_h(140, dest)
        m300.drop_tip()
    flow_rate()

    # Transfer 5uL RNAse + 500uL RBB buffer + 20uL Mag-Bind Beads
    ctx.comment('\nTransferring 5uL RNAse + 500uL RBB buffer + \
    20uL Mag-Bind Beads\n')

    m300.custom_pick_up()
    for idx, col in enumerate(mag_samps):
        src = rbb[idx//2]
        for _ in range(2):
            m300.aspirate_h(180, src)
            m300.slow_tip_withdrawal(10, src, to_surface=True)
            m300.dispense(180, col.top(-2))
        m300.aspirate_h(165, src)
        m300.slow_tip_withdrawal(10, src, to_surface=True)
        m300.dispense(165, col.top(-2))
    m300.drop_tip()

    incubate_msg = '\nIncubating at room temperature for 10 minutes\n'
    ctx.delay(minutes=10, msg=incubate_msg)

    mag_deck.engage()
    mag_msg = '\nIncubating on Mag Deck for 3 minutes\n'
    ctx.delay(minutes=3, msg=mag_msg)

    # Discard Supernatant
    ctx.comment('\nRemoving supernatant\n')
    for src, t_d in zip(mag_samps_h, all_tips[t_start:t_end]):
        m300.custom_pick_up()
        remove_supernatant(1025, src)
        m300.drop_tip(t_d)

    # Wash with 500uL CSPW1 Buffer
    wash(cspw1, 'CSPW1')

    # Wash with 500uL CSPW2 Buffer
    wash(cspw2, 'CSPW2')

    # Wash with SPM Buffer (1)
    wash(spm1, 'SPM (first wash)')

    # Wash with SPM Buffer (2)
    wash(spm2, 'SPM (second wash)')

    # Air dry for 10 minutes
    air_dry_msg = '\nAir drying the beads for 10 minutes. \
    Please add elution buffer at 65C to 12-well reservoir.\n'
    ctx.delay(minutes=10, msg=air_dry_msg)

    # Add Elution Buffer
    ctx.comment(f'\nAdding {elution_vol}uL Elution Buffer to samples\n')

    m300.custom_pick_up()
    for idx, col in enumerate(mag_samps):
        src = elution_buffer[idx//6]
        m300.aspirate_h(elution_vol, src)
        m300.slow_tip_withdrawal(10, src, to_surface=True)
        m300.dispense(elution_vol, col.top(-2))
    m300.drop_tip()

    flash_lights()
    ctx.pause('Please remove samples and incubate at 65C for 5 minutes.\
    When complete, replace samples and click RESUME\n')
    ctx.set_rail_lights(True)

    # Transfer elution to PCR plate
    mag_deck.engage()
    mag_msg = '\nIncubating on Mag Deck for 3 minutes\n'
    ctx.delay(minutes=3, msg=mag_msg)

    ctx.comment(f'\nTransferring {elution_vol}uL to final PCR plate\n')
    t_start += num_cols
    if t_start >= 60:
        t_start -= 60

    flow_rate(asp=20)
    for src, dest, tip in zip(mag_samps, pcr_samps, all_tips[t_start:]):
        m300.custom_pick_up()
        m300.aspirate(elution_vol, src)
        m300.dispense(elution_vol, dest)
        m300.drop_tip(tip)

    mag_deck.disengage()
    ctx.comment('\nProtocol complete! Please store samples at -20C or \
    continue processing')
