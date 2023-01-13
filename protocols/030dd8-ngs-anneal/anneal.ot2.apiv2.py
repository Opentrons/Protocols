from opentrons import protocol_api
from opentrons.types import Point
import math

metadata = {
    'protocolName': 'Illumina COVIDSeq - Part 1: Anneal RNA',
    'author': 'Opentrons <protocols@opentrons.com>',
    'apiLevel': '2.13'
}


def run(ctx):

    [num_samples] = get_values(  # noqa: F821
        'num_samples')

    # tuning parameters
    ctx.max_speeds['X'] = 200
    ctx.max_speeds['Y'] = 200

    sample_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '3', 'sample plate')
    cdna_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                  '2', 'cDNA plate')
    reagent_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                     '5', 'reagent plate')
    tips20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot,
                         '200µl filtertiprack')
        for slot in ['7']]

    # load P300M pipette
    m20 = ctx.load_instrument(
        'p20_multi_gen2', 'right', tip_racks=tips20)

    # reagents and variables
    eph3 = reagent_plate.rows()[0][0]

    vol_eph3 = 8.5
    vol_sample = 8.5
    num_cols = math.ceil(num_samples/8)
    ref_well = cdna_plate.wells()[0]
    if ref_well.width:
        radius = ref_well.width/2
    else:
        radius = ref_well.diameter/2

    def wick(pip, well, side=1):
        pip.move_to(well.bottom().move(Point(x=side*radius*0.8, z=3)))

    def slow_withdraw(pip, well):
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    def pick_up(pip, spot=None):
        if spot:
            pip.pick_up_tip(spot)
        else:
            try:
                pip.pick_up_tip()
            except protocol_api.labware.OutOfTipsError:
                ctx.pause("\n\n\n\nReplace 200ul filtertipracks before \
resuming.\n\n\n\n")
                pip.reset_tipracks()
                pip.pick_up_tip()

    pick_up(m20)
    for d in cdna_plate.rows()[0][:num_cols]:
        m20.aspirate(vol_eph3, eph3.bottom(0.5))
        slow_withdraw(m20, eph3)
        m20.dispense(vol_eph3, d.bottom(0.5))
        wick(m20, d)

    for s, d in zip(cdna_plate.rows()[0][:num_cols],
                    sample_plate.rows()[0][:num_cols]):
        if not m20.has_tip:
            pick_up(m20)
        m20.aspirate(vol_sample, s.bottom(0.5))
        slow_withdraw(m20, s)
        m20.dispense(vol_sample, d.bottom(2))
        wick(m20, d)
        m20.drop_tip()

    ctx.comment('\n\n\n\nProtocol complete.\nSeal and shake at 1600 rpm for 1 \
minute.\nCentrifuge at 1000 × g for 1 minute.\nPlace on the preprogrammed \
thermal cycler and run the COVIDSeq FSS program.\n\n\n\n')
