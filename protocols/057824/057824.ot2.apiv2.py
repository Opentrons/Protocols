import math
import time
import csv
from opentrons import types


metadata = {
    'protocolName': '''Custom Mass Spec Sample Prep''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.13'
}


def run(ctx):

    # get parameter values from json above
    [engage_height, target_temp_passive_cooling,
     sample_positions_csv, parameters_csv] = get_values(  # noqa: F821
      'engage_height', 'target_temp_passive_cooling', 'sample_positions_csv',
      'parameters_csv')

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    csvinput = [line for line in csv.DictReader(parameters_csv.splitlines())]

    samplepositions = [line[
     'Sample Position'] for line in csv.DictReader(
     sample_positions_csv.splitlines())]

    count_samples = len(samplepositions)

    # filter tips, p20 single, p300 single
    tips20 = [
     ctx.load_labware("opentrons_96_filtertiprack_20ul", str(
      slot)) for slot in [2]]
    tips300 = [
     ctx.load_labware("opentrons_96_filtertiprack_200ul", str(
      slot)) for slot in [6, 7, 11]]
    p20s = ctx.load_instrument(
        "p20_single_gen2", 'left', tip_racks=tips20)
    p300s = ctx.load_instrument(
        "p300_single_gen2", 'right', tip_racks=tips300)

    tips300park = ctx.load_labware(
     "opentrons_96_filtertiprack_200ul", '8', 'empty rack for tip parking')

    # yield next parking spot
    def parkingspots():

        yield from tips300park.wells()

    # heater shaker in slot 3 with WORKING_PLATE
    hs_mod = ctx.load_module('heaterShakerModuleV1', '3')

    lbwr = 'opentrons_96_pcr_adapter_nest_wellplate_100ul_pcr_full_skirt' if \
        csvinput[0]['WORKING_PLATE'] == \
        'nest_96_wellplate_100ul_pcr_full_skirt' else \
        'opentrons_96_pcr_adapter_biorad_wellplate_200ul'

    hs_plate = hs_mod.load_labware(
     lbwr, 'Heater Shaker Plate')

    # magnetic module in slot 1 with WORKING_PLATE
    mag = ctx.load_module('magnetic module gen2', '1')
    mag_plate = mag.load_labware(
     csvinput[0]['WORKING_PLATE'],
     'Magnetic Module Plate')
    mag.disengage()

    # source tubes for beadmixture, alk, red
    eppendorfrack = ctx.load_labware(
     'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
     '5', 'rack with 1.5 mL Eppendorf tubes')
    [beadmixture, alk, red] = [
     eppendorfrack.wells_by_name()[well] for well in ['A1', 'A2', 'A3']]

    # source tubes for 80 percent EtOH, ACN
    tentuberack = ctx.load_labware(
     'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical',
     '4', 'rack with 15 mL and 50 mL Falcon tubes')
    [etoh, acn] = [tentuberack.wells_by_name()[well] for well in ['A3', 'A4']]

    # etoh and acn initial volume
    etoh.liq_vol = int(csvinput[0]['V(EtOH)'])
    acn.liq_vol = int(csvinput[0]['V(ACN)'])

    # list of dig source tubes
    diglist = [tentuberack.wells_by_name()[
     'A1']] if '6x15ml' in csvinput[0]['DIG_VESSEL'].split('_') else [
     well for row in eppendorfrack.rows(
     ) for well in row if well.well_name not in [
      'A1', 'A2', 'A3']][:math.ceil((float(
       csvinput[0]['V(DIG)'])*count_samples)/1400)]

    # initial volume in dig source tubes
    for well in diglist:
        if '6x15ml' in csvinput[0]['DIG_VESSEL'].split('_'):
            # 15 mL tube filled with V(DIG) uL per sample plus 100 uL deadvol
            well.liq_vol = float(
             csvinput[0]['V(DIG)'])*count_samples + 100
        else:
            # eppendorfs always filled with 1500 uL
            well.liq_vol = 1500

    # yield next dig tube
    def digtubes():

        yield from diglist

    digtube = digtubes()

    final_plate = ctx.load_labware(
     csvinput[0]['FINAL_PLATE'], '9', 'final plate')

    reservoir = ctx.load_labware('nest_1_reservoir_195ml', '10', 'reservoir')

    """
    calculated values and checks
    """
    samplevolume = sum([float(csvinput[0][param]) for param in [
     'V(Sample)', 'V(RED first time)', 'V(ALK)', 'V(RED second time)',
     'V(Bead Mixture)']])

    ctx.comment(
     "\n***\nCalculated Sample Volume {}\n***\n".format(samplevolume))

    v_acn_calculated = samplevolume*(int(csvinput[0][
     'ACN_CONC']) / (100 - int(csvinput[0]['ACN_CONC'])))

    ctx.comment("\n***\nV(ACN calculated) {}\n***\n".format(v_acn_calculated))

    v_binding = samplevolume + v_acn_calculated

    ctx.comment("\n***\nCalculated V(BINDING) {}\n***\n".format(v_binding))

    # avoid over-fill of working plate and final plate
    for plate, v in zip([hs_plate, final_plate],
                        [(v_binding, 'V(BINDING)'),
                         (float(csvinput[0]['V(DIG)']), 'V(DIG)')]):
        limit = plate.wells()[0].max_volume
        if v[0] > limit:
            raise Exception(
             '''\n***\nPlanned {} volume {}
             exceeds well capacity {} in {}\n***\n'''.format(
              v[1], v[0], limit, plate))

    # check list of sample locations
    if not 1 <= count_samples <= 96:
        raise Exception(
             '''\n***\nSpecified sample count {} must be 1-96\n***\n'''.format(
              count_samples))

    if not len(set(samplepositions)) == count_samples:
        raise Exception(
             '''\n***\nSpecified sample positions must be unique\n***\n''')

    # return liquid height in a well
    def liq_height(well, effective_diameter=None):
        if well.diameter:
            if effective_diameter:
                radius = effective_diameter / 2
            else:
                radius = well.diameter / 2
            csa = math.pi*(radius**2)
        else:
            csa = well.length*well.width
        return well.liq_vol / csa

    ctx.comment(
     "STEP 1 - put Sample Plate on hs, set temperature to 60 C and wait")

    # open latch and place plate
    hs_mod.open_labware_latch()
    ctx.comment("\n***\nHeater Shaker latch status {}\n***\n".format(
     hs_mod.labware_latch_status))
    ctx.pause(
     """\n***\nPlace the Sample Plate
     on the Heater Shaker (slot 1). Resume\n***\n""")

    # close latch
    hs_mod.close_labware_latch()
    ctx.comment("\n***\nHeater Shaker latch status {}\n***\n".format(
     hs_mod.labware_latch_status))

    # set temperature and wait
    ctx.comment(
     "\n***\nHeater Shaker current temperature {}\n***\n".format(
      hs_mod.current_temperature))
    hs_mod.set_target_temperature(celsius=60)
    hs_mod.wait_for_temperature()
    ctx.comment(
     "\n***\nHeater Shaker current temperature {}\n***\n".format(
      hs_mod.current_temperature))

    ctx.comment(
     "\n***\nSTEP 2 - Distribute V(RED first time) to samples\n***\n")

    vol = float(csvinput[0]['V(RED first time)'])

    volpreairgap = 0.1*vol

    pipette = p20s if (vol + volpreairgap) <= 20 else p300s

    tipcapacity = 20 - volpreairgap if (vol + volpreairgap) <= 20 else 200

    reps = math.ceil(vol / tipcapacity)

    v = vol / reps

    source = red

    pipette.pick_up_tip()

    for well in [hs_plate.wells_by_name()[
     name] for name in samplepositions]:

        sideways_offset = well.diameter / 2

        vertical_offset = -5

        # dispense below well top, to northern side wall
        disp_loc = well.top(vertical_offset).move(
         types.Point(x=0, y=sideways_offset, z=0))

        for rep in range(reps):

            pipette.move_to(source.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            pipette.aspirate(v, source.bottom(1))
            pipette.touch_tip(radius=0.75, v_offset=-2, speed=10)

            pipette.move_to(well.top())
            pipette.move_to(well.top(vertical_offset))
            pipette.move_to(disp_loc)
            pipette.dispense(v+volpreairgap, disp_loc, rate=2)
            ctx.delay(seconds=0.5)

    pipette.drop_tip()

    ctx.comment("\n***\nSTEP 3 - 1500 rpm 30 sec\n***\n")

    # start shaking
    hs_mod.set_and_wait_for_shake_speed(rpm=1500)
    ctx.delay(seconds=1)
    ctx.comment(
     "\n***\nHeater-Shaker rpm {}\n***\n".format(hs_mod.current_speed))

    # wait
    ctx.delay(seconds=29)

    # shake at 1000 rpm
    hs_mod.set_and_wait_for_shake_speed(rpm=1000)
    ctx.delay(seconds=1)
    ctx.comment(
     "\n***\nHeater-Shaker rpm {}\n***\n".format(hs_mod.current_speed))

    ctx.comment(
     """\n***\nSTEP 4-5 - 30 min incubation
     with passive cooling and 1000 rpm shaking of heater shaker\n***\n""")

    # incubate while cooling and report current temperature
    for rep in range(10):
        ctx.delay(minutes=3)
        ctx.comment(
         "\n***\nHeater Shaker current temperature {}\n***\n".format(
          hs_mod.current_temperature))

    # stop heating
    hs_mod.deactivate_heater()

    # stop shaking
    hs_mod.deactivate_shaker()

    ctx.comment(
     "\n***\nSTEP 6 - wait for room temp, distribute V(ALK) to samples\n***\n")

    if not ctx.is_simulating():
        while hs_mod.current_temperature > target_temp_passive_cooling:
            time.sleep(30)
            continue

    ctx.comment(
         "\n***\nHeater Shaker current temperature {}\n***\n".format(
          hs_mod.current_temperature))

    vol = float(csvinput[0]['V(ALK)'])

    volpreairgap = 0.1*vol

    pipette = p20s if (vol + volpreairgap) <= 20 else p300s

    tipcapacity = 20 - volpreairgap if (vol + volpreairgap) <= 20 else 200

    reps = math.ceil(vol / tipcapacity)

    v = vol / reps

    source = alk

    pipette.pick_up_tip()

    for well in [hs_plate.wells_by_name()[name] for name in samplepositions]:

        sideways_offset = well.diameter / 2

        vertical_offset = -5

        # dispense below well top, to southern side wall
        disp_loc = well.top(vertical_offset).move(
         types.Point(x=0, y=-sideways_offset, z=0))

        for rep in range(reps):
            pipette.move_to(source.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            pipette.aspirate(v, source.bottom(1))
            pipette.touch_tip(radius=0.75, v_offset=-2, speed=10)

            pipette.move_to(well.top())
            pipette.move_to(well.top(vertical_offset))
            pipette.move_to(disp_loc)
            pipette.dispense(v+volpreairgap, disp_loc, rate=2)
            ctx.delay(seconds=0.5)

    pipette.drop_tip()

    ctx.comment("\n***\nSTEP 7 - 1500 rpm 30 sec\n***\n")

    # start shaking
    hs_mod.set_and_wait_for_shake_speed(rpm=1500)
    ctx.delay(seconds=1)
    ctx.comment("\n***\nHeater-Shaker rpm {}\n***\n".format(
     hs_mod.current_speed))

    # wait
    ctx.delay(seconds=29)

    # shake at 1000 rpm
    hs_mod.set_and_wait_for_shake_speed(rpm=1000)
    ctx.delay(seconds=1)
    ctx.comment(
     "\n***\nHeater-Shaker rpm {}\n***\n".format(hs_mod.current_speed))

    ctx.comment(
     "\n***\nSTEP 8 - 30 min incubation with 1000 rpm shaking\n***\n")

    ctx.delay(minutes=30)

    # stop shaking
    hs_mod.deactivate_shaker()

    ctx.comment(
     "\n***\nSTEP 9 - Distribute V(RED second time) to samples\n***\n")

    vol = float(csvinput[0]['V(RED second time)'])

    volpreairgap = 0.1*vol

    pipette = p20s if (vol + volpreairgap) <= 20 else p300s

    tipcapacity = 20 - volpreairgap if (vol + volpreairgap) <= 20 else 200

    reps = math.ceil(vol / tipcapacity)

    v = vol / reps

    source = red

    pipette.pick_up_tip()

    for well in [hs_plate.wells_by_name()[name] for name in samplepositions]:

        sideways_offset = well.diameter / 2

        vertical_offset = -5

        # dispense below well top, to eastern side wall
        disp_loc = well.top(vertical_offset).move(
         types.Point(x=sideways_offset, y=0, z=0))

        for rep in range(reps):

            pipette.move_to(source.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            pipette.aspirate(v, source.bottom(1))
            pipette.touch_tip(radius=0.75, v_offset=-2, speed=10)

            pipette.move_to(well.top())
            pipette.move_to(well.top(vertical_offset))
            pipette.move_to(disp_loc)
            pipette.dispense(v+volpreairgap, disp_loc, rate=2)
            ctx.delay(seconds=0.5)

    pipette.drop_tip()

    ctx.comment(
     "\n***\nSTEP 10 - 15 min incubation with 1000 rpm shaking\n***\n")

    # shake at 1000 rpm
    hs_mod.set_and_wait_for_shake_speed(rpm=1000)
    ctx.delay(seconds=1)
    ctx.comment(
     "\n***\nHeater-Shaker rpm {}\n***\n".format(hs_mod.current_speed))

    ctx.delay(minutes=15)

    # stop shaking
    hs_mod.deactivate_shaker()

    ctx.comment(
     "\n***\nSTEP 11 - Distribute V(Bead Mixture) to samples\n***\n")

    vol = float(csvinput[0]['V(Bead Mixture)'])

    volpreairgap = 0.1*vol

    pipette = p20s if (vol + volpreairgap) <= 20 else p300s

    tipcapacity = 20 - volpreairgap if (vol + volpreairgap) <= 20 else 200

    reps = math.ceil(vol / tipcapacity)

    v = vol / reps

    source = beadmixture

    pipette.pick_up_tip()

    for well in [hs_plate.wells_by_name()[name] for name in samplepositions]:

        sideways_offset = well.diameter / 2

        vertical_offset = -5

        # dispense below well top, to western side wall
        disp_loc = well.top(vertical_offset).move(
         types.Point(x=-sideways_offset, y=0, z=0))

        for rep in range(reps):

            pipette.move_to(source.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            # slower flow rate and delay for beads
            pipette.aspirate(v, source.bottom(1), rate=0.5)
            ctx.delay(seconds=0.5)
            pipette.touch_tip(radius=0.75, v_offset=-2, speed=10)

            pipette.move_to(well.top())
            pipette.move_to(well.top(vertical_offset))
            pipette.move_to(disp_loc)
            pipette.dispense(v+volpreairgap, disp_loc, rate=2)
            ctx.delay(seconds=0.5)

    pipette.drop_tip()

    ctx.comment("\n***\nSTEP 12 - 1500 rpm 30 sec\n***\n")

    # start shaking
    hs_mod.set_and_wait_for_shake_speed(rpm=1500)
    ctx.delay(seconds=1)
    ctx.comment(
     "\n***\nHeater-Shaker rpm {}\n***\n".format(hs_mod.current_speed))

    # wait
    ctx.delay(seconds=29)

    # stop shaking
    hs_mod.deactivate_shaker()

    ctx.comment(
     "\n***\nSTEP 13 - Distribute V(ACN calculated) to samples\n***\n")

    vol = v_acn_calculated

    volpreairgap = 0

    volpostairgap = 30

    pipette = p300s

    tipcapacity = 200 - (volpreairgap + volpostairgap)

    reps = math.ceil(vol / tipcapacity)

    v = vol / reps

    source = acn

    mixvol = 0.9*v_binding if 0.9*v_binding <= 200 else 200

    parkingspot = parkingspots()

    for well in [hs_plate.wells_by_name()[name] for name in samplepositions]:

        pipette.pick_up_tip()

        for rep in range(reps):

            source.liq_vol -= v

            ht = liq_height(source) - 3 if liq_height(source) - 3 > 1 else 1

            pipette.move_to(source.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            pipette.aspirate(v, source.bottom(ht))
            if volpostairgap:
                pipette.air_gap(volpostairgap)

            # if it is a first repeat, dispense at top
            if (reps > 1 and not rep):
                pipette.dispense(v+volpreairgap+volpostairgap, well.top())
                ctx.delay(seconds=0.5)
                pipette.blow_out(well.top())
            # otherwise dispense to bottom of well and mix
            else:
                # dispense air at top of well
                if volpreairgap + volpostairgap:
                    pipette.dispense(volpreairgap+volpostairgap, well.top())
                pipette.dispense(v, well.bottom(1))
                pipette.mix(5, mixvol)
                pipette.blow_out(well.top())

        # drop tip in empty rack for later reuse
        pipette.drop_tip(next(parkingspot))

    ctx.comment(
     """\n***\nSTEP 14 - 9 iterations of
     (1500 rpm 30 sec, 1000 rpm 90 sec)\n***\n""")

    for rep in range(9):

        # shake 1500 rpm
        hs_mod.set_and_wait_for_shake_speed(rpm=1500)
        ctx.delay(seconds=1)
        ctx.comment(
         "\n***\nHeater-Shaker rpm {}\n***\n".format(hs_mod.current_speed))

        # wait
        ctx.delay(seconds=29)

        # shake 100 rpm
        hs_mod.set_and_wait_for_shake_speed(rpm=1000)
        ctx.delay(seconds=1)
        ctx.comment(
         "\n***\nHeater-Shaker rpm {}\n***\n".format(hs_mod.current_speed))

        # wait
        ctx.delay(seconds=89)

    # stop shaking
    hs_mod.deactivate_shaker()

    ctx.comment(
     """\n***\nSTEP 15 - relocate plate from heater shaker (slot 3)
     to magnetic module (slot 1)\n***\n""")

    # open latch
    hs_mod.open_labware_latch()
    ctx.comment(" latch status {}".format(hs_mod.labware_latch_status))

    ctx.pause(
     """\n***\nrelocate plate from heater shaker (slot 3)
     to magnetic module (slot 1). Resume\n***\n""")

    # close latch
    hs_mod.close_labware_latch()
    ctx.comment("\n***\nHeater Shaker latch status {}\n***\n".format(
     hs_mod.labware_latch_status))

    ctx.comment("\n***\nSTEP 16 - engage magnets and wait\n***\n")

    mag.engage(height_from_base=engage_height)
    ctx.delay(minutes=1.5)

    ctx.comment(
     "\n***\nSTEP 17 - discard bead pellet supernatants to reservoir\n***\n")

    vol = sum(
     [float(csvinput[0]['V(Sample)']),
      float(csvinput[0]['V(RED first time)']),
      float(csvinput[0]['V(ALK)']),
      float(csvinput[0]['V(RED second time)']),
      float(csvinput[0]['V(Bead Mixture)'])])

    volpreairgap = 20

    volpostairgap = 20

    pipette = p300s

    parkingspot = parkingspots()

    offset_x = 1

    reps = 1 if vol <= 160 else 2

    for well in [mag_plate.wells_by_name()[name] for name in samplepositions]:

        pipette.pick_up_tip(next(parkingspot))

        side = 1 if math.floor(mag_plate.wells().index(well) / 8) % 2 else -1

        for rep in range(reps):

            pipette.move_to(well.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            loc = well.bottom(1).move(
             types.Point(x=side*offset_x, y=0, z=0))
            pipette.aspirate(vol, loc, rate=0.2)
            if volpostairgap:
                pipette.air_gap(volpostairgap)

            pipette.dispense(vol+volpreairgap+volpostairgap,
                             reservoir.wells()[0].top(), rate=2)
            ctx.delay(seconds=0.5)
            pipette.blow_out(reservoir.wells()[0].top())

        # return tip for continued reuse
        pipette.return_tip()

    ctx.comment("\n***\nSTEP 18 - disengage magnets\n***\n")

    mag.disengage()

    for rep in range(2):

        ctx.comment(
         "\n***\nSTEP 19 - distribute 80% EtOH to bead pellets\n***\n")

        vol = 100

        volpostairgap = 30

        pipette = p300s

        source = etoh

        pipette.pick_up_tip()

        for well in [mag_plate.wells_by_name()[
         name] for name in samplepositions]:

            source.liq_vol -= vol

            ht = liq_height(source) - 3 if liq_height(source) - 3 > 1 else 1

            pipette.aspirate(vol, source.bottom(ht))
            pipette.air_gap(volpostairgap)

            pipette.dispense(vol+volpostairgap, well.top())
            ctx.delay(seconds=0.5)
            pipette.blow_out(well.top())

        pipette.drop_tip()

        ctx.comment("\n***\nSTEP 20 - mix\n***\n")

        vol = 95

        pipette = p300s

        parkingspot = parkingspots()

        for well in [mag_plate.wells_by_name()[
         name] for name in samplepositions]:

            pipette.pick_up_tip(next(parkingspot))

            side = 1 if math.floor(
             mag_plate.wells().index(well) / 8) % 2 else -1

            for repeat in range(10):

                offset_x = 2.5 if repeat % 2 else 1

                clearance_mixdispense = 6 if repeat % 2 else 3

                disp_loc = well.bottom(clearance_mixdispense).move(
                 types.Point(x=side*offset_x, y=0, z=0))

                pipette.aspirate(vol, well.bottom(1))
                pipette.dispense(vol, disp_loc, rate=3)

            pipette.mix(5, vol, well.bottom(1))

            # return tip for continued reuse
            pipette.return_tip()

        ctx.comment("\n***\nSTEP 21 - engage magnets and wait\n***\n")

        mag.engage(height_from_base=engage_height)
        ctx.delay(minutes=1.5)

        ctx.comment(
         """\n***\nSTEP 22 - discard bead pellet supernatants
         to reservoir\n***\n""")

        vol = 110

        volpreairgap = 20

        volpostairgap = 20

        pipette = p300s

        parkingspot = parkingspots()

        offset_x = 1

        for well in [mag_plate.wells_by_name()[
         name] for name in samplepositions]:

            pipette.pick_up_tip(next(parkingspot))

            side = -1 if math.floor(
             mag_plate.wells().index(well) / 8) % 2 else 1

            pipette.move_to(well.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            loc = well.bottom(1).move(
             types.Point(x=side*offset_x, y=0, z=0))
            pipette.aspirate(vol, loc, rate=0.2)
            if volpostairgap:
                pipette.air_gap(volpostairgap)

            pipette.dispense(vol+volpreairgap+volpostairgap,
                             reservoir.wells()[0].top(), rate=2)
            ctx.delay(seconds=0.5)
            pipette.blow_out(reservoir.wells()[0].top())

            # return tip for continued reuse
            pipette.return_tip()

        ctx.comment("\n***\nSTEP 23 - disengage magnets\n***\n")

        mag.disengage()

    ctx.comment("\n***\nSTEP 24 - distribute ACN to bead pellets\n***\n")

    vol = 100

    volpostairgap = 30

    pipette = p300s

    source = acn

    pipette.pick_up_tip()

    for well in [mag_plate.wells_by_name()[name] for name in samplepositions]:

        source.liq_vol -= vol

        ht = liq_height(source) - 3 if liq_height(source) - 3 > 1 else 1

        pipette.aspirate(vol, source.bottom(ht))
        pipette.air_gap(volpostairgap)

        pipette.dispense(vol+volpostairgap, well.top())
        ctx.delay(seconds=0.5)
        pipette.blow_out(well.top())

    pipette.drop_tip()

    ctx.comment("\n***\nSTEP 25 - mix\n***\n")

    vol = 95

    pipette = p300s

    parkingspot = parkingspots()

    for well in [mag_plate.wells_by_name()[name] for name in samplepositions]:

        pipette.pick_up_tip(next(parkingspot))

        side = 1 if math.floor(mag_plate.wells().index(well) / 8) % 2 else -1

        for repeat in range(10):

            offset_x = 2.5 if repeat % 2 else 1

            clearance_mixdispense = 6 if repeat % 2 else 3

            disp_loc = well.bottom(clearance_mixdispense).move(
             types.Point(x=side*offset_x, y=0, z=0))

            pipette.aspirate(vol, well.bottom(1))
            pipette.dispense(vol, disp_loc, rate=3)

        pipette.mix(5, vol, well.bottom(1))

        # return tip for continued reuse
        pipette.return_tip()

    ctx.comment("\n***\nSTEP 26 - engage magnets and wait\n***\n")

    mag.engage(height_from_base=engage_height)
    ctx.delay(minutes=1.5)

    ctx.comment(
     "\n***\nSTEP 27 - discard bead pellet supernatants to reservoir\n***\n")

    vol = 110

    volpreairgap = 20

    volpostairgap = 20

    pipette = p300s

    parkingspot = parkingspots()

    offset_x = 1

    for well in [mag_plate.wells_by_name()[name] for name in samplepositions]:

        pipette.pick_up_tip(next(parkingspot))

        side = -1 if math.floor(mag_plate.wells().index(well) / 8) % 2 else 1

        pipette.move_to(well.top())
        if volpreairgap:
            pipette.air_gap(volpreairgap)
        loc = well.bottom(1).move(
         types.Point(x=side*offset_x, y=0, z=0))
        pipette.aspirate(vol, loc, rate=0.2)
        if volpostairgap:
            pipette.air_gap(volpostairgap)

        pipette.dispense(vol+volpreairgap+volpostairgap,
                         reservoir.wells()[0].top(), rate=2)
        ctx.delay(seconds=0.5)
        pipette.blow_out(reservoir.wells()[0].top())

        # return tip for continued reuse
        pipette.drop_tip()

    ctx.comment("\n***\nSTEP 28 - disengage magnets\n***\n")

    mag.disengage()

    ctx.comment("\n***\nSTEP 29 - dispense V(DIG) to samples\n***\n")

    vol = int(csvinput[0]['V(DIG)'])

    volpreairgap = 20

    volpostairgap = 0

    pipette = p300s

    tipcapacity = 200 - (volpreairgap + volpostairgap)

    reps = math.ceil(vol / tipcapacity)

    v = vol / reps

    offset_x = (mag_plate.wells()[0].diameter / 2) - 1  # within 1 mm of side

    source = next(digtube)

    pipette.pick_up_tip()

    for well in [mag_plate.wells_by_name()[name] for name in samplepositions]:

        side = 1 if math.floor(mag_plate.wells().index(well) / 8) % 2 else -1

        disp_loc = well.top(2).move(
         types.Point(x=side*offset_x, y=0, z=0))

        for rep in range(reps):

            source.liq_vol -= v

            if source.liq_vol < 100:

                source = next(digtube)
                source.liq_vol -= v

            ht = liq_height(source) - 3 if liq_height(source) - 3 > 1 else 1

            pipette.move_to(source.top())
            if volpreairgap:
                pipette.air_gap(volpreairgap)
            pipette.aspirate(v, source.bottom(ht))
            pipette.touch_tip(radius=0.75, v_offset=-2, speed=10)

            pipette.dispense(v+volpreairgap, disp_loc, rate=2)
            ctx.delay(seconds=0.5)
            pipette.blow_out(disp_loc)

    pipette.drop_tip()

    ctx.comment(
     """\n***\nSTEP 30 - relocate plate from magnetic module (slot 1)
     to heater shaker (slot 3)\n***\n""")

    # open latch
    hs_mod.open_labware_latch()
    ctx.comment(" latch status {}".format(hs_mod.labware_latch_status))

    ctx.pause(
     """\n***\nrelocate plate from magnetic module (slot 1)
     to heater shaker (slot 3). Resume\n***\n""")

    # close latch
    hs_mod.close_labware_latch()
    ctx.comment("\n***\nHeater Shaker latch status {}\n***\n".format(
     hs_mod.labware_latch_status))

    ctx.comment("""\n***\nSTEP 31 - at 37 degrees C
    (1500 rpm 2 min, 1000 rpm until user input)\n***\n""")

    # set temperature and wait
    ctx.comment(
     "\n***\nHeater Shaker current temperature {}\n***\n".format(
      hs_mod.current_temperature))
    hs_mod.set_target_temperature(celsius=37)
    hs_mod.wait_for_temperature()
    ctx.comment(
     "\n***\nHeater Shaker current temperature {}\n***\n".format(
      hs_mod.current_temperature))

    hs_mod.set_and_wait_for_shake_speed(rpm=1500)
    ctx.delay(seconds=1)
    ctx.comment("\n***\nHeater-Shaker rpm {}\n***\n".format(
     hs_mod.current_speed))

    ctx.delay(seconds=119)

    hs_mod.set_and_wait_for_shake_speed(rpm=1000)
    ctx.delay(seconds=1)
    ctx.comment("\n***\nHeater-Shaker rpm {}\n***\n".format(
     hs_mod.current_speed))

    ctx.comment("""\n***\nSTEP 32 - stop heating and shaking
    when robot user clicks resume\n***\n""")

    # pause - to continue heat and shake until user input (resume)
    ctx.pause("\n***\nClick resume to stop heating and shaking\n***\n")

    # stop heating and shaking
    hs_mod.deactivate_shaker()
    hs_mod.deactivate_heater()

    ctx.comment("""\n***\nSTEP 33 - relocate plate from heater shaker (slot 3)
    to magnetic module (slot 1)\n***\n""")

    # open latch
    hs_mod.open_labware_latch()
    ctx.comment(" latch status {}".format(hs_mod.labware_latch_status))

    ctx.pause("""\n***\nrelocate plate from heater shaker (slot 3)
    to magnetic module (slot 1). Resume\n***\n""")

    # close latch
    hs_mod.close_labware_latch()
    ctx.comment("\n***\nHeater Shaker latch status {}\n***\n".format(
     hs_mod.labware_latch_status))

    ctx.comment("\n***\nSTEP 34 - engage magnets and wait\n***\n")

    mag.engage(height_from_base=engage_height)
    ctx.delay(minutes=5)

    ctx.comment("""\n***\nSTEP 35 - transfer bead pellet supernatants
    to final plate (slot 9)\n***\n""")

    vol = int(csvinput[0]['V(DIG)'])

    pipette = p300s

    offset_x = 1.5

    for well in [mag_plate.wells_by_name()[name] for name in samplepositions]:

        pipette.pick_up_tip()

        side = -1 if math.floor(mag_plate.wells().index(well) / 8) % 2 else 1

        asp_loc = well.bottom(1.5).move(
         types.Point(x=side*offset_x, y=0, z=0))

        pipette.aspirate(vol, asp_loc, rate=0.15)
        ctx.delay(seconds=0.5)

        pipette.dispense(
         vol, final_plate.wells()[mag_plate.wells().index(well)].bottom(1))

        pipette.drop_tip()

    ctx.comment(
     '''Process Complete.''')
