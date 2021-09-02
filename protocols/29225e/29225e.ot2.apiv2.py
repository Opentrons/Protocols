from opentrons.protocol_api.labware import Well
import csv
import math

metadata = {
    'title': 'RNA Normalization',
    'author': 'Steve Plonk',
    'apiLevel': '2.10'
}


def run(ctx):

    [clearance_rna, clearance_dest, labware_rna, labware_dest, vol_h2o,
     uploaded_csv] = get_values(  # noqa: F821
        "clearance_rna", "clearance_dest", "labware_rna", "labware_dest",
        "vol_h2o", "uploaded_csv")

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    if not 500 <= vol_h2o <= 1500:
        raise Exception(
         'Starting volume of water must be between 500 and 1500 uL.')

    tfers = [line for line in csv.DictReader(uploaded_csv.splitlines())]

    sample_count = len(tfers)
    if not 1 <= sample_count <= 96:
        raise Exception('Invalid number of samples (must be 1-96).')

    # p300 single, p20 single, tips
    tips20 = [ctx.load_labware(
     'opentrons_96_tiprack_20ul', str(slot)) for slot in [10]]
    tips300 = [ctx.load_labware(
     'opentrons_96_tiprack_300ul', str(slot)) for slot in [11]]
    p20s = ctx.load_instrument("p20_single_gen2", 'left', tip_racks=tips20)
    p300s = ctx.load_instrument("p300_single_gen2", 'right', tip_racks=tips300)

    # input RNA samples
    if labware_rna == "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap":
        rna = [ctx.load_labware(labware_rna, slot, "Input RNA Tube Rack")
               for slot in [2, 3, 5, 6][:math.ceil(sample_count / 24)]]
    elif labware_rna == "nest_96_wellplate_2ml_deep":
        rna = ctx.load_labware(labware_rna, '2', "Input RNA Plate")
    else:
        raise Exception(
         'Adjustments to the protocol are needed for this labware.')

    # water tube with tracking of volume and liquid height
    rack = ctx.load_labware(
     'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
     '4', 'Reagent Rack')

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

    water = WellH(rack.wells()[0], min_height=1, current_volume=vol_h2o)

    def distribute_water(pip, lst, disposal):
        if lst != []:
            disp = []
            in_tip = 0
            pip.pick_up_tip()
            for index, tfer in enumerate(lst):
                vol = float(tfer['water vol'])
                dst = dest_plate.wells_by_name()[tfer['dest well']]
                if vol + in_tip <= pip.max_volume:
                    pip.aspirate(vol, water.height_dec(vol))
                    in_tip += vol
                    disp.append((vol, dst))
                else:
                    for d in disp:
                        pip.dispense(float(d[0]), d[1].bottom(clearance_dest))
                    disp = []
                    pip.dispense(disposal, water.height_inc(disposal))
                    in_tip = 0
                    pip.aspirate(disposal, water.height_dec(disposal))
                    in_tip += disposal
            pip.drop_tip()

    # 4 degree temperature module with destination plate
    temp = ctx.load_module('temperature module gen2', '1')
    dest_plate = temp.load_labware(
     labware_dest, "Destination Plate at 4 Degrees")
    temp.set_temperature(4)

    # transfer water
    small_tfers = []
    big_tfers = []
    for tfer in tfers:
        vol = float(tfer['water vol'])
        if vol <= 10:
            small_tfers.append(tfer)
        else:
            big_tfers.append(tfer)

    distribute_water(p20s, small_tfers, 2)

    distribute_water(p300s, big_tfers, 15)

    # transfer RNA and mix
    for tfer in tfers:
        vol = float(tfer['source vol'])
        if vol <= 20:
            pip = p20s
        else:
            pip = p300s
        pip.transfer(
         vol, rna[int(tfer['source rack or plate'])-1].wells_by_name(
         )[tfer['source well']].bottom(clearance_rna),
         dest_plate.wells_by_name(
          )[tfer['dest well']].bottom(clearance_dest),
         mix_after=(6, 20), new_tip='always')
