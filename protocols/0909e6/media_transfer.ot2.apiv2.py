from io import StringIO
import csv
import math
from opentrons.protocol_api.labware import Well

metadata = {
    'protocolName': 'Cell Culture',
    'author': 'Nick <ndiehl@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}


def run(ctx):

    [csv_factors, vol_media1, vol_media2, vol_mix] = get_values(  # noqa: F821
        'csv_factors', 'vol_media1', 'vol_media2', 'vol_mix')

    vol_pre_airgap_1000 = 50.0
    vol_pre_airgap_300 = 20.0

    class WellH(Well):
        def __init__(self, well, height=5, min_height=3,
                     comp_coeff=1.15, current_volume=0, min_vol=1000):
            super().__init__(well._impl)
            self.well = well
            self.height = height
            self.min_height = min_height
            self.comp_coeff = comp_coeff
            self.radius = self.diameter/2
            self.current_volume = current_volume
            self.min_vol = min_vol

        def height_dec(self, vol):
            dh = (vol/(math.pi*(self.radius**2)))*self.comp_coeff
            if self.height - dh > self.min_height:
                self.height = self.height - dh
            else:
                self.height = self.min_height
            if self.current_volume - vol > 0:
                self.current_volume = self.current_volume - vol
            else:
                self.current_volume = 0
            return self.well.bottom(self.height)

        def height_inc(self, vol):
            dh = (vol/(math.pi*(self.radius**2)))*self.comp_coeff
            if self.height + dh < self.depth:
                self.height = self.height + dh
            else:
                self.height = self.depth
            self.current_volume += vol
            return self.well.bottom(self.height + 20)

    # labware
    tuberack50 = ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical',
                                  '1', 'media tuberack')
    tuberacks15 = [
        ctx.load_labware('opentrons_15_tuberack_falcon_15ml_conical',
                         slot, f'factor {factor_ids} tuberack')
        for slot, factor_ids in zip(['4', '7'], ['1-15', '16-30'])]
    plate = ctx.load_labware('usascientific_96_wellplate_2.4ml_deep', '2')
    tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '3')]
    tiprack1000 = [
        ctx.load_labware('opentrons_96_filtertiprack_1000ul', slot)
        for slot in ['6']]

    # pipettes
    p300 = ctx.load_instrument('p300_single_gen2', 'left',
                               tip_racks=tiprack300)
    p1000 = ctx.load_instrument('p1000_single_gen2', 'right',
                                tip_racks=tiprack1000)

    # reagents
    media = [
        WellH(well, current_volume=vol, height=well.depth*(vol/50000)*0.9)
        for well, vol in zip(
            tuberack50.rows()[0][:2],
            [vol_media1*1000, vol_media2*1000])]

    # parse data
    f = StringIO(csv_factors)
    reader = csv.reader(f, delimiter=',')
    data = []
    factor_volumes_ml = None
    for i, row in enumerate(reader):
        if i == 1:
            factor_volumes_ml = [float(val) for val in row[1:] if val]
        if i > 1:
            content = [float(val) for val in row if val]
            data.append(content)
    num_factors = len(data[0]) - 1  # exclude media volume

    factor_tubes = [
        well for rack in tuberacks15 for well in rack.wells()][:num_factors]
    factor_heights = [
        # ensure tip is submerged
        round(vol/15*tuberacks15[0].wells()[0].depth*0.9, 1)
        for vol in factor_volumes_ml]
    factors = [
        WellH(well, current_volume=vol*1000, height=height)
        for well, vol, height in zip(
            factor_tubes, factor_volumes_ml, factor_heights)]

    def slow_withdraw(well, pip=p1000):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    def split_media_vol(vol):
        num_transfers = math.ceil(vol/(1000-vol_pre_airgap_1000))
        vol_per_transfer = round(vol/num_transfers, 1)
        return [vol_per_transfer]*num_transfers

    # iterate
    iterator_media = iter(media)
    current_media = next(iterator_media)

    def check_media(vol):
        nonlocal current_media
        if current_media.current_volume - vol < current_media.min_vol:
            current_media = next(iterator_media)

    # transfer media
    p1000.pick_up_tip()
    for well, line in zip(plate.wells(), data):
        vol_media_total = line[0]
        vol_media_split = split_media_vol(vol_media_total)
        for vol in vol_media_split:
            check_media(vol)
            p1000.dispense(p1000.current_volume, current_media.well.top())
            # pre-air_gap to fully void tip on blow_out
            p1000.aspirate(vol_pre_airgap_1000, current_media.well.top())
            p1000.aspirate(vol, current_media.height_dec(vol))
            slow_withdraw(current_media.well, p1000)
            p1000.dispense(p1000.current_volume, well.bottom(2))
            slow_withdraw(well, p1000)
            p1000.blow_out(well.bottom(7))
            p1000.aspirate(50, well.top())  # post-airgap to avoid dripping
    p1000.return_tip()
    p1000.reset_tipracks()

    # transfer factors
    wells_ordered = [well for row in plate.rows() for well in row]
    for i, factor in enumerate(factors):
        for well, line in zip(wells_ordered, data):
            factor_vol = line[1+i]
            if factor_vol > 0:
                if not p300.has_tip:
                    p300.pick_up_tip()
                p300.dispense(p300.current_volume, factor.well.top())
                # pre-air_gap to fully void tip on blow_out
                p300.aspirate(vol_pre_airgap_300, factor.well.top())
                p300.aspirate(factor_vol, factor.height_dec(factor_vol))
                slow_withdraw(factor.well, p300)
                p300.dispense(p300.current_volume, well.top(-2))
                p300.blow_out(well.top(-2))
                p300.aspirate(20, well.top())  # post-airgap to avoid dripping
        if p300.has_tip:
            p300.drop_tip()

    # mix
    for well in plate.wells()[:len(data)]:
        p1000.pick_up_tip()
        p1000.mix(5, vol_mix, well.bottom(2))
        slow_withdraw(well, p1000)
        p1000.drop_tip()
