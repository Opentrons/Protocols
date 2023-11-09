import math
from opentrons.protocol_api.labware import Well
from opentrons.protocols.api_support.types import APIVersion
from opentrons.types import Point

metadata = {
    'protocolName': 'DOE',
    'author': 'Nick <ndiehl@opentrons.com',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}


def run(ctx):

    [csv_factors, vol_media_tubes, vol_mix,
     reps_mix, type_pipette_small] = get_values(  # noqa: F821
        'csv_factors', 'vol_media_tubes', 'vol_mix', 'reps_mix',
        'type_pipette_small')

    vol_pre_airgap_1000 = 100.0
    if type_pipette_small == 'p300_single_gen2':
        vol_pre_airgap_small = 30.0
        tiprack_small_type = 'opentrons_96_filtertiprack_200ul'
    else:
        vol_pre_airgap_small = 10.0
        tiprack_small_type = 'opentrons_96_filtertiprack_20ul'

    class WellH(Well):
        def __init__(self, well, height=5, min_height=2.5,
                     comp_coeff=1.15, current_volume=0, min_vol=1000):
            try:
                super().__init__(well.parent, well._core, APIVersion(2, 13))
            except AttributeError:
                super().__init__(well._impl)
            self.well = well
            self.height = height
            self.min_height = min_height
            self.comp_coeff = comp_coeff
            self.radius = self.diameter/2 if self.diameter else self.width/2
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
        ctx.load_labware(
            'opentrons_15_tuberack_falcon_15ml_conical', slot,
            f'factors {tube_set}')
        for i, (slot, tube_set) in enumerate(
            zip(['4', '7'], ['1-15', '16-30']))]
    tuberacks2 = [
        ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', slot,
            f'factors {tube_set}')
        for i, (slot, tube_set) in enumerate(
            zip(['5', '8'], ['31-54', '55-78']))]
    plate = ctx.load_labware('usascientific_96_wellplate_2.4ml_deep', '2')
    tiprack_small = [ctx.load_labware(tiprack_small_type, '3')]
    tiprack1000 = [
        ctx.load_labware('opentrons_96_filtertiprack_1000ul', slot)
        for slot in ['6']]

    # pipettes
    pip_small = ctx.load_instrument(type_pipette_small, 'left',
                                    tip_racks=tiprack_small)
    p1000 = ctx.load_instrument('p1000_single_gen2', 'right',
                                tip_racks=tiprack1000)

    # reagents
    vol_media_list = [float(val) for val in vol_media_tubes.split(',')]
    media_rows_ordered = [tube for row in tuberack50.rows() for tube in row]
    media = [
        WellH(well, current_volume=vol, height=well.depth*(vol/50000)*0.9)
        for well, vol in zip(
            media_rows_ordered[:len(vol_media_list)],
            [vol_media_tube*1000 for vol_media_tube in vol_media_list])]

    # parse data
    factor_data = [
        [float(val) for val in line.split(',')[1:] if val.strip()]
        for line in csv_factors.splitlines()[3:]
    ]

    all_factor_tubes = [
        well for rack_set in [tuberacks15, tuberacks2]
        for rack in rack_set
        for well in rack.wells()]

    factor_indices = [
        int(cell.strip().split(' ')[-1]) - 1
        for cell in csv_factors.splitlines()[0].split(',')[1:]
        if cell.strip()]
    factor_tubes = [
        all_factor_tubes[ind] for ind in factor_indices]
    factor_viscosities = [
        bool(visc) for visc in csv_factors.splitlines()[1].split(',')[1:]
        if visc.strip()]
    factor_volumes_ul = [
        float(cell)*1000 for cell in csv_factors.splitlines()[2].split(',')[1:]
        if cell.strip()]
    # ref_vol = tuberacks15[0].wells()[0].max_volume / 1000  # 2ml or 15ml
    # ref_height = tuberacks15[0].wells()[0].depth
    factor_heights = [
        # ensure tip is submerged
        round(factor_vol/(factor_tube.max_volume)*factor_tube.depth*0.9,
              1)
        for factor_tube, factor_vol in zip(factor_tubes, factor_volumes_ul)]
    factors = [
        WellH(well, current_volume=vol, height=height)
        for well, vol, height in zip(
            factor_tubes, factor_volumes_ul, factor_heights)]

    def slow_withdraw(well, pip=p1000, delay_s=2.0):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        if delay_s > 0:
            ctx.delay(seconds=delay_s)
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

    def custom_distribute(info, pip):
        pip_volume = pip.tip_racks[0].wells()[0].max_volume
        vol_pre_airgap = vol_pre_airgap_small if pip == \
            pip_small else vol_pre_airgap_1000
        max_vol = pip_volume
        sets = []
        running = []
        current_vol = 0
        for d in info:
            well = [key for key in d.keys()][0]
            vol = [val for val in d.values()][0]
            if vol > 0:
                if current_vol + vol + vol_pre_airgap > max_vol:
                    sets.append(running)
                    running = []
                    current_vol = 0
                running.append({well: vol})
                current_vol += vol + vol_pre_airgap
        sets.append(running)
        return sets

    # transfer media
    p1000.pick_up_tip()
    wells_ordered = [well for row in plate.rows() for well in row]
    vols_media = [
        float(line.split(',')[0]) for line in csv_factors.splitlines()[3:]]
    media_info = []
    for well, vol_media in zip(wells_ordered, vols_media):
        vols_split = split_media_vol(vol_media)
        for vol in vols_split:
            media_info.append({well: vol})

    wells_h = [
        WellH(well, height=0) for well in wells_ordered]

    for d in media_info:
        well = list(d.keys())[0]
        asp_vol = list(d.values())[0]
        if p1000.current_volume:
            p1000.dispense(p1000.current_volume, current_media.well.top())
        check_media(asp_vol)
        p1000.aspirate(vol_pre_airgap_1000, current_media.well.top())
        p1000.aspirate(asp_vol, current_media.height_dec(asp_vol))
        slow_withdraw(current_media.well, p1000)
        p1000.dispense(p1000.current_volume, well.bottom(well.depth/2))
        p1000.blow_out(well.bottom(well.depth/2))
        slow_withdraw(well, p1000)

    # media_sets = custom_distribute(media_info, pip=p1000)
    # for media_set in media_sets:
    #     if p1000.current_volume:
    #         p1000.dispense(p1000.current_volume, current_media.well.top())
    #     # pre-air_gap to fully void tip on blow_out
    #     for d in media_set:
    #         asp_vol = sum(d.values())
    #         check_media(asp_vol)
    #         p1000.aspirate(vol_pre_airgap_1000, current_media.well.top())
    #         p1000.aspirate(asp_vol, current_media.height_dec(asp_vol))
    #     slow_withdraw(current_media.well, p1000)
    #     for i, d in enumerate(media_set):
    #         well = [key for key in d.keys()][0]
    #         vol = [val for val in d.values()][0]
    #         p1000.dispense(vol+vol_pre_airgap_1000,
    #                        well.bottom(well.depth/2))
    #         if i == len(media_set) - 1:
    #             p1000.blow_out(well.bottom(well.depth/2))
    #         slow_withdraw(well, p1000)
    p1000.return_tip()
    p1000.reset_tipracks()

    viscosity_map = {
        20: {
            'aspirate': 6.5,
            'delay_aspiration': 2.0,
            'dispense': 6.5,
            'delay_dispense': 2.0,
            'default': 7.56
        },
        300: {
            'aspirate': 80,
            'delay_aspiration': 2.0,
            'dispense': 80,
            'delay_dispense': 2.0,
            'default': 92.86
        },
        1000: {
            'aspirate': 247,
            'delay_aspiration': 2.0,
            'dispense': 247,
            'delay_dispense': 2.0,
            'default': 247
        }
    }

    # transfer factors
    for i, (visc, factor) in enumerate(zip(factor_viscosities, factors)):
        factor_vols = [line[i] for line in factor_data]
        factor_info = [
            {well: vol}
            for well, vol in zip(wells_h, factor_vols)]
        factor_sets = custom_distribute(factor_info, pip=pip_small)
        if visc:
            asp_rate_relative = viscosity_map[
                int(pip_small.max_volume)]['aspirate'] / (
                    viscosity_map[int(pip_small.max_volume)]['default'])
            asp_delay = viscosity_map[
                int(pip_small.max_volume)]['delay_aspiration']
            disp_rate_relative = viscosity_map[
                int(pip_small.max_volume)]['dispense'] / (
                    viscosity_map[int(pip_small.max_volume)]['default'])
            disp_delay = viscosity_map[
                int(pip_small.max_volume)]['delay_dispense']
        else:
            asp_rate_relative = 1
            asp_delay = 2.0
            disp_rate_relative = 1
            disp_delay = 2.0
        for factor_set in factor_sets:
            # aspirate total vol needed
            if not pip_small.has_tip:
                pip_small.pick_up_tip()
            # pre-air_gap to fully void tip on blow_out
            for d in factor_set:
                well = [k for k in d.keys()][0]
                asp_vol = [k for k in d.values()][0]
                if asp_vol + vol_pre_airgap_small <= pip_small.max_volume:
                    ag_vol = vol_pre_airgap_small
                else:
                    ag_vol = pip_small.max_volume - asp_vol
                pip_small.aspirate(ag_vol, factor.well.top())
                pip_small.aspirate(
                    asp_vol, factor.height_dec(asp_vol),
                    rate=asp_rate_relative)
                slow_withdraw(factor.well, pip_small, delay_s=asp_delay)
                pip_small.dispense(
                    pip_small.current_volume,
                    well.height_inc(asp_vol).move(Point(z=3)),
                    rate=disp_rate_relative)
                ctx.delay(seconds=disp_delay)
                pip_small.blow_out(well.top(-2))

            # total_factor_vol = sum([sum(dict.values()) for dict in
            # factor_set])
            # p300.aspirate(total_factor_vol,
            #               factor.height_dec(total_factor_vol))
            # for i, dict in enumerate(factor_set):
            #     for well, vol in dict.items():
            #         pip_small.dispense(
            #             vol+vol_pre_airgap_small, well.bottom(well.depth/2))
            #     if i == len(factor_set) - 1:
            #         pip_small.blow_out(well.top(-2))

            # for d in factor_set:
            #     asp_vol = sum(d.values())
            #     if asp_vol + vol_pre_airgap_small <= pip_small.max_volume:
            #         ag_vol = vol_pre_airgap_small
            #     else:
            #         ag_vol = pip_small.max_volume - asp_vol
            #     pip_small.aspirate(ag_vol, factor.well.top())
            #     pip_small.aspirate(asp_vol, factor.height_dec(asp_vol))
            # # total_factor_vol = sum([sum(dict.values()) for dict in
            # # factor_set])
            # # p300.aspirate(total_factor_vol,
            # #               factor.height_dec(total_factor_vol))
            # slow_withdraw(factor.well, pip_small)
            # for i, dict in enumerate(factor_set):
            #     for well, vol in dict.items():
            #         pip_small.dispense(
            #             vol+vol_pre_airgap_small, well.bottom(well.depth/2))
            #     if i == len(factor_set) - 1:
            #         pip_small.blow_out(well.top(-2))
        if pip_small.has_tip:
            pip_small.drop_tip()

    # mix
    for well in plate.wells()[:len(factor_data)]:
        p1000.pick_up_tip()
        p1000.mix(reps_mix, vol_mix, well.bottom(2))
        slow_withdraw(well, p1000)
        p1000.drop_tip()
