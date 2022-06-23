from opentrons import protocol_api
from typing import List
from opentrons.protocol_api.labware import Well
from opentrons.types import Point

metadata = {
    'protocolName': 'MethylPatch Protocol for Opentrons OT-2',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "p20_mount":"left",
                                  "barcode_tube_init_vol":10,
                                  "mag_engage_height":3.45,
                                  "num_mix_repns":1,
                                  "is_flash_lights":true
                                  }
                                  """)  # noqa: E501 Do not report 'line too long' warnings
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [p20_mount,
     barcode_tube_init_vol,
     mag_engage_height,
     num_mix_repns,
     is_flash_lights] = get_values(  # noqa: F821
     "p20_mount",
     "barcode_tube_init_vol",
     "mag_engage_height",
     "num_mix_repns",
     "is_flash_lights")

    p300_mount = 'right' if p20_mount == 'left' else 'left'

    # load modules

    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    # The Thermocycler has a default position that
    # covers Slots 7, 8, 10, and 11.
    tc_mod = ctx.load_module('thermocycler module')
    mag_mod = ctx.load_module('magnetic module gen2', '4')
    temp_mod = ctx.load_module('temperature module gen2', '1')

    # load labware

    resv = ctx.load_labware('nest_12_reservoir_15ml', '9')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_200ul_flat')
    mag_plate = mag_mod.load_labware('nest_96_wellplate_200ul_flat')
    tmod_tubes = temp_mod.load_labware(
        'opentrons_24_aluminumblock_nest_1.5ml_snapcap')

    # load tipracks

    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', '2')]
    tiprack200s = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', '5', '6')]

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
    # Keep track of how much waste we have generated so that the waste well
    # does not overflow
    waste_vol = 0

    def bead_cleanup(
            mix_vol: float,
            bead_vol: float,
            dna_vol: float,
            DNA_source_col: List[Well],
            mag_target_col: List[Well],
            dna_air_gap_vol: float,
            supernatant_vol: float,
            resusp_water_vol: float,
            water_column: List[Well],
            purified_DNA_vol: float,
            purified_dna_target_col: List[Well]):
        """
        This function transfers samples from a given DNA sample source column
        (on the thermocycler plate) to the magnetic module plate and performs
        an AMPure bead cleanup of the DNA. After the DNA has been cleaned it
        is transferred to a new column on the thermocycler plate. Reservoir
        well 1 contains beads and reservoir well 5 contains 80 % ethanol.

        :param mix_vol: The mixing volume for each tip of the 8-channel p300
        for mixing the bead well on the reservoir
        :param bead_vol: The volume of beads to use for the cleanup.
        :param dna_vol: The volume of DNA sample to transfer from the TC plate
        to the mag mod plate.
        :param mag_target_col: The magnetic plate column to dispense the
        DNA samples in for cleanup.
        :param dna_air_gap_vol: Air gap volume in µL for the DNA sample transfr
        :param supernatant_vol: The volume of supernatant to remove from the
        well after the beads have bound the DNA. The supernatant is transferred
        to either the last or penultimate well of the reservoir as trash.
        :param resusp_water_vol: The volume of water to resuspend the cleaned
        DNA in.
        :param water_column: The column on the thermocycler from which to
        aspirate water from for the resuspension.
        :param purified_DNA_vol: The volume of purified DNA to transfer back
        to the TC plate.
        :param purified_dna_target_col: The column (on the TC plate) to
        transfer the purified DNA to.
        """

        nonlocal p300, ctx, mag_beads, mag_mod, waste_wells
        nonlocal ethanol_well, waste_vol
        mag_well = mag_target_col[0]
        well_radius = mag_well.diameter/2
        # Left and right locations 1 mm from the bottom and 1 mm from the side
        # of the well.
        mag_well_left_locn = mag_well.bottom(1).move(
            Point(-well_radius-1, 0, 0))
        mag_well_right_locn = mag_well.bottom(1).move(
            Point(well_radius-1, 0, 0))
        ctx.comment("\nMixing and transferring AMPure beads\n")
        # 1. Use 8-channel P300 to mix Reservoir Well 1
        # (Ampure Beads - High Viscosity).
        pick_up(p300)
        p300.mix(num_mix_repns, mix_vol, mag_beads, rate=0.3)
        # 2. Transfer <bead_vol> uL of Reservoir Well 1 to
        # Magnet Wells Column <n> A-H.
        p300.aspirate(bead_vol, mag_beads, rate=0.3)
        p300.dispense(bead_vol, mag_well, rate=0.3)
        # Solution is viscous, try to get it all out
        p300.touch_tip()
        p300.blow_out()
        # 3. Transfer <dna_vol> uL of Thermocycler Column <n> A-H to
        # Magnet Wells Column <n> A-H.
        ctx.comment(
            "\nTransferring DNA samples from the thermocycler to the magnetic "
            "module\n")
        p300.aspirate(dna_vol, DNA_source_col[0])
        p300.air_gap(dna_air_gap_vol)
        p300.dispense(dna_vol+dna_air_gap_vol, mag_well)
        # 4. Mix Magnet Wells Column 1 A-H at 1 minute intervals for 10 minutes
        # Total volume in the mag column: bead_vol + dna_vol
        mix_vol = bead_vol + dna_vol - 20
        mix_vol = mix_vol if mix_vol < 200 else 200
        mix_vol = mix_vol if mix_vol > 5 else (bead_vol + dna_vol)/2
        if mix_vol < 0:
            raise Exception(
                "The mixing vol for step 4. in the bead cleanup function "
                f" is less than 0 uL ({mix_vol})")
        mix_vol = mix_vol if mix_vol < 200 else 200
        for i in range(10):
            p300.mix(num_mix_repns, mix_vol, mag_well, rate=1)
            ctx.delay(minutes=1)
        p300.touch_tip()
        p300.blow_out()
        # 5. Engage magnet.
        mag_mod.engage(height_from_base=mag_engage_height)
        # 6. Hold for 5 minutes
        ctx.delay(minutes=5)
        # 7. remove <supernatant_vol> from Magnet Wells Column 1 A-H.
        # The magnetic pellet is on the right, so aspirate supernatant
        # from the left so the pellet is not disturbed
        ctx.comment("\nRemoving supernatant from beads\n")
        p300.aspirate(supernatant_vol, mag_well_left_locn, rate=0.2)
        supernatant_air_gap_vol = 10 if supernatant_vol < 190 \
            else 200 - supernatant_vol
        if supernatant_air_gap_vol > 0:
            p300.air_gap(supernatant_air_gap_vol)
        p300.dispense(
            supernatant_vol+supernatant_air_gap_vol, waste_wells[-1].top())
        waste_vol += supernatant_vol * 8
        if waste_vol > 12_000:
            waste_wells.pop()
            waste_vol = 0
        # 400*8*4 uL of ethanol=12.8 mL
        # Supernatant volumes to waste: (111 + 151 + 150*2)*8 = 4.5 mL
        # Total waste volume: 12.8 mL + 4.5 = 17.3 mL for the entire ptcl.
        p300.blow_out()
        # 8. Discard tips.
        p300.drop_tip()
        # 9. Use 8-channel P300 to mix Reservoir Well 5
        # (80% EtOH -low viscosity)
        pick_up(p300)
        ctx.comment("\nPerforming first 80 % ethanol wash\n")
        p300.mix(num_mix_repns, 200, ethanol_well)
        # 10. Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 1 A-H.
        p300.aspirate(200, ethanol_well)
        p300.dispense(200, mag_well, rate=0.2)
        # 11. Slowly mix Magnet Wells Column 1 A-H 10 times.
        # (Magnet still engaged, washing bead pellet).
        p300.mix(num_mix_repns, 200, mag_well, rate=0.2)
        # 12. Remove 200 uL from Magnet Wells Column 1 A-H.
        p300.aspirate(200, mag_well_left_locn, rate=0.2)
        p300.dispense(200, waste_wells[-1].top())
        waste_vol += 200 * 8
        if waste_vol > 12_000:
            waste_wells.pop()
            waste_vol = 0
        p300.blow_out()
        # 13. Discard tips
        p300.drop_tip()
        # 14. Use 8-channel P300 to mix Reservoir Well 5
        # (80% EtOH -low viscosity)
        ctx.comment("\nPerforming second 80 % ethanol wash\n")
        pick_up(p300)
        p300.mix(num_mix_repns, 200, ethanol_well)
        # 15. Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 1 A-H.
        p300.aspirate(200, ethanol_well)
        p300.dispense(200, mag_well, rate=0.2)
        # 16. Slowly mix Magnet Wells Column 1 A-H 10 times.
        # (Magnet still engaged, washing bead pellet).
        p300.mix(num_mix_repns, 200, mag_well, rate=0.2)
        # 17 Remove 200 uL from Magnet Wells Column 1 A-H away from pellet.
        p300.aspirate(200, mag_well_left_locn, rate=0.2)
        p300.dispense(200, waste_wells[-1].top())
        waste_vol += 200 * 8
        if waste_vol > 12_000:
            waste_wells.pop()
            waste_vol = 0
        p300.blow_out()
        # 18 Discard tips. 24 tips used total
        p300.drop_tip()
        # 19 Hold for 10 minutes (magnet still engaged)
        #    to let residual ethanol evaporate.
        ctx.delay(minutes=10)
        # 20 Close thermocycler lid.
        tc_mod.close_lid()
        # 21 Heat thermocycler to 37C for 2 minutes
        # tc_mod.set_lid_temperature(98) - assume that the lid temperature
        # has been set already.
        ctx.comment("\nIncubating and resuspending cleaned DNA\n")
        tc_mod.set_block_temperature(37, hold_time_minutes=2)
        # 22 Open thermocycler lid.
        tc_mod.open_lid()
        # 23 Disengage magnet.
        mag_mod.disengage()
        # 24 Use 8-channel P300 to transfer 30 uL of water from
        #    Thermocycler Column 9 Rows A-H to Magnet Wells Column 1 A-H.
        #    Dispense liquid over the side of the tube with the magnetic
        #    contact.
        pick_up(p300)
        p300.aspirate(resusp_water_vol, water_column[0])
        p300.dispense(resusp_water_vol, mag_well_right_locn)
        # 25 Mix Magnet Wells Column 1 A-H at 1 minute intervals for
        #    10 minutes (eluting DNA from beads).
        for i in range(10):
            p300.mix(
                num_mix_repns, resusp_water_vol-5, mag_well_right_locn, rate=1)
            ctx.delay(minutes=1)
        p300.touch_tip()
        p300.blow_out(mag_well.top())
        # 26 Engage magnet.
        mag_mod.engage(height_from_base=mag_engage_height)
        # 27 Hold for 3 minutes (magnet still engaged).
        ctx.delay(minutes=3)
        # 28 Transfer <x> uL from Magnet Wells Column 1 A-H to Thermocycler
        #    Column <n> Rows A-H. Aspirate away from the bead pellet
        #    i.e. aspirate from the left side of the well.
        ctx.comment(
            "\nTransferring cleaned DNA back to the thermocycler plate\n")
        p300.aspirate(purified_DNA_vol, mag_well_left_locn)
        p300.dispense(purified_DNA_vol, purified_dna_target_col[0])
        # 29 Discard tips. 32 tips used
        p300.drop_tip()
        # 30 Disengage magnet.
        mag_mod.disengage()

    def transfer_reagent(
            dna_sample_column: List[Well],
            reagent: Well,
            reag_vol: float,
            well_mixing_vol: float,
            reagent_mix: bool = True):
        """
        This function is used to transfer a reagent from a tube on the
        temperature module to wells on the plate in the thermocycler.
        :param dna_sample_column: The column containing the target wells
        :param reagent: The reagent tube
        :param reag_vol: How much reagent volume to dispense into each
        target well.
        :param well_mixing_vol: Mixing volume for mixing the target well
        after the reagent has been added.
        :param reagent_mix: Whether to mix the reagent or not before dispensing
        it in the target well.
        """
        nonlocal p20
        num_wells = len(dna_sample_column)
        # Repeat for the entire column
        for i, well in enumerate(dna_sample_column):
            # 1. Use the p20 to mix the reagent tube
            pick_up(p20)
            # All reagents get mixed in this protocol except for water
            # The flag allows us to skip mixing in that case
            if reagent_mix:
                remaining_reagent_vol = (num_wells - i) * reag_vol
                mix_vol = remaining_reagent_vol if remaining_reagent_vol < 20 \
                    else 20
                p20.mix(num_mix_repns, mix_vol, reagent)
            # 2. Transfer x uL of the reagent tube to the target well
            p20.aspirate(10, reagent, rate=0.5)
            p20.dispense(10, well, rate=0.5)
            p20.touch_tip()
            # 3. Mix the target well
            p20.mix(num_mix_repns, well_mixing_vol, well)
            # 4. Drop the tip
            p20.drop_tip()

    # reagents & samples

    # DNA samples are moved to a fresh column after each bead cleanup
    # The exception is the 5th sample column which contained water previously
    DNA_initial_col = tc_plate.columns()[0]   # 1st sample col = 1st plate col
    DNA_target_col_1 = tc_plate.columns()[2]  # 2nd sample col = 3rd plate col
    DNA_target_col_2 = tc_plate.columns()[4]  # 3rd sample col = 5th plate col
    DNA_target_col_3 = tc_plate.columns()[6]  # 4th sample col = 7th plate col
    DNA_target_col_4 = tc_plate.columns()[8]  # 5th sample col = 9th plate col

    mag_target_col_1 = mag_plate.columns()[0]  # 1st sample cleanup column = 1
    mag_target_col_2 = mag_plate.columns()[2]  # 2nd sample cleanup column = 3
    mag_target_col_3 = mag_plate.columns()[4]  # 3rd sample cleanup column = 5
    mag_target_col_4 = mag_plate.columns()[6]  # 4th sample cleanup column = 7

    water_col_1_30ul = tc_plate.columns()[8]
    water_col_2_17ul = tc_plate.columns()[9]
    water_col_3_30ul = tc_plate.columns()[10]
    water_col_4_42ul = tc_plate.columns()[11]

    mag_beads = resv.wells_by_name()['A1']
    ethanol_well = resv.wells_by_name()['A5']
    waste_wells = resv.wells()[-2:]

    digest_mix = tmod_tubes.wells()[0]  # Temperature Tube 1
    patch_mix = tmod_tubes.wells()[1]  # Temperature Tube 2
    exo_mix = tmod_tubes.wells()[2]  # Temperature Tube 3
    TET2_mix = tmod_tubes.wells()[3]  # Temperature Tube 4
    Fe_sol = tmod_tubes.wells()[4]  # Temperature Tube 5
    stop_reagt = tmod_tubes.wells()[5]  # Temperature TUbe 6
    NaOH = tmod_tubes.wells()[6]  # Temperature Tube 7
    dH2O = tmod_tubes.wells()[7]  # Temperature Tube 8
    APOBEC_mix = tmod_tubes.wells()[8]  # Temperature Tube 9
    pcr_mix = tmod_tubes.wells()[9]  # Temperature Tube 10
    barcodes = tmod_tubes.wells()[10:18]

    # plate, tube rack maps

    # protocol
    temp_mod.set_temperature(4)

    ctx.comment("\n\nStep 1: Restriction enzyme digestion of DNA\n")
    # 1.1       Use P20 to mix Temperature Tube 1 (Digest Master Mix).
    # 1.2       Transfer 10 uL of Temperature Tube 1 to Thermocycler Tube 1A.
    # 1.3       Mix Thermocycler Tube A1.
    # 1.4       Discard Tip.
    # 1.5       Repeat steps 1.1 -1.4 for transfers from Temperature Tube 1
    # cont.     to Thermocycler Tubes 1B,1C,1D,1E,1F,1G, 1H.
    transfer_reagent(
        dna_sample_column=DNA_initial_col,
        reagent=digest_mix,
        reag_vol=10,
        well_mixing_vol=18)
    # 1.6       Close lid.
    tc_mod.close_lid()
    # Set the lid temperature here and keep it throughout the protocol
    tc_mod.set_lid_temperature(98)
    # 1.7       Incubate at 37C for 60 minutes.
    tc_mod.set_block_temperature(37, hold_time_minutes=60)
    # 1.8       Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 1.9       Open lid.
    tc_mod.open_lid()
    # Total volume after step 1: initial DNA sample 10 uL + 10 uL digest
    # master mix = 20 uL total

    ctx.comment("\n\nStep 2: Patch ligation\n")
    # 2.1       Use P20 to mix Temperature Tube 2 (Patch Master Mix).
    # 2.2       Transfer 15 uL of Temperature Tube 2 to Thermocycler Tube 1A.
    # 2.3       Mix Thermocycler Tube 1A.
    # 2.4       Discard Tip.
    # 2.5       Repeat steps 2.1 -2.4 for transfers from Temperature Tube 2
    #           to Thermocycler Tubes 1B,1C,1D,1E,1F,1G, 1H.
    transfer_reagent(
        dna_sample_column=DNA_initial_col,
        reagent=patch_mix,
        reag_vol=15,
        well_mixing_vol=20)
    # 2.6       Close lid.
    tc_mod.close_lid()
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

    ctx.comment("\n\nStep 3: Exonuclease degradation\n")
    # 3.1       Use P20 to mix Temperature Tube 3 (Exo Master Mix).
    # 3.2       Transfer 2 uL of Temperature Tube 3 to Thermocycler Tube 1A.
    #           total volume = 16 uL
    # 3.3       Mix Thermocycler Tube A1.
    # 3.4       Discard Tip.
    # 3.5       Repeat steps 3.1 -3.4 for transfers from Temperature Tube 3
    #           to Thermocycler Tubes B1, C1, D1, E1, F1, G1, H1.
    transfer_reagent(
        dna_sample_column=DNA_initial_col,
        reagent=exo_mix,
        reag_vol=2,
        well_mixing_vol=20)
    # 3.6       Close lid.
    tc_mod.close_lid()
    # 3.7       Incubate at 37C for 60 minutes.
    tc_mod.set_block_temperature(37, hold_time_minutes=60)
    # 3.8       Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 3.9       Open lid.
    tc_mod.open_lid()

    ctx.comment("\n\nStep 4: AMPure cleanup #1\n")

    bead_cleanup(
        mix_vol=200,
        bead_vol=74,
        dna_vol=37,
        DNA_source_col=DNA_initial_col,
        mag_target_col=mag_target_col_1,
        dna_air_gap_vol=10,
        supernatant_vol=111,
        resusp_water_vol=30,
        water_column=water_col_1_30ul,
        purified_DNA_vol=28,
        purified_dna_target_col=DNA_target_col_1)

    ctx.comment("\n\nStep 5: TET2 Oxidation\n")

    # 5.1      Use P20 to mix Temperature Tube 4 (TET2 Master Mix).
    # 5.2      Transfer 17 uL of Temperature Tube 4 to Thermocycler Tube A3.
    # 5.3      Mix Thermocycler Tube A3.
    # 5.4      Discard Tip.
    # 5.5      Repeat steps 5.1 -5.4 for transfers from Temperature Tube 4
    #          to Thermocycler Tubes 3B,3C,3D,3E,3F,3G, 3H.
    # Well volume: 28 + 17 = 45 uL
    transfer_reagent(
        dna_sample_column=DNA_target_col_1,
        reagent=TET2_mix,
        reag_vol=17,
        well_mixing_vol=20)
    # 5.6      Use P20 to mix Temperature Tube 5 (Fe solution).
    # 5.7      Transfer 5 uL of Temperature Tube 5 to Thermocycler Tube A3.
    # 5.8      Mix Thermocycler Tube 3A.
    # 5.9      Discard Tip.
    # 5.10     Repeat steps 5.6 -5.9 for transfers from Temperature Tube 5
    #          to Thermocycler Tubes B3, C3, D3, E3, F3, G3, H3.
    # Well volume: 45+5 = 50
    transfer_reagent(
        dna_sample_column=DNA_target_col_1,
        reagent=Fe_sol,
        reag_vol=5,
        well_mixing_vol=20)
    # 5.11     Close lid.
    tc_mod.close_lid()
    # 5.12     Incubate at 37C for 60 minutes.
    tc_mod.set_block_temperature(37, hold_time_minutes=60)
    # 5.13     Incubate at 25C for 3 minutes.
    tc_mod.set_block_temperature(25, hold_time_minutes=3)
    # 5.14     Open lid.
    tc_mod.open_lid()
    # 5.15     Use P20 to mix Temperature Tube 6 (Stop Reagent).
    # 5.16     Transfer 1 uL of Temperature Tube 6 to Thermocycler Tube 3A.
    # 5.17     Mix Thermocycler Tube 3A.
    # 5.18     Discard Tip.
    # 5.19     Repeat steps 5.15 -5.18 for transfers from Temperature Tube 6 to
    #          Thermocycler Tubes 3B,3C,3D,3E,3F,3G, 3H.
    transfer_reagent(
        dna_sample_column=DNA_target_col_1,
        reagent=stop_reagt,
        reag_vol=1,
        well_mixing_vol=20)
    # 5.20     Close lid.
    tc_mod.close_lid()
    # 5.21     Incubate at 37C for 30 minutes.
    tc_mod.set_block_temperature(37, hold_time_minutes=30)
    # 5.22     Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 5.23     Open lid.
    tc_mod.open_lid()

    ctx.comment("\n\nStep 6: AMPure cleanup #2\n")
    # 6.1 Use 8-channel P300 to mix Reservoir Well 1
    #     (Ampure Beads - High Viscosity).
    # 6.2 Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 3 A-H.
    # 6.3 Transfer 51 uL of Thermocycler Column 3 A-H to Magnet Wells
    #     Column 3 A-H.
    # 6.4 Mix Magnet Wells Column 3 A-H at 1 minute intervals for 10 minutes.
    # 6.5 Engage magnet.
    # 6.6 Hold for 5 minutes (magnet still engaged).
    # 6.7 Remove 151 uL from Magnet Wells Column 3 A-H.
    # 6.8 Discard tips.
    # 6.9 Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
    # 6.10 Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 3 A-H.
    # 6.11 Slowly mix Magnet Wells Column 3 A-H 10 times.
    #      (Magnet still engaged, washing bead pellet).
    # 6.12 Remove 200 uL from Magnet Wells Column 3 A-H.
    # 6.13 Discard tips.
    # 6.14 Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
    # 6.15 Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 3 A-H.
    # 6.16 Slowly mix Magnet Wells Column 3 A-H 10 times.
    #      (Magnet still engaged, washing bead pellet).
    # 6.17 Remove 200 uL from Magnet Wells Column 3 A-H.
    # 6.18 Discard tips.
    # 6.19 Hold for 10 minutes (magnet still engaged) to let
    #      residual ethanol evaporate.
    # 6.20 Close thermocycler lid.
    # 6.21 Heat thermocycler to 37C for 2 minutes.
    # 6.22 Open thermocycler lid.
    # 6.23 Disengage magnet.
    # 6.24 Use 8-channel P300 to transfer 17 uL of water from
    #      Thermocycler Column 10 Rows A-H to Magnet Wells Column 3 A-H.
    #      Dispense liquid over the side of the tube with the magnetic contact.
    # 6.25 Mix Magnet Wells Column 3 A-H at 1 minute intervals for 10 minutes
    #      (eluting DNA from beads).
    # 6.26 Engage magnet.
    # 6.27 Hold for 3 minutes (magnet still engaged).
    # 6.28 Transfer 16uL from Magnet Wells Column 3 A-H to Thermocycler
    #      Column 5 Rows A-H.
    # 6.29 Discard tips.
    # 6.30 Disengage magnet.
    bead_cleanup(
        mix_vol=200,
        bead_vol=100,
        dna_vol=51,
        DNA_source_col=DNA_target_col_1,
        mag_target_col=mag_target_col_2,
        dna_air_gap_vol=10,
        supernatant_vol=151,
        resusp_water_vol=17,
        water_column=water_col_2_17ul,
        purified_DNA_vol=16,
        purified_dna_target_col=DNA_target_col_2)

    ctx.comment("\n\nStep 7: APOBEC Deamination\n")

    # 7.1      Close thermocycler.
    tc_mod.close_lid()
    # 7.2      Incubate thermocycler at 50C for 3 minutes.
    tc_mod.set_block_temperature(50, hold_time_minutes=3)
    tc_mod.open_lid()
    # 7.3      Use P20 to mix Temperature Tube 7 (NaOH).
    # 7.4      Open thermocycler.
    # 7.5      Transfer 4 uL of Temperature Tube 7 to Thermocycler Tube 5A.
    # 7.6      Mix Thermocycler Tube 5A.
    # 7.7      Discard Tip.
    # 7.8      Repeat steps 7.5 -7.7 for transfers from Temperature Tube 7
    #          to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
    # Well volume: 16 + 4 = 20
    transfer_reagent(
        dna_sample_column=DNA_target_col_2,
        reagent=NaOH,
        reag_vol=4,
        well_mixing_vol=18)
    # 7.9      Close thermocycler.
    tc_mod.close_lid()
    # 7.10     Incubate at 50C for 10 minutes.
    tc_mod.set_block_temperature(50, hold_time_minutes=10)
    # 7.11     Incubate at 4C for 5 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=5)
    # 7.12     Open thermocycler.
    tc_mod.open_lid()
    # 7.13     Use P20 to transfer 10 uL of Temperature Tube 8 (water) to
    #          Thermocycler Tube 5A.
    # 7.14     Mix Thermocycler Tube 5A.
    # 7.15     Discard Tip.
    # 7.16     Repeat steps 7.13 -7.15 for transfers from Temperature Tube 8
    #          to Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
    # well volume: 20 + 10 = 30
    transfer_reagent(
        dna_sample_column=DNA_target_col_2,
        reagent=dH2O,
        reag_vol=10,
        well_mixing_vol=20,
        reagent_mix=False)
    # 7.17     Use P20 to mix Temperature Tube 9 (APOBEC Master Mix).
    # 7.18     Use P20 to transfer 20 uL of Temperature Tube 9 to Thermocycler
    #          Tube 5A.
    # 7.19     Mix Thermocycler Tube 5A.
    # 7.20     Discard Tip.
    # 7.21     Repeat steps 7.17 -7.20 for transfers from Temperature Tube 9 to
    #          Thermocycler Tubes 5B,5C,5D,5E,5F,5G, 5H.
    transfer_reagent(
        dna_sample_column=DNA_target_col_2,
        reagent=APOBEC_mix,
        reag_vol=20,
        well_mixing_vol=20)
    # 7.22     Close lid.
    tc_mod.close_lid()
    # 7.23     Incubate at 37C for 3 hours.
    tc_mod.set_block_temperature(37, hold_time_minutes=60*3)
    # 7.24     Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 7.25     Open lid.
    tc_mod.open_lid()

    ctx.comment("\n\nStep 8: AMPure cleanup #3\n")
    # 8.1 Use 8-channel P300 to mix Reservoir Well 1
    #     (Ampure Beads - High Viscosity).
    # 8.2 Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 5 A-H.
    # 8.3 Transfer 50 uL of Thermocycler Column 5 A-H to Magnet Wells
    #     Column 5 A-H.
    # 8.4 Mix Magnet Wells Column 5 A-H at 1 minute intervals for 10 minutes.
    # 8.5 Engage magnet.
    # 8.6 Hold for 5 minutes (magnet still engaged).
    # 8.7 Remove 150 uL from Magnet Wells Column 5 A-H.
    # 8.8 Discard tips.
    # 8.9 Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
    # 8.10 Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 5 A-H.
    # 8.11 Slowly mix Magnet Wells Column 5 A-H 10 times. (Magnet still
    #      engaged, washing bead pellet).
    # 8.12 Remove 200 uL from Magnet Wells Column 5 A-H.
    # 8.13 Discard tips.
    # 8.14 Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
    # 8.15 Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 5 A-H.
    # 8.16 Slowly mix Magnet Wells Column 5 A-H 10 times. (Magnet still
    #      engaged, washing bead pellet).
    # 8.17 Remove 200 uL from Magnet Wells Column 5 A-H.
    # 8.18 Discard tips.
    # 8.19 Hold for 10 minutes (magnet still engaged) to let residual
    #      ethanol evaporate.
    # 8.20 Close thermocycler lid.
    # 8.21 Heat thermocycler to 37C for 2 minutes.
    # 8.22 Open thermocycler lid.
    # 8.23 Disengage magnet.
    # 8.24 Use 8-channel P300 to transfer 30 uL of water from Thermocycler
    #      Column 11 Rows A-H to Magnet Wells Column 5 A-H. Dispense liquid
    #      over the side of the tube with the magnetic contact.
    # 8.25 Mix Magnet Wells Column 5 A-H at 1 minute intervals for
    #      10 minutes (eluting DNA from beads).
    # 8.26 Engage magnet.
    # 8.27 Hold for 3 minutes (magnet still engaged).
    # 8.28 Transfer 29 uL from Magnet Wells Column 5 A-H to Thermocycler
    #      Column 7 Rows A-H.
    # 8.29 Discard tips.
    # 8.30 Disengage magnet.

    bead_cleanup(
        mix_vol=200,
        bead_vol=100,
        dna_vol=50,
        DNA_source_col=DNA_target_col_2,
        mag_target_col=mag_target_col_3,
        dna_air_gap_vol=10,
        supernatant_vol=150,
        resusp_water_vol=30,
        water_column=water_col_3_30ul,
        purified_DNA_vol=29,
        purified_dna_target_col=DNA_target_col_3)

    ctx.comment("\n\nStep 9: PCR Master Mix Prep\n")

    # 9.1      Use P20 to mix Temperature Tube 10 (PCR Master Mix).
    # 9.2      Transfer 20 uL of Temperature Tube 10 to Thermocycler Tube 7A.
    # 9.3      Mix Thermocycler Tube 7A.
    # 9.4      Discard Tip.
    # 9.5      Repeat steps 9.1 -9.4 for transfers from Temperature Tube 10 to
    #          Thermocycler Tubes 7B,7C,7D,7E,7F,7G, 7H.
    # Well volume: 29 uL initial vol + 20 uL PCR mix = 49 uL
    transfer_reagent(
        dna_sample_column=DNA_target_col_3,
        reagent=pcr_mix,
        reag_vol=20,
        well_mixing_vol=20)
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
    for barcode_tube, d_well in zip(barcodes, DNA_target_col_3):
        pick_up(p20)
        mix_vol = barcode_tube_init_vol - 2
        mix_vol = barcode_tube_init_vol if barcode_tube_init_vol < 20 else 20
        p20.mix(num_mix_repns, mix_vol, barcode_tube)
        p20.aspirate(1, barcode_tube)
        p20.dispense(1, d_well)
        # The volume in the d_well is 29+1 = 30 uL, mix using 20 uL
        p20.mix(num_mix_repns, 20, d_well)
        p20.drop_tip()
    # 9.36     Close lid.
    tc_mod.close_lid()
    # 9.37     Incubate at 95C for 30 sec.
    tc_mod.set_block_temperature(95, hold_time_seconds=30)
    # 9.38     Cycle temperature: 94C for 30 seconds and 60 degrees for 3
    #          minutes for 25 cycles.
    # The well volume is 49 + 1 = 50 uL
    pcr_cycle_profile = [
        {'temperature': 94, 'hold_time_seconds': 30},
        {'temperature': 60, 'hold_time_minutes': 3}]
    tc_mod.execute_profile(
        steps=pcr_cycle_profile, repetitions=25, block_max_volume=50)
    # 9.39     Incubate at 4C for 3 minutes.
    tc_mod.set_block_temperature(4, hold_time_minutes=3)
    # 9.40     Open lid.
    tc_mod.open_lid()

    ctx.comment("\n\nStep 10: AMPure cleanup #4\n")
    # 10.1 Use 8-channel P300 to mix Reservoir Well 1 (Ampure Beads - High
    #      Viscosity).
    # 10.2 Transfer 100 uL of Reservoir Well 1 to Magnet Wells Column 7 A-H.
    # 10.3 Transfer 50 uL of Thermocycler Column 7 A-H to Magnet Wells
    #      Column 7 A-H.
    # 10.4 Mix Magnet Wells Column 7 A-H at 1 minute intervals for 10 minutes.
    # 10.5 Engage magnet.
    # 10.6 Hold for 5 minutes (magnet still engaged).
    # 10.7 Remove 150 uL from Magnet Wells Column 7 A-H.
    # 10.8 Discard tips.
    # 10.9 Use 8-channel P300 to mix Reservoir Well 5 (80% EtOH -low viscosity)
    # 10.10 Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 7 A-H.
    # 10.11 Slowly mix Magnet Wells Column 7 A-H 10 times. (Magnet still
    #       engaged, washing bead pellet).
    # 10.12 Remove 200 uL from Magnet Wells Column 7 A-H.
    # 10.13 Discard tips.
    # 10.14 Use 8-channel P300 to mix Reservoir Well 5
    #       (80% EtOH -low viscosity)
    # 10.15 Transfer 200 uL of Reservoir Well 5 to Magnet Wells Column 7 A-H.
    # 10.16 Slowly mix Magnet Wells Column 7 A-H 10 times.
    #       (Magnet still engaged, washing bead pellet).
    # 10.17 Remove 200 uL from Magnet Wells Column 7 A-H.
    # 10.18 Discard tips.
    # 10.19 Hold for 10 minutes (magnet still engaged) to let residual
    #       ethanol evaporate.
    # 10.20 Close thermocycler lid.
    # 10.21 Heat thermocycler to 37C for 2 minutes.
    # 10.22 Open thermocycler lid.
    # 10.23 Disengage magnet.
    # 10.24 Use 8-channel P300 to transfer 42 uL of water from Thermocycler
    #       Column 12 Rows A-H to Magnet Wells Column 7 A-H. Dispense liquid
    #       over the side of the tube with the magnetic contact.
    # 10.25 Mix Magnet Wells Column 7 A-H at 1 minute intervals for 10 minutes
    #       (eluting DNA from beads).
    # 10.26 Engage magnet.
    # 10.27 Hold for 3 minutes (magnet still engaged).
    # 10.28 Transfer 40 uL from Magnet Wells Column 7 A-H to Thermocycler
    #       Column 9 Rows A-H.
    # 10.29 Discard tips.
    # 10.30 Disengage magnet.

    bead_cleanup(
        mix_vol=200,
        bead_vol=100,
        dna_vol=50,
        DNA_source_col=DNA_target_col_3,
        mag_target_col=mag_target_col_4,
        dna_air_gap_vol=10,
        supernatant_vol=150,
        resusp_water_vol=42,
        water_column=water_col_4_42ul,
        purified_DNA_vol=40,
        purified_dna_target_col=DNA_target_col_4)

    # 10.31 Close thermocycler lid.
    tc_mod.close_lid()
    # 10.32 Hold thermocycler at 4C.
    tc_mod.set_block_temperature(4)
    # 10.33 Alert user that the protocol has finished.
    ctx.comment("\n\n ~~~ Protocol Finished!  ~~~ \n")
    initial_light_state = ctx.rail_lights_on
    opposite_state = not initial_light_state
    if is_flash_lights:
        for _ in range(5):
            ctx.set_rail_lights(opposite_state)
            ctx.delay(seconds=0.5)
            ctx.set_rail_lights(initial_light_state)
            ctx.delay(seconds=0.5)
