from opentrons.types import Point
import math

metadata = {
    'protocolName': 'MAI VIRAL ISOLATION',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [num_samples, m300_mount] = get_values(  # noqa: F821
        "num_samples", "m300_mount")

    num_samples = int(num_samples)

    # Load Labware
    mag_mod = ctx.load_module('magnetic module', '1')
    mag_mod.disengage()
    plate = mag_mod.load_labware('nest_96_wellplate_2000ul',
                                 'Extraction Plate')
    res = ctx.load_labware('usascientific_12_reservoir_22ml',
                           '2', 'Reagent Reservoir')
    trash = ctx.loaded_labwares[12].wells()[0]

    # Load Tip Racks
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_200ul',
                                 slot) for slot in range(4, 11)]

    # Load Pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks)
    max_vol = m300.tip_racks[0].wells()[0].max_volume

    # Samples Setup
    num_cols = math.ceil(num_samples/8)
    mag_samples = plate.rows()[0][:num_cols]

    # Reagent Reservoir Liquids
    etoh = res.wells()[:2]
    wash1 = res.wells()[2:4]
    wash2_1 = res.wells()[4:7]
    wash2_2 = res.wells()[7:10]
    elution_buffer = res.wells()[10]
    mag_beads = res.wells()[11]

    def shake(well, reps, shake_mode, z_offset=-2):
        if shake_mode == 'lateral':
            radius = well.geometry._length/2
            shake_locs = [well.top().move(Point(x=side*radius/2,
                          y=0, z=z_offset))
                          for side in [-1, 1]]
            print(f'Performing {shake_mode} shakes!')
            for _ in range(reps):
                for loc in shake_locs:
                    m300.move_to(loc)
        elif shake_mode == 'vertical':
            shake_locs = [well.top().move(Point(x=0, y=0, z=side*z_offset))
                          for side in [-1, 1]]
            print(f'Performing {shake_mode} shakes!')
            for _ in range(reps):
                for loc in shake_locs:
                    m300.move_to(loc)

    # Split large volumes into smaller volumes
    def split_volume(vol, max_vol):
        vols = []
        while vol > max_vol:
            vols.append(max_vol)
            vol -= max_vol
            if vol <= max_vol:
                vols.append(vol)
                break
        return vols

    # Transfer to Trash
    def transfer_trash(vol, asp_rate, disp_rate, asp_delay, disp_delay,
                       **kwargs):
        m300.flow_rate.aspirate = asp_rate
        m300.flow_rate.dispense = disp_rate
        for m in mag_samples:
            m300.pick_up_tip()
            if vol > max_vol:
                for i in split_volume(vol, max_vol):
                    m300.aspirate(i, m.bottom(1))
                    ctx.delay(seconds=asp_delay)
                    if "touch_tip_offset" in kwargs:
                        m300.touch_tip(v_offset=kwargs['touch_tip_offset'])
                    m300.dispense(i, trash.bottom(0.5))
                    shake(trash, 10, 'lateral')
                    ctx.delay(seconds=disp_delay)
            else:
                m300.aspirate(vol, m.bottom(1))
                ctx.delay(seconds=asp_delay)
                m300.touch_tip(v_offset=kwargs['touch_tip_offset'])
                m300.dispense(vol, trash.bottom(0.5))
                shake(trash, 10, 'lateral')
                ctx.delay(seconds=disp_delay)
            m300.drop_tip()

    def mag_mod_switch(switches=[0, 1, 0, 1, 0, 1, 0, 1, 1, 1]):
        for val in switches:
            if val == 0:
                mag_mod.disengage()
            else:
                mag_mod.engage(height=4.1)

    def regular_transfer(vol, source, delay_asp={}, delay_disp={}, shakes={},
                         mix_before=[], mix_after=[], **kwargs):
        if kwargs['new_tip'] == 'once':
            m300.pick_up_tip()
        if 'disp_flow_rate' in kwargs:
            m300.flow_rate.dispense = kwargs['disp_flow_rate']
        for i, wells in enumerate(mag_samples):
            if kwargs['new_tip'] == 'always':
                m300.pick_up_tip()
            if mix_before:
                if 'div_cols' in kwargs:
                    m300.mix(*mix_before, source[i//kwargs['div_cols']])
                else:
                    m300.mix(*mix_before, source)
            if vol > max_vol:
                for k in split_volume(vol, max_vol):
                    if 'div_cols' in kwargs:
                        m300.aspirate(k, source[i//kwargs['div_cols']].bottom(
                                      kwargs['asp_height']))
                    else:
                        m300.aspirate(k, source)
                    if delay_asp:
                        ctx.delay(**delay_asp)
                    if "touch_tip_offset" in kwargs:
                        m300.touch_tip(v_offset=kwargs['touch_tip_offset'])
                    m300.dispense(k, wells.bottom(kwargs['disp_height']))
                    if mix_after:
                        m300.mix(*mix_after, wells)
                    if delay_disp:
                        ctx.delay(**delay_disp)
                    if 'touch_tip_disp_offset' in kwargs:
                        m300.touch_tip(
                            v_offset=kwargs['touch_tip_disp_offset'])
                    if 'shake_type' in kwargs:
                        if 'div_cols' in kwargs:
                            shake(source[i//kwargs['div_cols']], 10,
                                  kwargs['shake_type'])
                        else:
                            shake(source, 10, kwargs['shake_type'])
            else:
                if 'div_cols' in kwargs:
                    m300.aspirate(vol, source[i//kwargs['div_cols']].bottom(
                                  kwargs['asp_height']))
                else:
                    m300.aspirate(vol, source)
                if delay_asp:
                    ctx.delay(**delay_asp)
                if "touch_tip_offset" in kwargs:
                    m300.touch_tip(v_offset=kwargs['touch_tip_offset'])
                m300.dispense(vol, wells.bottom(kwargs['disp_height']))
                if mix_after:
                    m300.mix(*mix_after, wells)
                if delay_disp:
                    ctx.delay(**delay_disp)
                if 'touch_tip_disp_offset' in kwargs:
                    m300.touch_tip(v_offset=kwargs['touch_tip_disp_offset'])
                if 'shake_type' in kwargs:
                    if 'div_cols' in kwargs:
                        shake(source[i//kwargs['div_cols']],
                              10, kwargs['shake_type'])
                    else:
                        shake(source, 10, kwargs['shake_type'])
            if kwargs['new_tip'] == 'always':
                m300.drop_tip()
        if kwargs['new_tip'] == 'once':
            m300.drop_tip()

    # Protocol Steps

    # Transfer EtOH (Steps 2-3)
    ctx.comment('Transferring EtOH')
    regular_transfer(150, source=etoh, disp_flow_rate=200,
                     delay_asp={'seconds': 2}, shake_type='vertical',
                     asp_height=1, disp_height=42, div_cols=6, new_tip='once')

    # Transfer Mag Beads (Step 4)
    ctx.comment('Transfer Mag Beads')
    regular_transfer(150, source=mag_beads, disp_flow_rate=200,
                     shake_type='vertical', mix_before=[5, 50],
                     mix_after=[10, 50], asp_height=1, disp_height=6,
                     new_tip='always')

    # Delay for bead incubation (Steps 5-8)
    ctx.delay(minutes=2, msg='Bead Incubation')
    mag_mod.engage(height=4.1)
    mag_mod.engage(height=4.1)
    ctx.delay(minutes=6, msg='Bead Binding')

    # Transfer to Trash (Step 9)
    transfer_trash(600, 50, 20, 2, 5, touch_tip_offset=32)
    mag_mod.disengage()

    # Transfer Wash Buffer 1 (Steps 11-12)
    regular_transfer(300, source=wash1, disp_flow_rate=200,
                     delay_asp={'seconds': 2}, shake_type='vertical',
                     asp_height=1, disp_height=50, touch_tip_offset=34.2,
                     div_cols=6, new_tip='once')

    # Delay for bead incubation (Steps 13-15)
    ctx.delay(seconds=30, msg='Wash Buffer 1 Incubation')
    mag_mod.engage(height=4.1)
    ctx.delay(seconds=30, msg='Bead Binding')

    # Mag Mod (Steps 16-25)
    mag_mod_switch()

    # Steps 26-27
    transfer_trash(600, 50, 20, 2, 5, touch_tip_offset=32)
    mag_mod.disengage()

    # Wash Buffer 2 (Steps 28-30)
    regular_transfer(400, source=wash2_1, disp_flow_rate=200,
                     delay_asp={'seconds': 10}, delay_disp={'seconds': 4},
                     shake_type='vertical', asp_height=1, disp_height=50,
                     touch_tip_offset=34.2, div_cols=4, new_tip='once')

    # Delay for bead incubation (Steps 31-33)
    ctx.delay(seconds=30, msg='Wash Buffer 2 Incubation')
    mag_mod.engage(height=4.1)
    ctx.delay(seconds=30, msg='Bead Binding')

    # Mag Mod Switching (Steps 34-45)
    mag_mod_switch()
    transfer_trash(600, 50, 20, 3, 5)
    mag_mod.disengage()

    # Wash Buffer 2 (Steps 46-48)
    regular_transfer(400, source=wash2_2, disp_flow_rate=200,
                     delay_asp={'seconds': 10}, delay_disp={'seconds': 4},
                     shake_type='vertical', asp_height=1, disp_height=50,
                     touch_tip_offset=34.2, div_cols=4, new_tip='once')

    # Delay for bead incubation (Steps 49-51)
    ctx.delay(seconds=30, msg='Wash Buffer 2 second wash incubation')
    mag_mod.engage(height=4.1)
    ctx.delay(seconds=30, msg='Wash Buffer 2 second wash bead binding')

    # Steps 52-64
    mag_mod_switch()
    transfer_trash(600, 50, 20, 3, 5)
    mag_mod.disengage()
    ctx.pause(msg='10 min at 55oC')

    # Transfer Elution Buffer Step 65
    regular_transfer(25, source=elution_buffer, disp_flow_rate=200,
                     shake_type='vertical', mix_after=[30, 25], asp_height=1,
                     disp_height=1.5, touch_tip_offset=33.2,
                     touch_tip_disp_offset=32, new_tip='always')

    # Steps 66-68
    ctx.delay(minutes=2, msg='Elution Incubation')
    mag_mod.engage(height=4.1)
    ctx.delay(minutes=1, msg='Bead Binding')

    # Steps 69-78
    mag_mod_switch(switches=[0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
