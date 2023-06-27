import time
from opentrons import protocol_api
from opentrons import types
from opentrons.protocol_api.labware import Well
import math
from types import MethodType
import subprocess
from opentrons.protocols.api_support.types import APIVersion

metadata = {
    'protocolName': 'Omega Bio-Tek Mag-Bind Environmental DNA 96 Kit',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}

AUDIO_FILE_PATH = '/etc/audio/speaker-test.mp3'


def run_quiet_process(command):
    subprocess.check_output('{} &> /dev/null'.format(command), shell=True)


def test_speaker(song=AUDIO_FILE_PATH):
    try:
        run_quiet_process('mpg123 {}'.format(song))
    except KeyboardInterrupt:
        pass


def run(ctx: protocol_api.ProtocolContext):
    [
     _m300_mount,
     lw_deepwell_plate,
     _num_samps,
     vol_xp1,
     vol_removal,
     _mag_time,
     _air_dry,
     _elution_vol,
     flow_rate_wash,
     _off_deck,
     _music
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
         '_m300_mount',
         'lw_deepwell_plate',
         '_num_samps',
         'vol_xp1',
         'vol_removal',
         '_mag_time',
         '_air_dry',
         '_elution_vol',
         'flow_rate_wash',
         '_off_deck',
         '_music')

    _inc_time = 10
    _fin_wash = 600

    if not 1 <= _num_samps <= 96:
        raise Exception('The Number of Samples should be between 1 and 96')

    # define all custom variables above here with descriptions

    m300_mount = _m300_mount  # mount for 8-channel p300 pipette
    num_cols = math.ceil(_num_samps/8)  # number of sample columns
    elution_vol = _elution_vol  # volume of elution buffer
    inc_time = _inc_time  # time for binding step
    mag_time = _mag_time  # time on magnetic module
    air_dry = _air_dry  # time for air drying
    fin_wash = _fin_wash  # volume for final wash removal
    off_deck = _off_deck  # True/False perform resuspension off-deck
    music = _music  # play custom music (only in Oregon)

    mag_deck = ctx.load_module('magnetic module gen2', 1)

    # load labware
    rsvr_12 = [ctx.load_labware('nest_12_reservoir_15ml', s) for s in [2, 3]]
    rsvr_1 = ctx.load_labware('nest_1_reservoir_195ml', 4)
    pcr_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 10)
    # Eluted DNA
    # samp_plate = ctx.load_labware(samp_labware, 4)
    mag_plate = mag_deck.load_labware(lw_deepwell_plate)

    # load tipracks
    tips = [
        ctx.load_labware(
            'opentrons_96_filtertiprack_200ul', s) for s in [5, 6, 7, 8, 9, 11]
            ]
    # all_tips = [t for rack in tips for t in rack.rows()[0]]
    t_start = 0
    t_end = int(num_cols)

    # load instrument
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tips)

    # extend well objects for improved liquid handling
    class WellH(Well):
        def __init__(self, well, min_height=0.5, comp_coeff=1.1,
                     current_volume=0):
            super().__init__(well.parent, well._core, APIVersion(2, 13))
            # super().__init__(well._impl)
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
                raise Exception('Labware definition must \
supply well radius or well length and width.')
            if self.height < min_height:
                self.height = min_height
            elif self.height > well.parent.highest_z:
                raise Exception('Specified liquid volume \
can not exceed the height of the labware.')

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
            return self.well.bottom(tip_ht)

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
                return self.well.bottom(tip_ht)
            else:
                return self.well.top()

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
        # `custom_pick_up` will pause the protocol when tip boxes are out of
        # tips, prompting the user to replace all tip racks. Once tipracks are
        # reset, the protocol will start picking up tips from the first tip
        # box as defined in the slot order when assigning the labware def
        # for that tip box. `pick_up()` will track tips for both pipettes if
        # applicable.

        # :param loc: User can manually specify location for tip pick up

        if loc:
            self.pick_up_tip(loc)
        else:
            try:
                self.pick_up_tip()
            except protocol_api.labware.OutOfTipsError:
                flash_lights()
                ctx.pause('Replace empty tip racks')
                self.reset_tipracks()
                t_start = 0
                t_end = int(num_cols)
                self.pick_up_tip()

    # bind additional methods to pipettes
    for met in [aspirate_h, dispense_h, slow_tip_withdrawal, custom_pick_up]:
        setattr(
         m300, met.__name__,
         MethodType(met, m300))

    # reagents
    liquid_waste = rsvr_1.wells()[0].top()
    # cspl = [WellH(well) for well in rsvr_12[0].wells()[:6]]
    # for idx in range(num_cols):
    #     cspl[idx//2].height_inc(720*8*1.1)

    # helper functions
    def flash_lights():
        initial_status = ctx.rail_lights_on
        for _ in range(19):
            ctx.set_rail_lights(not ctx.rail_lights_on)
            ctx.delay(seconds=0.25)
        ctx.set_rail_lights(initial_status)

    def mix_high_low(well, reps, vol, z_offset_low=1.0, z_offset_high=10.0,
                     x_offset=2.0, y_offset=1.0, pip=m300,
                     switch_sides_x=True):

        tip_ref_vol = pip.tip_racks[0].wells()[0].max_volume
        if pip.current_volume + vol >= tip_ref_vol - 10:
            vol_actual = tip_ref_vol - m300.current_volume
        else:
            vol_actual = vol

        for i in range(reps):
            if switch_sides_x:
                x_side = 1 if i % 2 == 0 else -1
            else:
                x_side = 1
            y_side = 1 if (i//2) % 2 == 0 else -1
            pip.aspirate(vol_actual, well.bottom().move(types.Point(
                x=x_side*x_offset, y=y_side*y_offset, z=z_offset_low)))
            pip.dispense(vol_actual, well.bottom().move(types.Point(
                x=x_side*x_offset, y=y_side*y_offset, z=z_offset_high)))

    def flow_rate(asp=92.86, disp=92.86, blow=92.86):
        # This function can be used to quickly modify the flow rates of the
        # pipette. If no parameters are entered, the flow rates will be
        # reset.

        # :param asp: Aspiration flow rate, in uL/sec
        # :param disp: Dispense flow rate, in uL/sec

        m300.flow_rate.aspirate = asp
        m300.flow_rate.dispense = disp
        m300.flow_rate.blow_out = blow

    def remove_supernatant(vol, src):
        w = int(str(src).split(' ')[0][1:])
        if src.width is not None:
            radi = float(src.width)/4
        else:
            radi = float(src.diameter)/4
        x0 = radi if w % 2 == 0 else -radi
        while vol > 180:
            m300.aspirate(180, src.bottom().move(types.Point(x=x0, y=0, z=1)))
            m300.dispense(200, liquid_waste)
            m300.blow_out()
            m300.aspirate(20, liquid_waste)
            vol -= 180
        m300.aspirate(vol, src.bottom().move(types.Point(x=x0, y=0, z=0.7)))
        m300.dispense(vol+20, liquid_waste)
        m300.blow_out()
        m300.aspirate(10, liquid_waste)

    def wash(srcs, msg, sup=600):
        if mag_deck.status == 'engaged':
            mag_deck.disengage()
        ctx.comment(f'Performing wash step: {msg}')
        flow_rate()
        for idx, (col, src) in enumerate(zip(mag_samps_h, srcs)):
            m300.custom_pick_up()

            # src = srcs[idx//3]
            for i in range(2):
                flow_rate(asp=flow_rate_wash, disp=flow_rate_wash)
                if i == 1:
                    m300.dispense(20, src.top(-1))
                    m300.dispense(20, src)
                m300.mix(1, 200, src)
                flow_rate()
                m300.aspirate(200, src)
                m300.slow_tip_withdrawal(10, src, to_surface=True)
                m300.dispense(180, col.top(-2))
                flow_rate(asp=10)
                m300.aspirate(20, col.top())
            m300.dispense(20, src.top())
            flow_rate()
            m300.mix(1, 140, src)
            m300.aspirate(140, src)
            m300.slow_tip_withdrawal(10, src, to_surface=True)
            m300.dispense(140, col)
            if not off_deck:
                side = 1 if idx % 2 == 0 else -1
                radius = col.diameter/2 if col.diameter else col.width/2
                # bead_loc = col.bottom().move(
                #     types.Point(x=side*radius*0.5, z=3))
                mix_high_low(col, 10, 190, z_offset_low=3,
                             x_offset=side*radius*0.4, switch_sides_x=False)
            ctx.delay(seconds=5)
            m300.slow_tip_withdrawal(10, col, to_surface=True)
            m300.blow_out()
            m300.touch_tip(speed=40)
            m300.aspirate(10, col.top())
            m300.drop_tip()

        if off_deck:
            flash_lights()
            ctx.pause('Please remove plate for manual resuspension')

        mag_deck.engage(7)
        mag_msg = f'Incubating on Mag Deck for {mag_time} minutes'
        ctx.delay(minutes=mag_time, msg=mag_msg)

        # Discard Supernatant
        ctx.comment(f'Removing supernatant for wash: {msg}')
        for src in mag_samps_h:
            m300.custom_pick_up()
            remove_supernatant(sup, src)
            m300.return_tip()

    # plate, tube rack maps
    # init_samps = samp_plate.rows()[0][:num_cols]
    mag_samps = mag_plate.rows()[0][:num_cols]
    mag_samps_h = [WellH(well) for well in mag_samps]
    pcr_samps = pcr_plate.rows()[0][:num_cols]

    # protocol
    ctx.set_rail_lights(True)
    # # Transfer 700µL CSPL Buffer + 20µL Prot K
    # ctx.comment('Transferring 720uL of CSPL Buffer + Proteinase K')
    #
    # m300.custom_pick_up()
    # for idx, col in enumerate(init_samps):
    #     src = cspl[idx//2]
    #     for _ in range(4):
    #         m300.aspirate_h(180, src)
    #         m300.slow_tip_withdrawal(10, src, to_surface=True)
    #         m300.dispense(180, col.top(-2))
    # m300.drop_tip()
    #
    # flash_lights()
    # ctx.pause('Please remove samples and incubate at 56C for 30 minutes, \
    # then centrifuge at 4000g for 10 minutes. Once complete, please replace \
    # samples on the deck and place ensure 12-well reservoirs are filled with \
    # necessary reagents in deck slots 2 and 3. When ready, click RESUME.')
    # ctx.set_rail_lights(True)
    # Creating reagent variables for second part of protocol
    xp1 = [WellH(well, current_volume=0) for well in rsvr_12[0].wells()[:4]]
    vhb = [WellH(well) for well in rsvr_12[0].wells()[4:8]]
    # cspw2 = [WellH(well) for well in rsvr_12[0].wells()[8:]]
    etoh = [WellH(well) for well in rsvr_12[1].wells()[:8]]
    elution_buffer = [WellH(well) for well in rsvr_12[1].wells()[10:]]

    vhb_wells = []
    # cspw2_wells = []
    etoh1_wells = []
    etoh2_wells = []
    elution_wells = []

    for idx in range(num_cols):
        xp1[idx//3].height_inc(vol_xp1*8)
        vhb[idx//3].height_inc(500*8)
        # cspw2[idx//3].height_inc(500*8)
        elution_buffer[idx//6].height_inc(elution_vol*8)
        vhb_wells.append(vhb[idx//3])
        # cspw2_wells.append(cspw2[idx//3])
        elution_wells.append(elution_buffer[idx//6])

    for idx in range(num_cols*2):
        etoh[idx//3].height_inc(500*8)
        if idx % 2 == 0:
            etoh1_wells.append(etoh[idx//3])
        else:
            etoh2_wells.append(etoh[idx//3])

    reagent_keys = {
        'XP1 + Mag-Bind Beads': xp1,
        'VHB Buffer': vhb,
        # 'CSPW 2 Buffer': cspw2,
        'Elution Buffer': elution_buffer,
        'ETOH': etoh
    }
    for key in reagent_keys:
        for x in reagent_keys[key]:
            ctx.comment(f'load {x.current_volume} of {key} in {x}')

    # for x in rbb:
    #     ctx.comment(f'load {x.current_volume} in {x}')

    # if samp_labware == 'qiagen_96_tuberack_1200ul':
    #    ctx.comment('Transferring 500uL of sample to plate on MagDeck')

    #    flow_rate(asp=20)
    #   for src, dest in zip(init_samps, mag_samps_h):
    #        src_asp = src.top(-asp_ht)
    #        m300.custom_pick_up()
    #        for i in range(2):
    #            m300.aspirate(20, src.top())
    #            m300.aspirate(180, src_asp)
    #            m300.slow_tip_withdrawal(10, src)
    #            m300.dispense_h(180, dest)
    #            m300.slow_tip_withdrawal(10, dest, to_surface=True)
    #            m300.dispense(20, dest.bottom(5))
    #        m300.aspirate(20, src.top())
    #        m300.aspirate(140, src_asp)
    #        m300.dispense_h(140, dest)
    #        m300.slow_tip_withdrawal(10, dest, to_surface=True)
    #        m300.dispense(20, dest.bottom(5))
    #        m300.drop_tip()
    #    flow_rate()
    # else:
    #    flash_lights()
    #    ctx.pause('Please make sure samples are loaded on MagDeck')

    # Transfer vol XP1/ Mag-bind Beads master mixture
    ctx.comment('Transferring XP1/ Mag-bind master mixture')

    m300.custom_pick_up()
    flow_rate(blow=10)
    for idx, dest in enumerate(mag_samps):
        src = xp1[idx//3]
        for _ in range(2):
            flow_rate(asp=40, disp=40)
            mix_high_low(src, 5, 190)
            m300.aspirate(vol_xp1/2, src)
            m300.slow_tip_withdrawal(10, src, to_surface=True)
            flow_rate(disp=10)
            m300.dispense(60, dest.top(-1))
            flow_rate(disp=5)
            m300.dispense(50, dest.top(-1))
            ctx.delay(seconds=3)
            m300.dispense(30, dest.top(-1))
            ctx.delay(seconds=3)
            flow_rate(disp=2)
            m300.dispense(20, dest.top(-1))
            m300.blow_out()
            m300.touch_tip(speed=40)
    m300.drop_tip()
    flow_rate()

    if off_deck:
        flash_lights()
        ctx.pause('Please incubate samples for 10 minutes post resuspension.')
    else:
        incubate_msg = f'Incubating at room temperature for {inc_time} \
        minutes plus mixing'
        ctx.comment(incubate_msg)

        m300.flow_rate.aspirate *= 3
        m300.flow_rate.dispense *= 3
        check_time = 8*60 if not ctx.is_simulating() else 0.05
        parking_spots = []
        first_pickup = True
        start_time = time.monotonic()

        while time.monotonic() - start_time < check_time:
            for i, col in enumerate(mag_samps):
                side = 1 if i % 2 == 0 else -1
                radius = col.diameter/2 if col.diameter else col.width/2
                bead_loc = col.bottom().move(types.Point(
                    x=side*radius*0.5, z=3))
                if first_pickup:
                    if not m300.has_tip:
                        m300.custom_pick_up()
                    parking_spots.append(m300._last_tip_picked_up_from)
                    if i == len(mag_samps) - 1:
                        first_pickup = False
                else:
                    if not m300.has_tip:
                        m300.custom_pick_up(parking_spots[i])

                mix_high_low(col, 10, 190, z_offset_low=3,
                             x_offset=side*radius*0.4, switch_sides_x=False)
                ctx.delay(seconds=1)
                m300.blow_out(col.top(-2))
                m300.touch_tip()
                if len(mag_samps) > 1:
                    m300.drop_tip(parking_spots[i])
                else:
                    ctx.delay(seconds=30)
        if m300.has_tip:
            m300.drop_tip(parking_spots[i])
        m300.flow_rate.aspirate /= 3
        m300.flow_rate.dispense /= 3

    mag_deck.engage(7)
    mag_msg = f'Incubating on Mag Deck for {mag_time} minutes'
    ctx.delay(minutes=mag_time, msg=mag_msg)

    # Discard Supernatant
    ctx.comment('Removing supernatant')
    flow_rate(asp=40, disp=40)
    for src in mag_samps_h:
        m300.custom_pick_up()
        remove_supernatant(vol_removal, src)
        # m300.drop_tip()
        # m300.custom_pick_up()
        # remove_supernatant(vol_removal/2, src)
        m300.return_tip()

    flow_rate()

    # Wash with 500uL VHB Buffer
    wash(vhb_wells, 'VHB')

    # Wash with 500uL CSPW2 Buffer
    # wash(cspw2_wells, 'CSPW2')

    # Wash with 70% ETOH (1)
    wash(etoh1_wells, 'ETOH (first wash)')
    # Wash with ETOH Buffer (2)
    wash(etoh2_wells, 'ETOH (second wash)', fin_wash)
    ctx.delay(minutes=1)
    for i, src in enumerate(mag_samps_h):
        side = -1 if i % 2 == 0 else 1
        radius = src.diameter/2 if src.diameter else src.width/2
        anti_bead_loc = src.bottom().move(
            types.Point(x=side*radius*0.5, z=3))
        m300.custom_pick_up()
        flow_rate(asp=30, disp=30)
        m300.aspirate(100, anti_bead_loc)
        ctx.delay(seconds=0.5)
        m300.dispense(120, liquid_waste)
        flow_rate()
        m300.blow_out()
        m300.drop_tip()

    # Air dry for 10 minutes
    mag_deck.engage(7)
    # if add_water:
    #     for i, src in enumerate(mag_samps_h):
    #         side = -1 if i % 2 == 0 else 1
    #         radius = src.diameter/2 if src.diameter else src.width/2
    #         anti_bead_loc = src.bottom().move(
    #             types.Point(x=side*radius*0.5, z=3))
    #         m300.custom_pick_up()
    #         m300.aspirate(100, h2o)
    #         flow_rate(asp=30, disp=30)
    #         m300.dispense(80, anti_bead_loc)
    #         ctx.delay(seconds=0.5)
    #         m300.aspirate(100, anti_bead_loc)
    #         flow_rate()
    #         m300.dispense(120, liquid_waste)
    #         m300.blow_out()
    #         m300.drop_tip()

    # ctx.delay(minutes=1)
    # for i, src in enumerate(mag_samps_h):
    #     side = -1 if i % 2 == 0 else 1
    #     radius = src.diameter/2 if src.diameter else src.width/2
    #     anti_bead_loc = src.bottom().move(
    #         types.Point(x=side*radius*0.5, z=3))
    #     m300.custom_pick_up()
    #     flow_rate(asp=30, disp=30)
    #     m300.aspirate(100, anti_bead_loc)
    #     ctx.delay(seconds=0.5)
    #     m300.dispense(120, liquid_waste)
    #     flow_rate()
    #     m300.blow_out()
    #     m300.drop_tip()

    ctx.home()
    air_dry_msg = f'Air drying the beads for {air_dry} minutes. \
Please add elution buffer at 70C to 12-well reservoir.'
    ctx.delay(minutes=air_dry, msg=air_dry_msg)
    flash_lights()
    if not ctx.is_simulating():
        if music:
            test_speaker('/var/lib/jupyter/notebooks/mr-blue-sky-ot2.mp3')
        else:
            test_speaker()
    ctx.pause('Please check the Well Plate')

    mag_deck.disengage()
    # Add Elution Buffer
    ctx.comment(f'Adding {elution_vol}uL Elution Buffer to samples')

    for idx, (col, src) in enumerate(zip(mag_samps_h, elution_wells)):
        m300.custom_pick_up()
        m300.aspirate(elution_vol, src)
        m300.slow_tip_withdrawal(10, src, to_surface=True)
        m300.dispense_h(elution_vol, col)
        if not off_deck:
            side = 1 if idx % 2 == 0 else -1
            radius = col.diameter/2 if col.diameter else col.width/2
            bead_loc = col.bottom().move(
                types.Point(x=side*radius*0.5, z=3))
            mix_high_low(col, 10, 50, z_offset_low=3, z_offset_high=6,
                         x_offset=side*radius*0.4, switch_sides_x=False)
        m300.slow_tip_withdrawal(10, col, to_surface=True)
        m300.blow_out(col.bottom(6))
        for _ in range(2):
            m300.move_to(col.bottom(5))
            m300.move_to(col.bottom(6))
        m300.drop_tip()

    # Transfer elution to PCR plate
    if not off_deck:
        start_time = time.monotonic()
        check_time = 8*60 if not ctx.is_simulating() else 0.05
        tip_list = []
        first = True
        while time.monotonic() - start_time < check_time:
            for i, col in enumerate(mag_samps_h):
                if first:
                    m300.custom_pick_up()
                    current_tip = m300._last_tip_picked_up_from
                    tip_list.append(current_tip)
                    if i == len(mag_samps_h) - 1:
                        first = False
                else:
                    m300.pick_up_tip(tip_list[i])
                side = 1 if idx % 2 == 0 else -1
                radius = col.diameter/2 if col.diameter else col.width/2
                bead_loc = col.bottom().move(
                    types.Point(x=side*radius*0.5, z=3))
                m300.mix(10, 50, bead_loc)
                m300.slow_tip_withdrawal(10, col, to_surface=True)
                m300.blow_out(col.bottom(6))
                for _ in range(2):
                    m300.move_to(col.bottom(5))
                    m300.move_to(col.bottom(6))
                m300.return_tip()
    else:
        flash_lights()
        ctx.home()
        if not ctx.is_simulating():
            if music:
                test_speaker('/var/lib/jupyter/notebooks/all-i-want-ot2.mp3')
            else:
                test_speaker()
        # ctx.pause('Please remove samples and incubate at 65C for 5 minutes.\
        # When complete, replace samples and click RESUME')
        ctx.pause('Please remove samples and mix off-deck for 10 minutes \
then resume run.')

    mag_deck.engage(7)
    mag_msg = f'Incubating on Mag Deck for {mag_time} minutes.'
    ctx.delay(minutes=mag_time, msg=mag_msg)

    ctx.comment(f'Transferring {elution_vol}uL to final PCR plate')
    t_start += num_cols
    if t_start >= 60:
        t_start -= 60

    flow_rate(asp=20)
    for src, dest in zip(mag_samps, pcr_samps):
        w = int(str(src).split(' ')[0][1:])
        if src.width is not None:
            radi = float(src.width)/4
        else:
            float(src.diameter)/4
        x0 = radi if w % 2 == 0 else -radi
        m300.custom_pick_up()
        m300.aspirate(
            elution_vol, src.bottom().move(types.Point(x=x0, y=0, z=1)))
        m300.dispense(elution_vol, dest)
        m300.return_tip()

    mag_deck.disengage()
    ctx.comment('Protocol complete! Please store samples at -20C or \
continue processing')
