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
        for slot in ['4', '5', '7', '8']]
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '6', 'reservoir')
    oligo_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 'oligos')

    # pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', mount_m20,
                              tip_racks=tipracks20)
    p20 = ctx.load_instrument('p20_single_gen2', mount_p20,
                              tip_racks=tipracks20)

    # reagents
    oligos = oligo_plate.rows()[0][:3]

    def wick(well, pip, side=1):
        pip.move_to(well.bottom().move(Point(x=side*well.diameter/2*0.8, z=3)))

    def slow_withdraw(well, pip):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    