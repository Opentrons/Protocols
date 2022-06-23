from opentrons import protocol_api
from typing import List
from opentrons.protocol_api.labware import Well

metadata = {
    'protocolName': '',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "p20_mount":"left"
                                  }
                                  """)  # noqa: E501 Do not report 'line too long' warnings
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [p20_mount,
     p20_mount] = get_values(  # noqa: F821
     "p20_mount")

    p300_mount = 'right' if p20_mount == 'left' else 'left'

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    tc_mod = ctx.load_module('thermocycler module')
    mag_mod = ctx.load_module('magnetic module gen2', '4')
    temp_mod = ctx.load_module('temperature module gen2', '1')

    # load labware

    resv = ctx.load_labware('nest_12_reservoir_15ml', '11')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_200ul_flat')
    mag_plate = mag_mod.load_labware('nest_96_wellplate_200ul_flat')
    tmod_tubes = temp_mod.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap')

    # load tipracks

    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '2')]
    tiprack200s = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', '5', '8')]

    # load instrument

    p20 = ctx.load_instrument(
                              'p20_single_gen2',
                              p20_mount,
                              tip_racks=tiprack20
                              )

    p300 = ctx.load_instrument(
                              'p300_multi_gen2',
                              p300_mount,
                              tip_racks=tiprack200s
                              )

    # pipette functions   # INCLUDE ANY BINDING TO CLASS
    def pick_up(pipette):
        """`pick_up()` will pause the protocol when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the protocol will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.

        :param pipette: The pipette desired to pick up tip
        as definited earlier in the protocol (e.g. p300, m20).
        """
        try:
            pipette.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            pipette.pick_up_tip()

    # helper functions
    def bead_cleanup(
            mix_vol: float,
            bead_vol: float,
            dna_vol: float,
            DNA_col: List[Well],
            dna_air_gap_vol: float,
            supernatant_vol: float,
            resusp_water_vol: float,
            water_column: List[Well],
            purified_DNA_vol: float,
            target_col: List[Well]):

        nonlocal p300, ctx, mag_beads, mag_target_col, mag_mod, waste_well
        nonlocal ethanol_well
        # 1. Use 8-channel P300 to mix Reservoir Well 1
        # (Ampure Beads - High Viscosity).
        pick_up(p300)
        p300.mix(10, mix_vol, mag_beads)
        # 2. Transfer <bead_vol> uL of Reservoir Well 1 to
        # Magnet Wells Column 1 A-H.
        p300.aspirate(bead_vol, mag_beads[0], rate=0.3)
        p300.dispense(bead_vol, mag_target_col[0], rate=0.3)
        # Solution is viscous, try to get it all out
        p300.touch_tip()
        p300.blow_out()
        # 3. Transfer <dna_vol> uL of Thermocycler Column 1 A-H to
        # Magnet Wells Column <n> A-H.
        p300.aspirate(dna_vol, DNA_col[0])
        p300.air_gap(dna_air_gap_vol)
        p300.dispense(dna_vol+dna_air_gap_vol, mag_target_col[0])
        # 4. Mix Magnet Wells Column 1 A-H at 1 minute intervals for 10 minutes
        # Total volume in the mag column: bead_vol + dna_vol
        mix_vol = bead_vol + dna_vol - 20
        if mix_vol < 0:
            raise Exception(
                "The mixing vol for step 4. in the bead cleanup function "
                f" is less than 0 uL ({mix_vol})")
        mix_vol = mix_vol if mix_vol < 200 else 200
        for i in range(10):
            p300.mix(10, mix_vol, mag_target_col[0], rate=1)
            ctx.delay(minutes=1)
        p300.touch_tip()
        p300.blow_out()
        # 5. Engage magnet.
        mag_mod.engage()
        # 6. Hold for 5 minutes
        ctx.delay(minutes=5)
        # 7. remove <supernatant_vol> from Magnet Wells Column 1 A-H.
        # TODO: Look into what side of the well the magnetic pellet is loctd.
        # and aspirate from the other side.
        p300.aspirate(supernatant_vol, mag_target_col[0], rate=0.2)
        supernatant_air_gap_vol = 10 if supernatant_vol < 190 \
            else 200 - supernatant_vol
        if supernatant_air_gap_vol > 0:
            p300.air_gap(supernatant_air_gap_vol)
        p300.dispense(
            supernatant_vol+supernatant_air_gap_vol, waste_well.top())
        p300.blow_out()
        # 8. Discard tips.
        p300.drop_tip()
        # 9. Use 8-channel P300 to mix Reservoir Well 5
        # (80% EtOH -low viscosity)
        pick_up(p300)
        p300.mix(10, 200, ethanol_well)
        # 10. Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 1 A-H.
        p300.aspirate(200, ethanol_well)
        p300.dispense(200, mag_target_col[0], rate=0.2)
        # 11. Slowly mix Magnet Wells Column 1 A-H 10 times.
        # (Magnet still engaged, washing bead pellet).
        p300.mix(10, 200, mag_target_col[0], rate=0.2)
        # 12. Remove 200 uL from Magnet Wells Column 1 A-H.
        # TODO: Aspirate away from pellet
        p300.aspirate(200, mag_target_col[0], rate=0.2)
        p300.dispense(200, waste_well.top())
        p300.blow_out()
        # 13. Discard tips
        p300.drop_tip()
        # 14. Use 8-channel P300 to mix Reservoir Well 5
        # (80% EtOH -low viscosity)
        pick_up(p300)
        p300.mix(10, 200, ethanol_well)
        # 15. Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 1 A-H.
        p300.aspirate(200, ethanol_well)
        p300.dispense(200, mag_target_col[0], rate=0.2)
        # 16. Slowly mix Magnet Wells Column 1 A-H 10 times.
        # (Magnet still engaged, washing bead pellet).
        p300.mix(10, 200, mag_target_col[0], rate=0.2)
        # 17 Remove 200 uL from Magnet Wells Column 1 A-H.
        p300.aspirate(200, mag_target_col[0], rate=0.2)
        p300.dispense(200, waste_well.top())
        p300.blow_out()
        # 18 Discard tips. 24 tips used total
        p300.drop_tip()
        # 19 Hold for 10 minutes (magnet still engaged)
        #    to let residual ethanol evaporate.
        ctx.delay(minutes=10)
        # 20 Close thermocycler lid.
        tc_mod.close_lid()
        # 21 Heat thermocycler to 37C for 2 minutes
        tc_mod.lid_temperature(98)
        tc_mod.set_block_temperature(37, hold_time_minutes=2)
        # 22 Open thermocycler lid.
        tc_mod.open_lid()
        # 23 Disengage magnet.
        tc_mod.disengage()
        # 24 Use 8-channel P300 to transfer 30 uL of water from
        #    Thermocycler Column 9 Rows A-H to Magnet Wells Column 1 A-H.
        #    Dispense liquid over the side of the tube with the magnetic
        #    contact.
        pick_up(p300)
        # TODO: Alter the dispense location so that it dispenses over the bead
        p300.aspirate(resusp_water_vol, water_column[0])
        p300.dispense(resusp_water_vol, mag_target_col[0])
        # 25 Mix Magnet Wells Column 1 A-H at 1 minute intervals for
        #    10 minutes (eluting DNA from beads).
        for i in range(10):
            p300.mix(10, resusp_water_vol-5, mag_target_col[0], rate=1)
            ctx.delay(minutes=1)
        p300.touch_tip()
        p300.blow_out(mag_target_col.center())
        # 26 Engage magnet.
        mag_mod.engage()
        # 27 Hold for 3 minutes (magnet still engaged).
        ctx.delay(minutes=3)
        # 28 Transfer 28uL from Magnet Wells Column 1 A-H to Thermocycler
        #    Column <n> Rows A-H.
        p300.aspirate(purified_DNA_vol, target_col[0])
        # 29 Discard tips. 32 tips used
        p300.drop_tip()
        # 30 Disengage magnet.
        mag_mod.disengage()

    # reagents & samples
    DNA_initial_col = tc_plate.columns()[0]
    DNA_target_col_1 = tc_plate.columns()[2]
    DNA_target_col_2 = tc_plate.columns()[4]
    DNA_target_col_3 = tc_plate.columns()[6]
    DNA_target_col_4 = tc_plate.columns()[8]

    mag_target_col = mag_plate.columns()[0]
    water_col_1_30ul = tc_plate.columns()[7]
    water_col_2_17ul = tc_plate.columns()[8]
    water_col_3_30ul = tc_plate.columns()[9]
    water_col_4_42ul = tc_plate.columns()[10]

    mag_beads = resv.wells_by_name()['A1']
    ethanol_well = resv.wells_by_name()['A5']
    waste_well = resv.wells()[-1]

    digest_mix = tmod_tubes.wells_by_name()['A1']
    patch_mix = tmod_tubes.wells_by_name()['A2']
    exo_mix = tmod_tubes.wells_by_name()['A3']
    TET2_mix = tmod_tubes.wells_by_name()['A4']
    Fe_sol = tmod_tubes.wells_by_name()['A5']
    stop_reagt = tmod_tubes.wells_by_name()['A6']
    NaOH = tmod_tubes.wells_by_name()['A7']
    dH2O = tmod_tubes.wells_by_name()['A8']
    APOBEC_mix = tmod_tubes.wells_by_name()['A9']
    pcr_mix = tmod_tubes.wells_by_name()['A10']
    barcode_pmr_1 = tmod_tubes.wells_by_name()['A11']
    barcode_pmr_2 = tmod_tubes.wells_by_name()['A12']
    barcode_pmr_3 = tmod_tubes.wells_by_name()['A13']
    barcode_pmr_4 = tmod_tubes.wells_by_name()['A14']
    barcode_pmr_5 = tmod_tubes.wells_by_name()['A15']
    barcode_pmr_6 = tmod_tubes.wells_by_name()['A16']
    barcode_pmr_7 = tmod_tubes.wells_by_name()['A17']
    barcode_pmr_8 = tmod_tubes.wells_by_name()['A18']

    # plate, tube rack maps

    # protocol
    ctx.comment("\n\nStep 1: Restriction enzyme digestion of DNA\n")
    # 1.1       Use P20 to mix Temperature Tube 1 (Digest Master Mix).
    # 1.2       Transfer 10 uL of Temperature Tube 1 to Thermocycler Tube 1A.
    # 1.3       Mix Thermocycler Tube A1.
    # 1.4       Discard Tip.
    # 1.5       Repeat steps 1.1 -1.4 for transfers from Temperature Tube 1
    # cont.     to Thermocycler Tubes 1B,1C,1D,1E,1F,1G, 1H.
    for i, well in enumerate(DNA_initial_col):
        pick_up(p20)
        mix_vol = 10 if i == len(DNA_initial_col) - 1 else 20
        p20.mix(10, mix_vol, digest_mix)
        p20.aspirate(10, digest_mix, rate=0.5)
        p20.dispense(10, well, rate=0.5)
        p20.mix(10, well)
        p20.drop_tip()
    # 1.6       Close lid.
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(98)
    # 1.7       Incubate at 37C for 60 minutes.
    tc_mod.set_block_temperature(37, hold_time_minutes=60)
    # 1.8       Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 1.9       Open lid.
    tc_mod.open_lid()
    tc_mod.set_lid_temperature(25)
    # Total volume after step 1: initial DNA sample 10 uL + 10 uL digest
    # master mix = 20 uL

    ctx.comment("\n\nStep 2: Patch ligatio\n")
    # 2.1       Use P20 to mix Temperature Tube 2 (Patch Master Mix).
    # 2.2       Transfer 15 uL of Temperature Tube 2 to Thermocycler Tube 1A.
    # 2.3       Mix Thermocycler Tube 1A.
    # 2.4       Discard Tip.
    # 2.5       Repeat steps 2.1 -2.4 for transfers from Temperature Tube 2
    #           to Thermocycler Tubes 1B,1C,1D,1E,1F,1G, 1H.
    for i, well in enumerate(DNA_initial_col):
        pick_up(p20)
        mix_vol = 15 if i == len(DNA_initial_col) - 1 else 20
        p20.mix(10, mix_vol, patch_mix)
        p20.aspirate(15, patch_mix, rate=0.5)
        p20.dispense(15, well, rate=0.5)
        p20.mix(10, well)
        p20.drop_tip()
    # 2.6       Close lid.
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(98)
    # 2.7       Cycle temperature: 94C for 30 seconds and 65 degrees for 4
    #           minutes for 25 cycles.
    # total volume: 20 + volume of patch master mix = 35 uL
    patch_cycle_profile = [
        {'temperature': 94, 'hold_time_seconds': 30},
        {'temperature': 65, 'hold_time_minutes': 4}]
    tc_mod.execute_profile(
        steps=patch_cycle_profile, repetitions=25, block_max_volume=35)
    # 2.8       Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 2.9       Open lid.
    tc_mod.open_lid()
    tc_mod.set_lid_temperature(25)

    ctx.comment("Step 3: Exonuclease degradation")
    # 3.1       Use P20 to mix Temperature Tube 3 (Exo Master Mix).
    # 3.2       Transfer 2 uL of Temperature Tube 3 to Thermocycler Tube 1A.
    #           total volume = 16 uL
    # 3.3       Mix Thermocycler Tube A1.
    # 3.4       Discard Tip.
    # 3.5       Repeat steps 3.1 -3.4 for transfers from Temperature Tube 3
    #           to Thermocycler Tubes B1, C1, D1, E1, F1, G1, H1.
    for i, well in enumerate(DNA_initial_col):
        pick_up(p20)
        # Mix such that there is 2 uL left in the well
        # (7-0)*2=14 (7-1)*2=12 etc.
        mix_vol = (len(DNA_initial_col) - 1 - i) * 2
        mix_vol = mix_vol if mix_vol > 2 else 1  # last mix only 2 uL left
        p20.mix(10, mix_vol, exo_mix)
        p20.aspirate(10, exo_mix, rate=0.5)
        p20.dispense(10, well, rate=0.5)
        p20.mix(10, well)
        p20.drop_tip()
    # 3.6       Close lid.
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(98)
    # 3.7       Incubate at 37C for 60 minutes.
    tc_mod.set_block_temperature(37, hold_time_minutes=60)
    # 3.8       Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 3.9       Open lid.
    tc_mod.open_lid()
    tc_mod.set_lid_temperature(25)

    ctx.comment("\n\nStep 4: AMPure cleanup #1\n")

    bead_cleanup(
        mix_vol=200,
        bead_vol=74,
        dna_vol=37,
        DNA_col=DNA_initial_col,
        dna_air_gap_vol=10,
        supernatant_vol=111,
        resusp_water_vol=30,
        water_column=water_col_1_30ul,
        purified_DNA_vol=28,
        target_col=DNA_target_col_1)

    ctx.comment("\n\nStep 5: TET2 Oxidation\n")

    # 5.1      Use P20 to mix Temperature Tube 4 (TET2 Master Mix).
    # 5.2      Transfer 17 uL of Temperature Tube 4 to Thermocycler Tube A3.
    # 5.3      Mix Thermocycler Tube A3.
    # 5.4      Discard Tip.
    # 5.5      Repeat steps 5.1 -5.4 for transfers from Temperature Tube 4
    #          to Thermocycler Tubes 3B,3C,3D,3E,3F,3G, 3H.
    # 5.6      Use P20 to mix Temperature Tube 5 (Fe solution).
    # 5.7      Transfer 5 uL of Temperature Tube 5 to Thermocycler Tube A3.
    # 5.8      Mix Thermocycler Tube 3A.
    # 5.9      Discard Tip.
    # 5.10     Repeat steps 5.6 -5.9 for transfers from Temperature Tube 5
    #          to Thermocycler Tubes B3, C3, D3, E3, F3, G3, H3.
    # 5.11     Close lid.
    # 5.12     Incubate at 37C for 60 minutes.
    # 5.13     Incubate at 25C for 3 minutes.
    # 5.14     Open lid.
    # 5.15     Use P20 to mix Temperature Tube 6 (Stop Reagent).
    # 5.16     Transfer 1 uL of Temperature Tube 6 to Thermocycler Tube 3A.
    # 5.17     Mix Thermocycler Tube 3A.
    # 5.18     Discard Tip.
    # 5.19     Repeat steps 5.15 -5.18 for transfers from Temperature Tube 6 to
    #          Thermocycler Tubes 3B,3C,3D,3E,3F,3G, 3H.
    # 5.20     Close lid.
    # 5.21     Incubate at 37C for 30 minutes.
    # 5.22     Incubate at 4C for 3 minutes.
    # 5.23     Open lid.

    ctx.comment("\n\nStep 6: AMPure cleanup #2\n")

    bead_cleanup(
        mix_vol=200,
        bead_vol=100,
        dna_vol=51,
        DNA_col=DNA_target_col_1,
        dna_air_gap_vol=10,
        supernatant_vol=151,
        resusp_water_vol=30,
        water_column=water_col_1_30ul,
        purified_DNA_vol=16,
        target_col=DNA_target_col_2)

    ctx.comment("\n\nStep 7: APOBEC Deamination\n")

    # 7.1      Close thermocycler.
    # 7.2      Incubate thermocycler at 50C for 3 minutes.
    # 7.3      Use P20 to mix Temperature Tube 7 (NaOH).
    # 7.4      Open thermocycler.
    # 7.5      Transfer 4 uL of Temperature Tube 7 to Thermocycler Tube 5A.
    # 7.6      Mix Thermocycler Tube 5A.
    # 7.7      Discard Tip.
    # 7.8      Repeat steps 7.5 -7.7 for transfers from Temperature Tube 7
    #          to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
    # 7.9      Close thermocycler.
    # 7.10     Incubate at 50C for 10 minutes.
    # 7.11     Incubate at 4C for 5 minutes.
    # 7.12     Open thermocycler.
    # 7.13     Use P20 to transfer 10 uL of Temperature Tube 8 (water) to
    #          Thermocycler Tube 5A.
    # 7.14     Mix Thermocycler Tube 5A.
    # 7.15     Discard Tip.
    # 7.16     Repeat steps 7.13 -7.15 for transfers from Temperature Tube 8
    #          to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
    # 7.17     Use P20 to mix Temperature Tube 9 (APOBEC Master Mix).
    # 7.18     Use P20 to transfer 20 uL of Temperature Tube 9 to Thermocycler
    #          Tube 5A.
    # 7.19     Mix Thermocycler Tube 5A.
    # 7.20     Discard Tip.
    # 7.21     Repeat steps 7.17 -7.20 for transfers from Temperature Tube 9 to
    #          Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
    # 7.22     Close lid.
    # 7.23     Incubate at 37C for 3 hours.
    # 7.24     Incubate at 4C for 3 minutes.
    # 7.25     Open lid.

    ctx.comment("\n\nStep 8: AMPure cleanup #3\n")

    bead_cleanup(
        mix_vol=200,
        bead_vol=100,
        dna_vol=50,
        DNA_col=DNA_target_col_2,
        dna_air_gap_vol=10,
        supernatant_vol=150,
        resusp_water_vol=30,
        water_column=water_col_3_30ul,
        purified_DNA_vol=29,
        target_col=DNA_target_col_3)

    ctx.comment("\n\nStep 9: PCR Master Mix Prep\n")

    # 9.1      Use P20 to mix Temperature Tube 10 (PCR Master Mix).
    # 9.2      Transfer 20 uL of Temperature Tube 10 to Thermocycler Tube 7A.
    # 9.3      Mix Thermocycler Tube 7A.
    # 9.4      Discard Tip.
    # 9.5      Repeat steps 9.1 -9.4 for transfers from Temperature Tube 10 to
    #          Thermocycler Tubes 7B,7C,7D,7E,7F,7G, 7H.
    # 9.6      Use P20 to mix Temperature Tube 11 (Barcode Primer 1).
    # 9.7      Transfer 1 uL of Temperature Tube 11 to Thermocycler Tube 7A.
    # 9.8      Mix Thermocycler Tube 7A.
    # 9.9       Discard Tip.
    # 9.10     Use P20 to mix Temperature Tube 12 (Barcode Primer 2).
    # 9.11     Transfer 1 uL of Temperature Tube 12 to Thermocycler Tube 7B.
    # 9.12     Mix Thermocycler Tube 7B.
    # 9.13     Discard Tip.
    # 9.14     Use P20 to mix Temperature Tube 13 (Barcode Primer 3).
    # 9.15     Transfer 1 uL of Temperature Tube 13 to Thermocycler Tube 7C.
    # 9.16     Mix Thermocycler Tube 7C.
    # 9.17     Discard Tip.
    # 9.18     Use P20 to mix Temperature Tube 14 (Barcode Primer 4).
    # 9.19     Transfer 1 uL of Temperature Tube 14 to Thermocycler Tube 7D.
    # 9.20     Mix Thermocycler Tube 7D.
    # 9.21     Use P20 to mix Temperature Tube 15 (Barcode Primer 5).
    # 9.22     Transfer 1 uL of Temperature Tube 15 to Thermocycler Tube 7E.
    # 9.23     Mix Thermocycler Tube 7E.
    # 9.24     Discard Tip.
    # 9.25     Use P20 to mix Temperature Tube 16 (Barcode Primer 6).
    # 9.26     Transfer 1 uL of Temperature Tube 16 to Thermocycler Tube 7F.
    # 9.27     Mix Thermocycler Tube 7F.
    # 9.28     Use P20 to mix Temperature Tube 17 (Barcode Primer 7).
    # 9.29     Transfer 1 uL of Temperature Tube 17 to Thermocycler Tube 7G.
    # 9.30     Mix Thermocycler Tube 7G.
    # 9.31     Discard Tip.
    # 9.32     Use P20 to mix Temperature Tube 18 (Barcode Primer 8).
    # 9.33     Transfer 1 uL of Temperature Tube 18 to Thermocycler Tube 7H.
    # 9.34     Mix Thermocycler Tube 7H.
    # 9.35     Discard Tip.
    # 9.36     Close lid.
    # 9.37     Incubate at 95C for 30 sec.
    # 9.38     Cycle temperature: 94C for 30 seconds and 60 degrees for 3
    #          minutes for 25 cycles.
    # 9.39     Incubate at 4C for 3 minutes.
    # 9.40     Open lid.

    ctx.comment("\n\nStep 10: AMPure cleanup #4\n")

    bead_cleanup(
        mix_vol=200,
        bead_vol=100,
        dna_vol=50,
        DNA_col=DNA_target_col_3,
        dna_air_gap_vol=10,
        supernatant_vol=150,
        resusp_water_vol=42,
        water_column=water_col_3_30ul,
        purified_DNA_vol=40,
        target_col=DNA_target_col_4)

    tc_mod.set_lid_temperature(98)
    tc_mod.close_lid()
    tc_mod.set_block_temperature(4)
    ctx.comment("\n\n ~~~ Protocol Finished!  ~~~ \n")
