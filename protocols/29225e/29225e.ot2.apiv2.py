from types import MethodType
from opentrons.protocol_api.labware import Well, OutOfTipsError
import csv
import math

metadata = {
    'title': 'RNA Normalization',
    'author': 'Steve Plonk',
    'apiLevel': '2.10'
}


def run(ctx):

    [mix_rate, clearance_rna, clearance_dest, labware_rna, labware_dest,
     vol_h2o, uploaded_csv] = get_values(  # noqa: F821
        "mix_rate", "clearance_rna", "clearance_dest", "labware_rna",
        "labware_dest", "vol_h2o", "uploaded_csv")

    ctx.set_rail_lights(True)
    ctx.delay(seconds=10)

    if not 500 <= vol_h2o <= 1500:
        raise Exception(
         'Starting volume of water must be between 500 and 1500 uL per tube.')

    if not 1 <= mix_rate <= 3:
        raise Exception(
         'p20 flow rate for mix must be 1 and 3 times the default rate.')

    if not clearance_rna >= 1:
        raise Exception(
         'Well bottom clearance must be 1 mm or greater.')

    if not clearance_dest >= 1:
        raise Exception(
         'Well bottom clearance must be 1 mm or greater.')

    # ignore lines that are missing both water vol and source vol
    tfers = [line for line in csv.DictReader(
     uploaded_csv.splitlines()) if (line['water vol'] or line['source vol'])]

    # handle missing water vol as 0 uL
    for tfer in tfers:
        if not tfer['water vol']:
            tfer['water vol'] = 0

    sample_count = len(tfers)
    if not 1 <= sample_count <= 96:
        raise Exception('Invalid number of samples (must be 1-96).')

    # p300 single, p20 single, tips
    tips20 = [ctx.load_labware(
     'opentrons_96_filtertiprack_20ul', str(slot)) for slot in [10]]
    tips300 = [ctx.load_labware(
     'opentrons_96_filtertiprack_200ul', str(slot)) for slot in [11]]
    p20s = ctx.load_instrument("p20_single_gen2", 'left', tip_racks=tips20)
    p300s = ctx.load_instrument("p300_single_gen2", 'right', tip_racks=tips300)

    # count unique values in csv, load input RNA lbwr instances
    rna = [
     ctx.load_labware(labware_rna, slot, "Input RNA Samples") for slot in [
      2, 3, 5, 6][:len(set([tfer['source rack or plate'] for tfer in tfers]))]]

    # water tubes with volume and liquid height tracking
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

    water_tubes = []
    num_tubes = math.ceil(sum([float(
     tfer['water vol']) for tfer in tfers]) / vol_h2o)
    for index, tube in enumerate(rack.wells()[:num_tubes]):
        new = WellH(rack.wells()[index], min_height=1, current_volume=vol_h2o)
        water_tubes.append(new)

    ctx.pause(
     "Please place {0} tubes each containing {1} uL water in {2}".format(
      num_tubes, vol_h2o, rack))

    def wtr_tubes():
        yield from water_tubes

    water_tube = wtr_tubes()

    water = next(water_tube)

    def distribute_water(pip, lst, disposal):
        nonlocal water
        if lst != []:
            disp = []
            in_tip = 0
            pip.pick_up_tip()
            pip.aspirate(disposal, water.height_dec(disposal))
            in_tip += disposal
            for index, tfer in enumerate(lst):
                vol = float(tfer['water vol'])
                dst = dest_plate.wells_by_name()[tfer['dest well']]
                if water.current_volume <= 50:
                    try:
                        water = next(water_tube)
                    except StopIteration:
                        ctx.comment("The next water tube was not found.")
                if vol + in_tip > pip._tip_racks[0].wells()[0].max_volume:
                    for d in disp:
                        pip.dispense(float(d[0]), d[1].bottom(clearance_dest))
                    disp = []
                    pip.dispense(disposal, water.height_inc(disposal))
                    in_tip = 0
                    pip.aspirate(disposal, water.height_dec(disposal))
                    in_tip += disposal
                pip.aspirate(vol, water.height_dec(vol))
                in_tip += vol
                disp.append((vol, dst))
                if index == len(lst)-1:
                    for d in disp:
                        pip.dispense(float(d[0]), d[1].bottom(clearance_dest))
            pip.drop_tip()

    def pick_up_or_refill(self):
        try:
            self.pick_up_tip()
        except OutOfTipsError:
            pause_attention(
             """Please Refill the {} Tip Boxes
                and Empty the Tip Waste.""".format(self))
            self.reset_tipracks()
            self.pick_up_tip()

    def pause_attention(message):
        ctx.set_rail_lights(False)
        ctx.delay(seconds=10)
        ctx.pause(message)
        ctx.set_rail_lights(True)

    for pipette_object in [p20s, p300s]:
        for method in [pick_up_or_refill]:
            setattr(
             pipette_object, method.__name__,
             MethodType(method, pipette_object))

    # 4 degree temp module with dest plate
    temp = ctx.load_module('temperature module gen2', '1')
    dest_plate = temp.load_labware(
     labware_dest, "Destination Plate at 4 Degrees")
    temp.set_temperature(4)

    # transfer water
    small_tfers = []
    big_tfers = []
    for tfer in tfers:
        vol = float(tfer['water vol'])
        if 0 < vol <= 10:
            small_tfers.append(tfer)
        elif vol > 10:
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
        pip.pick_up_or_refill()
        pip.aspirate(
         vol, rna[int(tfer['source rack or plate'])-1].wells_by_name(
         )[tfer['source well']].bottom(clearance_rna))
        pip.dispense(vol, dest_plate.wells_by_name()[
         tfer['dest well']].bottom(clearance_dest))
        rt = mix_rate if pip == p20s else 1
        pip.mix(6, 20, rate=rt)
        pip.drop_tip()

    for tfer in tfers:
        vol = float(tfer['water vol']) + float(tfer['source vol'])
        if vol > 50:
            p300s.pick_up_or_refill()
            p300s.mix(4, 0.8*vol, dest_plate.wells_by_name()[
             tfer['dest well']].bottom(2))
            p300s.drop_tip()
