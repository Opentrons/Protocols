from opentrons.protocol_api.labware import Well
from opentrons import types
import math


metadata = {
    'title': 'Anti-CD154 Labeling of Peptide- and PMA-Stimulated Cells',
    'author': 'Steve Plonk',
    'apiLevel': '2.10'
}


def run(ctx):

    [adjust_final_vol, vol_cd154, vol_peptide1, vol_peptide2, vol_peptide3,
     vol_pma_ca, vol_culture_medium, labware_cultureplate, labware_tips,
     slot_cultureplate, slot_tipbox, slot_snapcaps, slot_screwcaps,
     clearance_snapcap, clearance_screwcap, clearance_plate,
     clearance_mix] = get_values(  # noqa: F821
        "adjust_final_vol", "vol_cd154", "vol_peptide1", "vol_peptide2",
        "vol_peptide3", "vol_pma_ca", "vol_culture_medium",
        "labware_cultureplate", "labware_tips", "slot_cultureplate",
        "slot_tipbox", "slot_snapcaps", "slot_screwcaps", "clearance_snapcap",
        "clearance_screwcap", "clearance_plate", "clearance_mix")

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    # p20 single and tips
    tips20 = [ctx.load_labware(
     labware_tips, str(slot)) for slot in [slot_tipbox]]
    p20s = ctx.load_instrument("p20_single_gen2", 'left', tip_racks=tips20)

    # load labware
    culture_plate = ctx.load_labware(
     labware_cultureplate, slot_cultureplate, "Culture Plate")
    rack_snapcaps = ctx.load_labware(
     "opentrons_24_tuberack_nest_1.5ml_snapcap", slot_snapcaps,
     "Rack with Snap Cap Tubes")
    rack_screwcaps = ctx.load_labware(
     "opentrons_24_tuberack_nest_1.5ml_screwcap", slot_screwcaps,
     "Rack with Screw Cap Tubes")

    def pause_attention(message):
        ctx.set_rail_lights(False)
        ctx.delay(seconds=10)
        ctx.pause(message)
        ctx.set_rail_lights(True)

    # extended well class to track liquid vol and height
    class WellH(Well):
        def __init__(self, well, min_height=5, comp_coeff=1.15,
                     current_volume=0):
            super().__init__(well._impl)
            self.well = well
            self.min_height = min_height
            self.comp_coeff = comp_coeff
            self.current_volume = current_volume
            if self.diameter is not None:
                self.radius = self.diameter/2
                cse = math.pi*(self.radius**2)
            elif self.length is not None:
                cse = self.length*self.width
            self.height = round(current_volume/cse)
            if self.height < min_height:
                self.height = min_height
            elif self.height > well.parent.highest_z:
                raise Exception("""Specified liquid volume
                can not exceed the height of the labware.""")

        def height_dec(self, vol):
            if self.diameter is not None:
                cse = math.pi*(self.radius**2)
            elif self.length is not None:
                cse = self.length*self.width
            dh = round((vol/cse)*self.comp_coeff)
            if self.height - dh > self.min_height:
                self.height = self.height - dh
            else:
                self.height = self.min_height
            if self.current_volume - vol > 0:
                self.current_volume = self.current_volume - vol
            else:
                self.current_volume = 0
            return(self.well.bottom(self.height))

        def height_inc(self, vol, top=False):
            if self.diameter is not None:
                cse = math.pi*(self.radius**2)
            elif self.length is not None:
                cse = self.length*self.width
            ih = round((vol/cse)*self.comp_coeff)
            if self.height < self.min_height:
                self.height = self.min_height
            if self.height + ih < self.depth:
                self.height = self.height + ih
            else:
                self.height = self.depth
            self.current_volume += vol
            if top is False:
                return(self.well.bottom(self.height))
            else:
                return(self.well.top())

    # reagents in snapcaps with vol and liquid height tracking
    [peptide1, peptide2, peptide3, pma_ca] = [WellH(
     well, min_height=clearance_snapcap, current_volume=vol
     ) for well, vol in zip([well for row in rack_snapcaps.rows(
     ) for well in row][:4], [
      vol_peptide1, vol_peptide2, vol_peptide3, vol_pma_ca])]

    # reagents in screwcaps with vol and liquid height tracking
    [cd154, culture_medium] = [WellH(
     well, min_height=clearance_screwcap, current_volume=vol
     ) for well, vol in zip([well for row in rack_screwcaps.rows(
     ) for well in row][:2], [vol_cd154, vol_culture_medium])]

    # culture plate wells with vol and liquid height tracking
    plate_wells = [[WellH(well, min_height=clearance_plate, current_volume=vol
                          ) for well, vol in zip([well for well in column], [
                           200, 0, 0, 0, 0])] for column in [column[
                            :5] for column in culture_plate.columns()[:2]]]

    # add anti-CD154 to cell suspension in A1 and A2 and mix
    for column in plate_wells:
        p20s.pick_up_tip()
        p20s.aspirate(5, cd154.height_dec(5))
        p20s.dispense(5, column[0].height_inc(5))
        for rep in range(5):
            p20s.aspirate(
             20, column[0].height_dec(20).move(types.Point(x=0, y=0, z=-(
              column[0].height-column[0].min_height)+clearance_mix)))
            p20s.dispense(20, column[0].height_inc(20))
        p20s.drop_tip()

    # transfer cell suspension to B1-E1 and B2-E2
    for column in plate_wells:
        p20s.pick_up_tip()
        for rep in range(5):
            p20s.aspirate(
             20, column[0].height_dec(20).move(types.Point(x=0, y=0, z=-(
              column[0].height-column[0].min_height)+clearance_mix)))
            p20s.dispense(20, column[0].height_inc(20))
        for well in column[1:]:
            reps = math.ceil(
             float(40) / p20s._tip_racks[0].wells()[0].max_volume)
            vol = 40 / reps
            for rep in range(reps):
                p20s.aspirate(vol, column[0].height_dec(vol))
                p20s.dispense(vol, well.height_inc(vol))
                p20s.touch_tip(radius=0.75, v_offset=-4, speed=20)
        p20s.drop_tip()

    # add reagent (peptides 1, 2 and 3 and PMA) to B1-B2, C1-C2, D1-D2, E1-E2
    for reagent, vol, index in zip(
     [peptide1, peptide2, peptide3, pma_ca], [5, 5, 10, 12], [1, 2, 3, 4]):
        for column in plate_wells:
            p20s.pick_up_tip()
            p20s.aspirate(vol, reagent.height_dec(vol))
            p20s.dispense(vol, column[index].bottom(clearance_plate))
            for rep in range(1):
                p20s.aspirate(20, column[index].bottom(clearance_plate))
                p20s.dispense(20, column[index].bottom(clearance_plate))
            p20s.drop_tip()

    # optionally add 60 uL culture medium to each well
    if adjust_final_vol:
        for column in plate_wells:
            for well in column:
                reps = math.ceil(
                 float(60) / p20s._tip_racks[0].wells()[0].max_volume)
                vol = 60 / reps
                for rep in range(reps):
                    p20s.pick_up_tip()
                    p20s.aspirate(vol, culture_medium.height_dec(vol))
                    p20s.dispense(vol, well.height_inc(vol))
                    p20s.touch_tip(radius=0.75, v_offset=-4, speed=20)
                    p20s.drop_tip()
