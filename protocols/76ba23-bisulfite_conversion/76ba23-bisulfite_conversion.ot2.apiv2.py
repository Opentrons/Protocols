metadata = {
    'protocolName': 'Bisulfite Conversion',
    'author': 'Steve <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    ctx.set_rail_lights(True)

    [choose_tip_rack] = get_values(  # noqa: F821
        "choose_tip_rack")

    # tips (max volume 200 ul if filter tips, otherwise 300 ul)
    tips300 = [ctx.load_labware(choose_tip_rack, str(slot)) for slot in [6, 9]]
    tip_max = tips300[0].wells_by_name()['A1'].max_volume

    # p300 multi
    p300m = ctx.load_instrument(
        "p300_multi_gen2", 'right', tip_racks=tips300)

    # magnetic module in slot 4 with deep well plate
    mag = ctx.load_module('magnetic module gen2', '4')
    mag.disengage()
    mag_plate = mag.load_labware('usascientific_96_wellplate_2.4ml_deep')
    mag_height = {
        'omni_96_wellplate_2000ul': 8.5,
        'nest_96_wellplate_2ml_deep': 8.5,
        'usascientific_96_wellplate_2.4ml_deep': 8.5
        }

    # cf DNA (slot 1), CT rxn plate (slot 2), eluate (slot 10)
    [cf_dna, pcr_plate, barcoded_pcr_plate] = [
     ctx.load_labware(labware, slot) for labware, slot in zip(
        ["nest_96_wellplate_100ul_pcr_full_skirt",
         "biorad_96_wellplate_200ul_pcr",
         "nest_96_wellplate_100ul_pcr_full_skirt"],
        [str(num) for num in [1, 2, 10]])]

    # reagent trough (slot 3): CT conv buffer (A1), beads (A2), water (A3)
    trough = ctx.load_labware("nest_12_reservoir_15ml", '3')
    ct_conv, beads_mm, water = [
     trough.wells_by_name()[well_name] for well_name in ['A1', 'A2', 'A3']]

    # reservoirs for wash, desulph, waste in slots 5, 8, 11
    [wash_reservoir, desulph_reservoir,
     waste_reservoir] = [
     ctx.load_labware(labware, slot) for labware, slot in zip(
      ["nest_1_reservoir_195ml", "nest_1_reservoir_195ml",
       "agilent_1_reservoir_290ml"],
      [str(num) for num in [5, 8, 11]])]
    wash, desulph, waste = [labware.wells()[0] for labware in [
     wash_reservoir, desulph_reservoir, waste_reservoir]]

    # helper function for repeat large vol transfers
    def rep_max_transfer(remaining, source, dest, tip_max_vol=tip_max, air=0):
        vol = tip_max_vol - air
        while remaining > vol:
            p300m.aspirate(vol, source)
            if air > 0:
                p300m.air_gap(air)
            p300m.dispense(tip_max_vol, dest)
            remaining -= vol
        p300m.aspirate(remaining, source)
        if air > 0:
            p300m.air_gap(air)
        p300m.dispense(remaining + air, dest)

    # helper function to reuse tips
    def reuse_tips(which_tips):
        p300m.reset_tipracks()
        p300m.starting_tip = which_tips

    # cf DNA + CT conversion buffer to PCR plate
    sample_tips = tips300[0].next_tip()

    p300m.distribute(130, ct_conv, [
     column[0] for column in pcr_plate.columns()], disposal_volume=0)

    p300m.transfer(20, [column[0] for column in cf_dna.columns()], [
     column[0] for column in pcr_plate.columns()],
     mix_after=(4, 75), new_tip='always')

    ctx.set_rail_lights(False)
    ctx.pause("""Paused for thermocycling step. When cycling is finished,
                 please return the pcr plate to its deck slot, replenish
                 the used tips in the tipboxes on the OT-2 deck,
                 then click resume.""")
    ctx.set_rail_lights(True)

    # bead-buffer mix and cycler product to collect plate (on magnetic module)
    reuse_tips(sample_tips)
    for index, column in enumerate(pcr_plate.columns()):
        p300m.pick_up_tip()
        p300m.mix(10, tip_max, beads_mm)
        rep_max_transfer(610, beads_mm, mag_plate.columns()[index][0].top())
        p300m.transfer(150, column[0], mag_plate.columns()[
         index][0].top(), mix_after=(5, tip_max), new_tip='never')
        p300m.return_tip()
    wash_tips = tips300[1].next_tip()

    mag.engage(height=mag_height['usascientific_96_wellplate_2.4ml_deep'])
    ctx.delay(minutes=7)

    # remove supernatant
    reuse_tips(sample_tips)
    for column in mag_plate.columns():
        p300m.pick_up_tip()
        rep_max_transfer(760, column[0], waste)
        p300m.return_tip()

    mag.disengage()

    for rep in range(3):
        # add wash (contains ethanol)
        reuse_tips(wash_tips)
        p300m.pick_up_tip()
        for column in mag_plate.columns():
            rep_max_transfer(400, wash, column[0], air=1)
        p300m.return_tip()
        desulph_tips = tips300[1].next_tip()

        # mix
        reuse_tips(sample_tips)
        for column in mag_plate.columns():
            p300m.pick_up_tip()
            p300m.mix(4, 200, column[0])
            p300m.return_tip()

        mag.engage(height=mag_height['usascientific_96_wellplate_2.4ml_deep'])
        ctx.delay(minutes=7)

        # remove sup
        reuse_tips(sample_tips)
        for column in mag_plate.columns():
            p300m.pick_up_tip()
            rep_max_transfer(400, column[0], waste, air=40)
            p300m.return_tip()

        mag.disengage()

        if rep == 0:
            # add desulphonation buffer
            reuse_tips(desulph_tips)
            p300m.pick_up_tip()
            for column in mag_plate.columns():
                rep_max_transfer(200, desulph, column[0])
            p300m.return_tip()
            water_tips = tips300[1].next_tip()

            # mix
            reuse_tips(sample_tips)
            for column in mag_plate.columns():
                p300m.pick_up_tip()
                p300m.mix(4, 100, column[0])
                p300m.return_tip()

            ctx.delay(minutes=11)

            mag.engage(
             height=mag_height['usascientific_96_wellplate_2.4ml_deep'])
            ctx.delay(minutes=7)

            # remove sup
            reuse_tips(sample_tips)
            for column in mag_plate.columns():
                p300m.pick_up_tip()
                rep_max_transfer(200, column[0], waste)
                p300m.return_tip()

            mag.disengage()

    ctx.pause("""Please dry the magnetic module plate for 20 min at 55 C.
                 Then return the plate to the magnetic module
                 and click resume.""")

    reuse_tips(water_tips)
    p300m.distribute(25, water, [
     column[0].top() for column in mag_plate.columns()], trash=False)

    ctx.pause("""Please incubate the magnetic module plate for 4 min at 55 C
                 to elute. Then place it back on the magnetic module. Please
                 replace the used tip boxes with fresh tips to transfer the
                 eluate.""")

    mag.engage(height=mag_height['usascientific_96_wellplate_2.4ml_deep'])
    ctx.delay(minutes=5)

    # transfer eluate to barcoded, labeled PCR plate
    p300m.reset_tipracks()
    p300m.transfer(25, [column[0] for column in mag_plate.columns()], [
     column[0] for column in barcoded_pcr_plate.columns()], new_tip='always')
