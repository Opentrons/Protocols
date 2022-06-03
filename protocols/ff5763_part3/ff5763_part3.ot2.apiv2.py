"""OPENTRONS."""
import math
from opentrons import types

metadata = {
    'protocolName': 'Illumina DNA Prep, Amplify Tagmented DNA',
    'author': 'John C. Lynch <john.lynch@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx):
    """PROTOCOL."""
    [
     num_samples
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples")

    # define all custom variables above here with descriptions:

    # number of samples
    num_cols = math.ceil(num_samples/8)

    # load modules/labware
    """SAMPLE PLATE ON MAG MODULE"""
    temp_1 = ctx.load_module('tempdeck', '1')
    cycler_plate = ctx.load_labware('customabnest_96_wellplate_200ul', '2')
    thermo_tubes = temp_1.load_labware('opentrons_96_aluminumblock_generic_'
                                       'pcr_strip_200ul')
    mag_module = ctx.load_module('magnetic module gen2', '4')
    sample_plate = mag_module.load_labware('nest_96_wellplate_2ml_deep')
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '5')
    liquid_trash = ctx.load_labware('nest_1_reservoir_195ml', '6')

    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['7', '8']]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                  for slot in ['9', '10']]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2', 'left', tip_racks=tiprack200)

    # reagents
    '''includes reagents used in other steps for housekeeping purposes'''
    # master_mix = thermo_tubes.rows()[0][0]
    # nf_water = thermo_tubes.rows()[0][1]
    tsb = thermo_tubes.rows()[0][2]
    sample_dest = sample_plate.rows()[0][:num_cols]
    pcr_mix = reagent_resv.wells()[0]
    index_adapters = reagent_resv.wells()[0]
    # can reuse other half of plate from previous step!
    cycler_dest = cycler_plate.rows()[0][6:6+num_cols]
    # Constants

    # hard code variables
    vol_supernatant = 110
    supernatant_headspeed_modulator = 5
    airgap_index = 5
    airgap_mastermix = 10
    airgap_plate = 10

    # keeps temp module loaded
    m300.move_to(tsb.top(3))

    # Discard supernatant
    ctx.comment('''discarding supernatant''')
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source in sample_dest:
        side = 1 if num_times % 2 == 0 else -1
        m300.pick_up_tip()
        m300.flow_rate.aspirate /= 5
        m300.move_to(source.top())
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.aspirate(
            vol_supernatant, source.bottom().move(types.Point(x=side,
                                                              y=0, z=0.5)))
        m300.move_to(source.top())
        m300.flow_rate.aspirate *= 5
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.dispense(vol_supernatant, liquid_trash.wells()[0])
        m300.drop_tip()
        num_times += 1
        print(side)
    mag_module.disengage()

    # Add 40ul Master mix (EFW and NFW made off-deck w/10% overage), mix 10x
    for dest in sample_dest:
        m300.pick_up_tip()
        m300.flow_rate.aspirate /= 5
        m300.flow_rate.dispense /= 5
        m300.aspirate(40, pcr_mix)
        m300.move_to(pcr_mix.top())
        m300.aspirate(airgap_mastermix, pcr_mix.top())
        m300.dispense(airgap_mastermix, dest.top())
        m300.dispense(40, dest)
        m300.flow_rate.aspirate *= 5
        m300.flow_rate.dispense *= 5
        m300.mix(10, 40)
        m300.drop_tip()

    # Move samples to thermocycler plate for centrifuge
    for source, dest in zip(sample_dest, cycler_dest):
        m300.pick_up_tip()
        m300.flow_rate.aspirate /= 5
        m300.flow_rate.dispense /= 5
        m300.aspirate(60, source)
        m300.move_to(source.top())
        m300.aspirate(airgap_plate, source.top())
        m300.move_to(dest.top())
        m300.dispense(airgap_plate, dest.top())
        m300.dispense(60, dest)
        m300.flow_rate.aspirate *= 5
        m300.flow_rate.dispense *= 5
        m300.drop_tip()

    # centrifuge off deck, 280 x g for 3 seconds
    ctx.pause('Please centrifuge plate in slot 2 at 280 x g for 3 seconds,'
              ' return to slot 2 when done')

    # Add 10ul index adapters (made offdeck or supplied in 96 well plate)
    for dest in cycler_dest:
        m20.pick_up_tip()
        m20.flow_rate.aspirate /= 4
        m20.flow_rate.dispense /= 4
        m20.aspirate(10, index_adapters)
        m20.move_to(index_adapters.top(-2))
        m20.aspirate(airgap_index, index_adapters.top(-2))
        m20.move_to(index_adapters.top(-2))
        m20.dispense(airgap_index, dest.top())
        m20.dispense(10, dest)
        m20.flow_rate.aspirate *= 4
        m20.flow_rate.dispense *= 4
        m20.drop_tip()
    # mix 10x at 40ul
    for dest in cycler_dest:
        m300.pick_up_tip()
        m300.flow_rate.aspirate /= 3
        m300.flow_rate.dispense /= 3
        m300.mix(10, 40, dest)
        m300.flow_rate.aspirate *= 3
        m300.flow_rate.dispense *= 3
        m300.drop_tip()

    # Move to off-deck thermo cycler
    ctx.pause('Run complete, please move sample plate to off-deck thermocycler'
              )
    for c in ctx.commands():
        print(c)
