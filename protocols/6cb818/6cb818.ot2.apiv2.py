import math


metadata = {
    'title': 'Anti-CD154 Labeling of Peptide- and PMA-Stimulated Cells',
    'author': 'Steve Plonk',
    'apiLevel': '2.10'
}


def run(ctx):

    [adjust_final_vol, vol_cd154, vol_peptide1, vol_peptide2, vol_peptide3,
     vol_pma_ca, vol_culture_medium, labware_cultureplate,
     slot_cultureplate, slot_snapcaps, slot_screwcaps,
     clearance_snapcap, clearance_screwcap, clearance_plate,
     clearance_mix] = get_values(  # noqa: F821
        "adjust_final_vol", "vol_cd154", "vol_peptide1", "vol_peptide2",
        "vol_peptide3", "vol_pma_ca", "vol_culture_medium",
        "labware_cultureplate", "slot_cultureplate",
        "slot_snapcaps", "slot_screwcaps", "clearance_snapcap",
        "clearance_screwcap", "clearance_plate", "clearance_mix")

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    # p20s, p300s and tips
    tips20 = [ctx.load_labware(
     'opentrons_96_tiprack_20ul', str(slot)) for slot in [2]]
    p20s = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=tips20)

    tips300 = [ctx.load_labware(
     'opentrons_96_tiprack_300ul', str(slot)) for slot in [5]]
    p300s = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=tips300)

    # load labware
    culture_plate = ctx.load_labware(
     labware_cultureplate, slot_cultureplate, "Culture Plate")
    rack_snapcaps = ctx.load_labware(
     "opentrons_24_tuberack_nest_1.5ml_snapcap", slot_snapcaps,
     "Rack with Snap Cap Tubes")
    rack_screwcaps = ctx.load_labware(
     "opentrons_24_tuberack_nest_1.5ml_screwcap", slot_screwcaps,
     "Rack with Screw Cap Tubes")

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

    # reagents in snapcaps with vol and liquid height tracking
    [peptide1, peptide2, peptide3, pma_ca] = rack_snapcaps.rows()[0][:4]

    peptide1.liq_vol = vol_peptide1
    peptide2.liq_vol = vol_peptide2
    peptide3.liq_vol = vol_peptide3
    pma_ca.liq_vol = vol_pma_ca

    # reagents in screwcaps with vol and liquid height tracking
    [cd154, culture_medium] = rack_screwcaps.rows()[0][:2]

    cd154.liq_vol = vol_cd154
    culture_medium.liq_vol = vol_culture_medium

    # culture plate wells with vol and liquid height tracking
    plate_wells = [column[:5] for column in culture_plate.columns()[:2]]

    for column in plate_wells:
        for index, well in enumerate(column):
            well.liq_vol = 200 if index == 0 else 0

    # add anti-CD154 to cell suspension in A1 and A2 and mix
    for column in plate_wells:

        p20s.pick_up_tip()
        p300s.pick_up_tip()

        ht_cd154 = liq_height(cd154) - 3 if liq_height(cd154) - 3 > 1 else 1
        ht_cells = liq_height(
         column[0]) - 3 if liq_height(column[0]) - 3 > 1 else 1
        p20s.aspirate(5, cd154.bottom(ht_cd154))
        p20s.dispense(5, column[0].bottom(ht_cells))
        for rep in range(5):
            p300s.aspirate(160, column[0].bottom(1), rate=2)
            p300s.dispense(160, column[0].bottom(ht_cells), rate=2)

        p300s.drop_tip()
        p20s.drop_tip()

    # transfer cell suspension to B1-E1 and B2-E2
    for column in plate_wells:
        p300s.pick_up_tip()
        for rep in range(5):
            p300s.aspirate(160, column[0].bottom(1), rate=2)
            ht = 7 if rep < 4 else 1
            p300s.dispense(160, column[0].bottom(ht), rate=2)
        for well in column[1:]:
            p300s.aspirate(40, column[0].bottom(1))
            p300s.dispense(40, well.bottom(1))
            p300s.touch_tip(radius=0.75, v_offset=-4, speed=20)
        p300s.drop_tip()

    # add reagent (peptides 1, 2 and 3 and PMA) to B1-B2, C1-C2, D1-D2, E1-E2
    for reagent, vol, index in zip(
     [peptide1, peptide2, peptide3, pma_ca], [5, 5, 10, 12], [1, 2, 3, 4]):
        for column in plate_wells:
            p20s.pick_up_tip()
            reagent.liq_vol -= vol
            ht = liq_height(reagent) - 3 if liq_height(reagent) - 3 > 1 else 1
            p20s.aspirate(vol, reagent.bottom(ht))
            p20s.dispense(vol, column[index].bottom(2))
            for rep in range(1):
                p20s.aspirate(20, column[index].bottom(2))
                p20s.dispense(20, column[index].bottom(2))
            p20s.drop_tip()

    # optionally add 60 uL culture medium to each well
    if adjust_final_vol:
        for column in plate_wells:
            for well in column:
                p300s.pick_up_tip()
                culture_medium.liq_vol -= 60
                ht = liq_height(
                 culture_medium) - 3 if liq_height(culture_medium) > 1 else 1
                p300s.aspirate(60, culture_medium.bottom(ht))
                p300s.dispense(60, well.bottom(4))
                p300s.touch_tip(radius=0.75, v_offset=-4, speed=20)
                p300s.drop_tip()
