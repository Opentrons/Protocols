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

    [csv_factors] = get_values(  # noqa: F821
        'csv_factors')

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
            return(self.well.bottom(self.height))

        def height_inc(self, vol):
            dh = (vol/(math.pi*(self.radius**2)))*self.comp_coeff
            if self.height + dh < self.depth:
                self.height = self.height + dh
            else:
                self.height = self.depth
            self.current_volume += vol
            return(self.well.bottom(self.height + 20))

    # labware
    tuberack50 = ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical',
                                  '1', 'media tuberack')
    tuberack15 = ctx.load_labware('opentrons_15_tuberack_falcon_15ml_conical',
                                  '4', 'factor tuberack')
    plate = ctx.load_labware('usascientific_96_wellplate_2.4ml_deep', '2')
    tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '3')]
    tiprack1000 = [ctx.load_labware('opentrons_96_filtertiprack_1000ul', '6')]

    # pipettes
    p300 = ctx.load_instrument('p300_single_gen2', 'left',
                               tip_racks=tiprack300)
    p1000 = ctx.load_instrument('p1000_single_gen2', 'right',
                                tip_racks=tiprack1000)

    # reagents
    media = [
        WellH(well, current_volume=48000, height=well.depth*0.9)
        for well in tuberack50.rows()[0]]

    # parse data
    f = StringIO(csv_factors)
    reader = csv.reader(f, delimiter=',')
    data = []
    for i, row in enumerate(reader):
        if i > 1:
            content = [float(val) for val in row[2:] if val]
            data.append(content)
    num_factors = len(data[0]) - 3  # exclude total volume, media volume
    factors = tuberack15.wells()[:num_factors]

    def slow_withdraw(well, pip=p1000):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    def split_media_vol(vol):
        num_transfers = math.ceil(vol/1000)
        vol_per_transfer = round(vol/num_transfers, 1)
        return [vol_per_transfer]*num_transfers

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
            p1000.aspirate(vol, current_media.height_dec(vol))
            slow_withdraw(current_media, p1000)
            p1000.dispense(vol, well.bottom(2))
            slow_withdraw(well, p1000)

    # transfer factors
    for i, factor in enumerate(factors):
        p300.pick_up_tip()
        for well, line in zip(plate.wells(), data):
            factor_vol = line[3+i]
            if factor_vol > 0:
                p300.aspirate(factor_vol, factor.bottom(1.5))
                slow_withdraw(factor, p300)
                p300.dispense(factor_vol, well.top(-2))
        p300.drop_tip()

    # mix
    for well in plate.wells()[:len(data)]:
        if not p1000.has_tip:
            p1000.pick_up_tip()
        p1000.mix(5, 800, well.bottom(2))
        slow_withdraw(well, p1000)
        p1000.drop_tip()
