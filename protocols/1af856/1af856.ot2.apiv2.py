import math
from opentrons import types

metadata = {
    'protocolName': '''Lexogen QuantSeq-Pool Sample-Barcoded 3-Prime
    mRNA-Seq Library Prep Kit for Illumina''',
    'author': 'Steve Plonk <protocols@opentrons.com>',
    'apiLevel': '2.11'
}


def run(ctx):

    # get values from json above
    [count_samples, time_dry, time_engage,
     offset_x] = get_values(  # noqa: F821
      'count_samples', 'time_dry', 'time_engage', 'offset_x')

    ctx.set_rail_lights(True)

    if not 8 <= count_samples <= 96:
        raise Exception('Invalid sample count (must be 8-96).')

    # helper functions

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

    # 20 and 200 uL filter tips, p20 single, p300 single

    tips20 = [ctx.load_labware(
     "opentrons_96_filtertiprack_20ul", str(slot)) for slot in [10, 11]]

    p20s = ctx.load_instrument(
        "p20_single_gen2", 'left', tip_racks=tips20)

    tips300 = [
     ctx.load_labware(
      "opentrons_96_filtertiprack_200ul", str(slot)) for slot in [6, 9]]

    p300s = ctx.load_instrument(
        "p300_single_gen2", 'right', tip_racks=tips300)

    # tube rack for PS, EB, PB, empty tubes for RT mastermix, PCR mastermix
    tuberack = ctx.load_labware(
     'opentrons_24_tuberack_nest_1.5ml_snapcap', '2',
     'Tube Rack for PS, EB, PB')
    ps, eb, pb, mastermix, pcr_mastermix = [
     tuberack.wells_by_name()[name] for name in ['A1', 'A2', 'A3', 'A4', 'A5']]
    num_purifications = 2 if count_samples > 56 else 1
    pb.liq_vol = 1.1*(num_purifications*24 + 7 + 31.5)
    ps.liq_vol = 1.1*(13.5*count_samples - 24 + 52 + 30)
    eb.liq_vol = 1.1*(12 + 40 + 20 + 30 + 20)

    # reservoir for 80 percent ethanol
    etoh = ctx.load_labware(
     'nest_12_reservoir_15ml', '3', '80 Percent Ethanol').wells()[0]
    deadvol_res = 10000
    etoh.liq_vol = 2*23*count_samples + 2*(2*120) + deadvol_res

    # magnetic module
    mag = ctx.load_module('magnetic module gen2', '4')
    mag.disengage()
    mag_plate = mag.load_labware(
     'nest_96_wellplate_2ml_deep', 'Magnetic Module Plate')

    # Nest PCR plate in slot 5
    pcr_plate = ctx.load_labware(
     'nest_96_wellplate_100ul_pcr_full_skirt', '5',
     'Nest 100 uL PCR plate in slot 5')

    # final output plate in slot 1
    output_plate = ctx.load_labware(
     'nest_96_wellplate_100ul_pcr_full_skirt', '1',
     'Final Output plate in slot 1')

    # temperature module for FS, E1, DTT, RS, RPM, E2, PM, P5, P7, PE
    temp = ctx.load_module('Temperature Module', '7')
    block = temp.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap')
    [fs, e1, dtt, rs, rpm, e2, pm, p5, p7, pe] = [
     block.wells_by_name()[name] for name in [
      'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4']]
    deadvol_tube = 3
    temp.set_temperature(4)
    fs.liq_vol = 1.1*(2.5*count_samples) + deadvol_tube
    e1.liq_vol = 0.25*count_samples + deadvol_tube
    dtt.liq_vol = 0.25*count_samples + deadvol_tube
    rs.liq_vol = 2 + deadvol_tube
    rpm.liq_vol = 6.5 + deadvol_tube
    e2.liq_vol = 1 + deadvol_tube
    pm.liq_vol = 7 + deadvol_tube
    p5.liq_vol = 5 + deadvol_tube
    p7.liq_vol = 5 + deadvol_tube
    pe.liq_vol = 1 + deadvol_tube

    # alert user to reagent volumes needed
    ctx.comment("Ensure reagents in sufficient volume are present on deck.")
    for volume, units, reagent, location in zip(
     [math.ceil(rgnt.liq_vol) if rgnt.liq_vol < 1500 else math.ceil(
      rgnt.liq_vol / 1000) for rgnt in [
      fs, e1, dtt, pb, ps, eb, rs, rpm, e2, pm, p5, p7, pe, etoh]],
     ['uL', 'uL', 'uL', 'uL', 'uL', 'uL', 'uL', 'uL', 'uL', 'uL',
      'uL', 'uL', 'uL', 'mL'],
     ['FS', 'E1', 'DTT', 'PB', 'PS', 'EB', 'RS', 'RPM', 'E2',
      'PM', 'P5', 'P7', 'PE', 'EtOH'],
     [fs, e1, dtt, pb, ps, eb, rs, rpm, e2, pm, p5, p7, pe, etoh]):
        ctx.comment(
         "{0} {1} {2} in {3}".format(
          str(volume), units, reagent.upper(), location))

    # index plate
    index_plate = ctx.load_labware(
     'index_96_aluminumblock_200ul', '8', 'Index Plate')

    ctx.comment("\nSTEP - please confirm and resume\n")

    ctx.pause("""\n
Add 10-120 ng total RNA (7 uL) to dried-in sample-barcode RT primer in {}\n\n
Mix well to dissolve primer\n\n
Then 3 minutes at 85 degrees C (thermocycler)\n\n
Cool to 25 degrees C\n\n
Spin to collect liquid at well bottom.\n\n
Return plate to slot 8. Resume\n\n
\n""".format(index_plate.wells()[:count_samples]))

    # is this reagent assembly using the automation well?
    ctx.comment(
     "\nSTEP - assemble mastermix\n")

    total = 0

    for vol, reagent in zip([2.5, 0.25, 0.25], [fs, dtt, e1]):
        v = 1.05*vol*count_samples
        pip = p20s if v <= 20 else p300s
        pip.transfer(v, reagent, mastermix)
        total += v

    p300s.pick_up_tip()
    mx_vol = 0.8*total if 0.8*total <= 200 else 200
    p300s.mix(5, mx_vol, mastermix)
    p300s.drop_tip()

    ctx.comment("\nSTEP - add 3 uL mastermix to each RT reaction\n")

    for well in index_plate.wells()[:count_samples]:
        p20s.transfer(3, mastermix, well, new_tip='always')

    ctx.pause("""\n
Seal the plate\n\n
Gently vortex to mix\n\n
Spin\n\n
Incubate 42 degrees C 15 min\n\n
Spin\n\n
Return plate to slot 8. Resume\n\n
\n""")

    ctx.comment("\nSTEP - combine 9 uL each of up to 56 RT reactions\n")

    purifications = [
     mag_plate.wells_by_name()[name] for name in [
      'A1', 'A2']][:num_purifications]

    counts = [math.ceil(count_samples / num_purifications)]
    if num_purifications > 1:
        new = count_samples - counts[0]
        counts.append(new)

    p20s.pick_up_tip()

    for index, well in enumerate(index_plate.wells()[:count_samples]):

        dest = purifications[math.floor(index / counts[0])]

        p20s.transfer(9, well, dest, new_tip='never')

    p20s.drop_tip()

    ctx.comment("\nSTEP - add 24 uL beads to each purification\n")

    for purification in purifications:
        p300s.transfer(
         24, pb, purification, mix_before=(5, 0.8*24*num_purifications),
         new_tip='always')

    ctx.comment("\nSTEP - add PS for final vol 22.5 uL per sample and mix\n")

    for purification, count in zip(purifications, counts):

        vol = 13.5*count - 24

        reps = math.ceil(vol / 200)

        v = vol / reps

        for rep in range(reps):

            p300s.pick_up_tip()

            p300s.aspirate(v, ps)

            p300s.dispense(v, purification)

            if rep == reps - 1:

                mx_vol = 0.8*(22.5*count) if 0.8*(22.5*count) <= 200 else 200

                p300s.mix(5, mx_vol, purification)

            p300s.drop_tip()

    ctx.comment("\nSTEP - incubate 5 min room temp\n")

    ctx.delay(minutes=5)

    ctx.comment("\nSTEP - engage magnets for 10 min\n")

    mag.engage()
    ctx.delay(minutes=10)

    ctx.comment("STEP - processing purifications")

    for index, purification, count in zip(
     [0, 1][:num_purifications], purifications, counts):

        vol = 22.5*count

        reps = math.ceil(vol / (tips300[0].wells()[0].max_volume - 40))

        v = vol / reps

        ctx.comment("\nSTEP - processing purifications: remove initial sup\n")

        p300s.pick_up_tip()

        for rep in range(reps):

            ht = 4 if rep < reps - 1 else 1

            asp_loc = purification.bottom(ht).move(types.Point(
             x={True: -1}.get(not index % 2, 1)*offset_x, y=0, z=0))

            # pre air gap
            p300s.move_to(purification.top())
            p300s.air_gap(20)

            # aspirate at 4 mm until last rep at 1 mm avoiding bead pellet
            p300s.aspirate(v, asp_loc, rate=0.2)
            p300s.air_gap(20)

            # dispense to trash with delayed blowout
            p300s.dispense(v+40, ctx.fixed_trash.wells()[0].top(-5), rate=2)
            ctx.delay(seconds=1)
            p300s.blow_out()

        p300s.drop_tip()

        ctx.comment("\nSTEP - purifications: wash 2x with 80 pct EtOH\n")

        for repeat in range(2):

            p300s.pick_up_tip()

            vol = 23*count

            reps = math.ceil(vol / (tips300[0].wells()[0].max_volume - 20))

            v = vol / reps

            ctx.comment("\nSTEP - purifications: add 80 pct ethanol\n")

            for rep in range(reps):

                etoh.liq_vol -= v

                ht = liq_height(etoh) - 3 if liq_height(etoh) - 3 > 1 else 1

                if p300s.current_volume:
                    p300s.dispense(p300s.current_volume, etoh.top())
                p300s.aspirate(v, etoh.bottom(ht))
                p300s.air_gap(20)

                p300s.dispense(v+20, purification.top())
                ctx.delay(seconds=1)
                p300s.blow_out()
                p300s.air_gap(20)

            ctx.delay(seconds=30)

            vol = 25*count

            reps = reps = math.ceil(
             vol / (tips300[0].wells()[0].max_volume - 40))

            v = vol / reps

            ctx.comment("\nSTEP - purifications: remove and discard EtOH\n")

            for rep in range(reps):

                ht = 4 if rep < reps - 1 else 1

                asp_loc = purification.bottom(ht).move(types.Point(
                 x={True: -1}.get(not index % 2, 1)*offset_x, y=0, z=0))

                # pre air gap
                if p300s.current_volume:
                    p300s.dispense(p300s.current_volume, purification)
                p300s.move_to(purification.top())
                p300s.air_gap(20)

                # aspirate at 4 mm until last rep at 1 mm avoiding bead pellet
                p300s.aspirate(v, asp_loc, rate=0.2)
                p300s.air_gap(20)

                # dispense to trash with delayed blowout
                p300s.dispense(
                 v+40, ctx.fixed_trash.wells()[0].top(-5), rate=2)
                ctx.delay(seconds=1)
                p300s.blow_out()

            # to improve completeness of removal
            for clearance in [0.7, 0.4, 0.2, 0]:
                loc = purification.bottom(clearance).move(types.Point(
                 x={True: -1}.get(not index % 2, 1)*offset_x, y=0, z=0))
                p300s.aspirate(25, loc)

            p300s.drop_tip()

        ctx.comment("\nSTEP - purifications: air dry bead pellet\n")

        ctx.delay(minutes=time_dry)

        ctx.comment("\nSTEP - purifications: elute purification 1\n")

        mag.disengage()

        if not index:

            asp_loc = eb

            disp_loc = purification.bottom(1).move(types.Point(x={True: 1}.get(
             not index % 2, -1)*offset_x, y=0, z=0))

        else:

            ctx.comment("\nSTEP - purifications: elute purification 2\n")

            asp_loc = purifications[0].bottom(1).move(types.Point(
             x=-1*offset_x, y=0, z=0))

            disp_loc = purifications[1].bottom(1).move(types.Point(
             x={True: 1}.get(not index % 2, -1)*offset_x, y=0, z=0))

        p20s.transfer(12, asp_loc, disp_loc, mix_after=(5, 9))

        ctx.delay(minutes=2)

        mag.engage()
        ctx.delay(minutes=time_engage)

    ctx.comment("\nSTEP - recover final purification eluate\n")

    asp_loc = purifications[-1].bottom(1).move(types.Point(
     x={True: 1}.get(num_purifications > 1, -1)*offset_x, y=0, z=0))

    p20s.transfer(10.5, asp_loc, pcr_plate.wells_by_name()['A1'])

    ctx.comment("\nSTEP - treat with RNA removal solution\n")

    p20s.transfer(2, rs, pcr_plate.wells_by_name()['A1'], mix_after=(5, 10))

    ctx.pause("""\n
Seal the plate\n\n
Spin\n\n
Incubate 95 degrees C 10 min\n\n
Spin\n\n
Unseal and return plate to slot 5. Resume\n\n
\n""")

    ctx.comment("\nSTEP - add Random Priming Mix\n")

    p20s.transfer(6.5, rpm, pcr_plate.wells_by_name()['A1'], mix_after=(5, 15))

    ctx.pause("""\n
Seal the plate\n\n
Spin\n\n
Incubate 98 degrees C 2 min\n\n
Cool to 25 degrees C at reduced 0.5 deg/sec\n\n
Incubate 25 degrees C 3 min\n\n
Spin\n\n
Unseal and return plate to slot 5. Resume\n\n
\n""")

    ctx.comment("\nSTEP - add E2\n")

    p20s.transfer(1, e2, pcr_plate.wells_by_name()['A1'], mix_after=(5, 15))

    ctx.pause("""\n
Seal the plate\n\n
Spin\n\n
Incubate 30 degrees C 30 min\n\n
Spin\n\n
Unseal and return plate to slot 5. Resume\n\n
\n""")

    ctx.comment("\nSTEP - transfer pool to mag plate\n")

    p20s.transfer(
     20, pcr_plate.wells_by_name()['A1'], mag_plate.wells_by_name()['A3'])

    ctx.comment("\nSTEP - add 7 uL beads, wait, engage magnets, wait\n")

    p20s.transfer(7, pb, mag_plate.wells_by_name()['A3'], mix_before=(5, 7))

    ctx.delay(minutes=5)

    mag.engage()
    ctx.delay(minutes=time_engage)

    ctx.comment("\nSTEP - remove sup\n")

    p300s.pick_up_tip()

    asp_loc = mag_plate.wells_by_name()['A3'].bottom(1).move(types.Point(
     x=-1*offset_x, y=0, z=0))

    p300s.aspirate(30, asp_loc, rate=0.2)
    p300s.air_gap(20)

    p300s.drop_tip()

    ctx.comment("\nSTEP - elute\n")

    disp_loc = mag_plate.wells_by_name()['A3'].bottom(1).move(types.Point(
     x=1*offset_x, y=0, z=0))

    mag.disengage()

    p300s.transfer(40, eb, disp_loc, mix_after=(5, 32))

    ctx.delay(minutes=2)

    ctx.comment("\nSTEP - add PS\n")

    p300s.transfer(52, ps, mag_plate.wells_by_name()['A3'], mix_after=(5, 74))

    ctx.delay(minutes=5)

    mag.engage()
    ctx.delay(minutes=time_engage)

    ctx.comment("\nSTEP - remove sup\n")

    p300s.pick_up_tip()

    asp_loc = mag_plate.wells_by_name()['A3'].bottom(1).move(types.Point(
     x=-1*offset_x, y=0, z=0))

    p300s.aspirate(100, asp_loc, rate=0.2)
    p300s.air_gap(20)

    p300s.drop_tip()

    for rep in range(2):

        ctx.comment("\nSTEP - add 80 percent EtOH\n")

        p300s.pick_up_tip()

        etoh.liq_vol -= 120

        ht = liq_height(etoh) - 3 if liq_height(etoh) - 3 > 1 else 1

        p300s.aspirate(120, etoh.bottom(ht))
        p300s.air_gap(20)

        p300s.dispense(140, mag_plate.wells_by_name()['A3'].top())
        ctx.delay(seconds=1)
        p300s.blow_out()

        ctx.delay(seconds=30)

        ctx.comment("\nSTEP - remove sup\n")

        asp2_loc = mag_plate.wells_by_name()['A3'].bottom(1).move(types.Point(
         x=-1*offset_x, y=0, z=0))

        p300s.move_to(mag_plate.wells_by_name()['A3'].top())
        p300s.air_gap(20)
        p300s.aspirate(
         100, mag_plate.wells_by_name()['A3'].bottom(4), rate=0.2)
        p300s.aspirate(60, asp2_loc, rate=0.2)
        p300s.air_gap(20)

        if not rep:
            p300s.drop_tip()
        else:
            p300s.dispense(200, ctx.fixed_trash.wells()[0].top(-5), rate=2)
            ctx.delay(seconds=1)
            p300s.blow_out()

    # to improve completeness of removal
    for clearance in [0.7, 0.4, 0.2, 0]:
        loc = mag_plate.wells_by_name()['A3'].bottom(clearance).move(
         types.Point(x=-1*offset_x, y=0, z=0))
        p300s.aspirate(25, loc)

    p300s.drop_tip()

    ctx.comment("\nSTEP - dry beads\n")

    ctx.delay(minutes=time_dry)

    ctx.comment("\nSTEP - elute and engage magnets\n")

    disp_loc = mag_plate.wells_by_name()['A3'].bottom(1).move(
     types.Point(x=1*offset_x, y=0, z=0))

    mag.disengage()

    p300s.transfer(20, eb, disp_loc, mix_after=(5, 16))

    ctx.delay(minutes=2)

    mag.engage()
    ctx.delay(minutes=time_engage)

    ctx.comment("\nSTEP - recover eluate\n")

    asp_loc = mag_plate.wells_by_name()['A3'].bottom(1).move(
     types.Point(x=1*offset_x, y=0, z=0))

    p20s.transfer(17, asp_loc, pcr_plate.wells_by_name()['A2'])

    ctx.comment("\nSTEP - assemble PCR mastermix\n")

    for vol, reagent in zip([7, 5, 5, 1], [pm, p5, p7, pe]):
        p20s.transfer(vol, reagent, pcr_mastermix, new_tip='always')

    ctx.comment("\nSTEP - add PCR mastermix\n")

    p20s.transfer(
     18, pcr_mastermix.bottom(0.5), pcr_plate.wells_by_name()['A2'])

    ctx.pause(
     "Pausing for PCR. When finished, return plate to slot 5. Resume.")

    ctx.comment("\nSTEP - transfer PCR reaction to mag plate\n")

    p300s.transfer(
     35, pcr_plate.wells_by_name()['A2'], mag_plate.wells_by_name()['A4'])

    ctx.comment("\nSTEP - add beads\n")

    p300s.transfer(
     31.5, pb, mag_plate.wells_by_name()['A4'],
     mix_before=(10, 24), mix_after=(5, 50))

    ctx.delay(minutes=5)

    mag.engage()
    ctx.delay(time_engage)

    ctx.comment("\nSTEP - remove sup\n")

    p300s.pick_up_tip()

    asp_loc = mag_plate.wells_by_name()['A4'].bottom(1).move(
     types.Point(x=1*offset_x, y=0, z=0))

    p300s.aspirate(70, asp_loc, rate=0.2)
    p300s.air_gap(20)

    p300s.drop_tip()

    ctx.comment("\nSTEP - elute, add ps, enage magnets\n")

    disp_loc = mag_plate.wells_by_name()['A4'].bottom(1).move(
     types.Point(x=-1*offset_x, y=0, z=0))

    mag.disengage()

    p300s.transfer(30, eb, disp_loc, mix_after=(5, 24))

    ctx.delay(minutes=2)

    p300s.transfer(30, ps, disp_loc, mix_after=(5, 48))

    ctx.delay(minutes=5)

    mag.engage()
    ctx.delay(minutes=time_engage)

    ctx.comment("\nSTEP - remove sup\n")

    asp_loc = mag_plate.wells_by_name()['A4'].bottom(1).move(
     types.Point(x=1*offset_x, y=0, z=0))

    p300s.pick_up_tip()

    p300s.aspirate(70, asp_loc, rate=0.2)
    p300s.air_gap(20)

    p300s.drop_tip()

    for rep in range(2):

        ctx.comment("\nSTEP - add 80 percent EtOH\n")

        p300s.pick_up_tip()

        etoh.liq_vol -= 120

        ht = liq_height(etoh) - 3 if liq_height(etoh) - 3 > 1 else 1

        p300s.aspirate(120, etoh.bottom(ht))
        p300s.air_gap(20)

        p300s.dispense(140, mag_plate.wells_by_name()['A4'].top())
        ctx.delay(seconds=1)
        p300s.blow_out()

        ctx.delay(seconds=30)

        ctx.comment("\nSTEP - remove sup\n")

        asp2_loc = mag_plate.wells_by_name()['A4'].bottom(1).move(
         types.Point(x=-1*offset_x, y=0, z=0))

        p300s.move_to(mag_plate.wells_by_name()['A4'].top())
        p300s.air_gap(20)
        p300s.aspirate(
         100, mag_plate.wells_by_name()['A4'].bottom(4), rate=0.2)
        p300s.aspirate(60, asp2_loc, rate=0.2)
        p300s.air_gap(20)

        if not rep:
            p300s.drop_tip()
        else:
            p300s.dispense(200, ctx.fixed_trash.wells()[0].top(-5), rate=2)
            ctx.delay(seconds=1)
            p300s.blow_out()

    # to improve completeness of removal
    for clearance in [0.7, 0.4, 0.2, 0]:
        loc = mag_plate.wells_by_name()['A4'].bottom(clearance).move(
         types.Point(x=1*offset_x, y=0, z=0))
        p300s.aspirate(25, loc)

    p300s.drop_tip()

    ctx.comment("\nSTEP - dry beads\n")

    ctx.delay(minutes=time_dry)

    ctx.comment("\nSTEP - elute and engage magnets\n")

    disp_loc = mag_plate.wells_by_name()['A4'].bottom(1).move(
     types.Point(x=-1*offset_x, y=0, z=0))

    mag.disengage()

    p300s.transfer(20, eb, disp_loc, mix_after=(5, 16))

    ctx.delay(minutes=2)

    mag.engage()
    ctx.delay(minutes=time_engage)

    ctx.comment("\nSTEP - recover eluate\n")

    asp_loc = mag_plate.wells_by_name()['A4'].bottom(1).move(
     types.Point(x=1*offset_x, y=0, z=0))

    p20s.transfer(17, asp_loc, output_plate.wells_by_name()['A1'])

    ctx.comment(
     """\nProcess complete\n""")
