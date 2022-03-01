import math
from opentrons.protocol_api.labware import OutOfTipsError
from opentrons import types

metadata = {
    'protocolName': '''ArcBio RNA Workflow Continuous:
    Pre-PCR Instrument: Part-2: cDNA Synthesis''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.11'
}


def run(ctx):

    # get parameter values from json above
    [clearance_bead_resuspension, offset_x_resuspension, count_samples,
     clearance_reservoir, height_engage, time_engage, offset_x,
     time_dry] = get_values(  # noqa: F821
      'clearance_bead_resuspension', 'offset_x_resuspension', 'count_samples',
      'clearance_reservoir', 'height_engage', 'time_engage', 'offset_x',
      'time_dry')

    ctx.set_rail_lights(True)

    if not 1 <= count_samples <= 96:
        raise Exception('Invalid sample count (must be 1-96).')

    num_cols = math.ceil(count_samples / 8)

    # helper functions

    # pause, flash lights, notify user
    def pause_attention(message):
        ctx.set_rail_lights(False)
        ctx.delay(seconds=5)
        ctx.set_rail_lights(True)
        ctx.delay(seconds=5)
        ctx.set_rail_lights(False)
        ctx.pause(message)

    # notify user to replenish tips
    def pick_up_or_refill(pip, vol=200):
        nonlocal tipCtr
        try:
            if vol == 200:
                pip.pick_up_tip()
            else:
                if tipCtr < len(tips300.rows()[0]):
                    pip.pick_up_tip(tips300.rows()[0][tipCtr])
                    tipCtr += 1
                else:
                    tipCtr = 0
                    pause_attention(
                     """Please Refill the 300 uL Tip Box
                     and Empty the Tip Waste""")
                    pip.pick_up_tip(tips300.rows()[0][tipCtr])
                    tipCtr += 1
        except OutOfTipsError:
            pause_attention(
             """Please Refill the {} Tip Boxes
             and Empty the Tip Waste""".format(pip))
            pip.reset_tipracks()
            pip.pick_up_tip()

    # set liquid volume
    def liq_volume(wells, vol):
        for well in wells:
            well.liq_vol = vol

    # return liquid height in a well
    def liq_height(well):
        if well.diameter is not None:
            radius = well.diameter / 2
            cse = math.pi*(radius**2)
        elif well.length is not None:
            cse = well.length*well.width
        else:
            cse = None
        if cse:
            return well.liq_vol / cse
        else:
            raise Exception("""Labware definition must
                supply well radius or well length and width.""")

    # tips, p20 multi, p300 multi
    tips20 = [ctx.load_labware(
     "opentrons_96_filtertiprack_20ul", str(slot)) for slot in [10, 11]]
    p20m = ctx.load_instrument(
        "p20_multi_gen2", 'left', tip_racks=tips20)
    tips200 = [
     ctx.load_labware(
      "opentrons_96_filtertiprack_200ul", str(slot)) for slot in [7, 8]]
    tips300 = ctx.load_labware("opentrons_96_tiprack_300ul", 9)
    tipCtr = 0
    p300m = ctx.load_instrument(
        "p300_multi_gen2", 'right', tip_racks=tips200)

    # reagents block for EDTA, RT Master Mix 1, RT Master Mix 2
    reagents = ctx.load_labware(
     'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '2', 'Reagents')
    [edta, rt_mm1, rt_mm2] = [reagents.columns()[index] for index in [0, 1, 2]]

    # reservoir for beads and tris
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '5', 'Reservoir')

    beads = reservoir.wells()[:3]
    liq_volume(beads, 9600)

    tris = reservoir.wells()[-1]

    # reservoir for 80 percent ethanol
    etoh = ctx.load_labware(
     'nest_1_reservoir_195ml', '6', '80 percent etoh').wells()[0]
    liq_volume([etoh], 144000)
    waste = ctx.load_labware(
     'nest_1_reservoir_195ml', '4', '80 percent etoh').wells()[0]

    # input samples
    temp = ctx.load_module('temperature module gen2', '3')
    sampleplate200 = temp.load_labware(
     'eppendorftwin.tec96_96_aluminumblock_200ul',
     "Sample Plate at 4 Degrees")
    temp.set_temperature(4)

    # magnetic module with deep well plate
    mag = ctx.load_module('magnetic module gen2', '1')
    mag.disengage()
    mag_plate = mag.load_labware(
     'corning_96_wellplate_600ul', 'Mag Plate')

    ctx.comment("STEP - EDTA")
    p20m.transfer(
     0.8, edta,
     [column[0] for column in sampleplate200.columns()[:num_cols]],
     mix_after=(1, 10), new_tip='always')

    ctx.comment("STEP - Transfer to larger plate")
    p300m.transfer(
     80.8, [column[0] for column in sampleplate200.columns()[:num_cols]],
     [column[0] for column in mag_plate.columns()[:num_cols]])

    ctx.comment("STEP - RNA Concentration and RT setp 1")

    def beadwells():
        yield from beads

    beadwell = beadwells()
    source = next(beadwell)
    reps = math.ceil(240 / tips300.wells()[0].max_volume)

    for column in mag_plate.columns()[:num_cols]:
        if source.liq_vol <= 1920:
            source = next(beadwell)
        for rep in range(reps):
            pick_up_or_refill(p300m, 300)
            p300m.aspirate(240 / reps, source, rate=0.5)
            ctx.delay(seconds=1)
            source.liq_vol -= (1920 / reps)
            p300m.dispense(240 / reps, column[0])
            if reps != 0:
                p300m.mix(10, 200)
            p300m.drop_tip()

    pause_attention(
        ''' Remove plate from magnetic module. Incubate 4 degree C at least
        15 minutes. Return the plate to the magnetic module and resume.''')

    mag.engage(height=height_engage)
    ctx.delay(minutes=time_engage)

    # remove supernatant
    for index, column in enumerate(mag_plate.columns()[:num_cols]):
        pick_up_or_refill(p300m)
        p300m.aspirate(200, column[0].bottom(4), rate=0.33)
        p300m.dispense(200, waste.top())
        p300m.aspirate(
         50, column[0].bottom(1).move(types.Point(
          x={True: 1}.get(not index % 2, -1)*offset_x, y=0, z=0)), rate=0.33)
        p300m.drop_tip()

    for repeat in range(2):
        # add ethanol
        pick_up_or_refill(p300m, 300)
        for column in mag_plate.columns()[:num_cols]:
            for rep in range(3):
                etoh.liq_vol -= 1520
                p300m.aspirate(190, etoh.bottom(liq_height(etoh)-3))
                p300m.air_gap(10)
                p300m.dispense(200, column[0].top())
                ctx.delay(seconds=0.5)
                p300m.blow_out()
        p300m.drop_tip()

        ctx.delay(seconds=30)

        # remove sup
        for column in mag_plate.columns()[:num_cols]:
            pick_up_or_refill(p300m)
            for rep in range(3):
                clearance = 5 if not rep == 2 else 2
                p300m.aspirate(190, column[0].bottom(clearance))
                p300m.air_gap(10)
                p300m.dispense(200, waste.top())
                ctx.delay(seconds=0.5)
                p300m.blow_out()
            p300m.drop_tip()

    mag.disengage()

    # air dry bead pellets
    ctx.delay(minutes=time_dry)

    # resuspend bead pellet in Tris
    for index, column in enumerate(mag_plate.columns()[:num_cols]):
        p20m.pick_up_tip()
        p20m.aspirate(13, tris.bottom(clearance_reservoir))
        p20m.dispense(
         13, column[0].bottom(clearance_bead_resuspension).move(types.Point(
          x={True: -1}.get(not index % 2, 1)*offset_x_resuspension, y=0, z=0)))
        p20m.mix(10, 13)
        p20m.drop_tip()

    ctx.delay(minutes=5)

    mag.engage(height=height_engage)
    ctx.delay(minutes=time_engage)

    pause_attention(
     '''Place a fresh 200 uL PCR plate on the temperature module. Resume.''')

    # combine RT master mix 1 and eluted sample
    for column in sampleplate200.columns()[:num_cols]:
        pick_up_or_refill(p20m)
        p20m.transfer(6, rt_mm1, column[0], new_tip='never')
        p20m.drop_tip()

    for index, column in enumerate(mag_plate.columns()[:num_cols]):
        pick_up_or_refill(p20m)
        p20m.transfer(
         11, column[0].bottom().move(types.Point(
          x={True: 1}.get(not index % 2, -1)*offset_x, y=0, z=0)),
         sampleplate200.columns()[index][0],
         mix_after=(10, 15), new_tip='never')
        p20m.drop_tip()

    pause_attention(
     '''Remove the 200 uL PCR plate for off-deck cycler steps.
     Return plate and resume.''')

    ctx.comment("STEP - cDNA Synthesis")

    # add RT master mix 2
    for column in sampleplate200.columns()[:num_cols]:
        pick_up_or_refill(p20m)
        p20m.transfer(6, rt_mm2, column[0], new_tip='never')
        p20m.drop_tip()

    pause_attention(
     '''cDNA Synthesis protocol complete. Proceed to off deck cycler steps
     and cDNA Library Prep protocol''')
