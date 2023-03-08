import math
from opentrons.types import Point

metadata = {
    'protocolName': 'Reaction Library Screening',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}


def run(ctx):

    [num_samples, mount_m20, mount_p20] = get_values(  # noqa: F821
        'num_samples', 'mount_m20', 'mount_p20')

    mix_reps_oligo = 5
    mix_vol_oligo = 5.0
    vol_pcr_reagent = 30.0
    mix_reps_pcr_reagent = 5
    mix_vol_pcr_reagent = 20.0

    # modules and labware
    hs = ctx.load_module('heaterShakerModuleV1', '1')
    hs_plate = hs.load_labware(
        'opentrons_96_deep_well_adapter_nest_wellplate_2ml_deep')
    azides_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '3',
                                    'azides')
    tipracks20 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['10', '7']]
    tipracks300 = [
        ctx.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['11', '8']]
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '6', 'reservoir')
    oligo_plate = ctx.load_labware('roarprinted_48_wellplate_1500ul', 'oligos')

    # pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', mount_m20,
                              tip_racks=tipracks20)
    m300 = ctx.load_instrument('p300_single_gen2', mount_p20,
                               tip_racks=tipracks300)

    # reagents
    num_cols = math.ceil(num_samples/6)
    oligos = oligo_plate.rows()[0][:3]
    [teaa, h2o, dmso, sodium_abscorbate, cu_ligand] = reservoir.rows()[:5]

    default_current = 0.6
    offset_pickup_columns = m20.tip_racks[-1].columns()[::-1]
    offset_column_counter = 0

    def pick_up_offset(num_tips, pip=m20):
        nonlocal offset_column_counter

        current_modifier = num_tips/8
        current = default_current*current_modifier
        ctx._hw_manager.hardware._attached_instruments[
            pip._implementation.get_mount()
            ].update_config_item('pick_up_current', current)

        col = offset_pickup_columns[offset_column_counter]
        offset_column_counter += 1
        pick_up_well = col[8-num_tips]

        m20.pick_up_tip(pick_up_well)

        # reset current to default
        ctx._hw_manager.hardware._attached_instruments[
            pip._implementation.get_mount()
            ].update_config_item('pick_up_current', default_current)

    def wick(well, pip, side=1):
        pip.move_to(well.bottom().move(Point(x=side*well.diameter/2*0.8, z=3)))

    def slow_withdraw(well, pip):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    # transfer reagents to oligo plate 