"""OPENTRONS."""
import math

metadata = {
    'protocolName': 'rhAmpSeq Library Prep Part 1 - PCR Prep 1',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}


def run(ctx):
    """PROTOCOL."""
    [
     num_samples, m20_mount
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples", "m20_mount")

    # define all custom variables above here with descriptions:

    num_cols = math.ceil(num_samples/8)
    m20_speed_mod = 4
    # airgap_library = 5
    # load modules
    mag_module = ctx.load_module('magnetic module gen2', '1')

    # load labware
    sample_plate = mag_module.load_labware('nest_96_wellplate'
                                           '_100ul_pcr_full_skirt')
    reagent_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                     '2')
    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul',
                                  str(slot))
                 for slot in [3, 5, 6][:math.ceil(num_samples/32)]]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tiprack20)

    # pipette functions   # INCLUDE ANY BINDING TO CLASS

    # helper functions

    # reagents
    library_mix = reagent_plate.rows()[0][0]
    pcr_forward = reagent_plate.rows()[0][1]
    pcr_reverse = reagent_plate.rows()[0][2]
    # plate, tube rack maps
    sample_dest = sample_plate.rows()[0][:num_cols]
    # protocol

    # add library mix, 5 uL
    for dest in sample_dest:
        m20.flow_rate.aspirate /= m20_speed_mod
        m20.flow_rate.dispense /= m20_speed_mod
        m20.pick_up_tip()
        m20.aspirate(5, library_mix)
        m20.move_to(library_mix.top(-2))
        ctx.delay(seconds=2)
        # m20.touch_tip(v_offset=-2)
        # m20.move_to(library_mix.top(-2))
        # m20.aspirate(airgap_library, library_mix.top())
        # m20.dispense(airgap_library, dest.top())
        m20.dispense(5, dest)
        m20.mix(1, 5, dest)
        ctx.max_speeds['A'] = 100
        ctx.max_speeds['Z'] = 100
        m20.drop_tip()
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']
        m20.flow_rate.aspirate *= m20_speed_mod
        m20.flow_rate.dispense *= m20_speed_mod
    # add forward, reverse primers, 2 uL each
    for reagent_source in [pcr_forward, pcr_reverse]:
        for dest in sample_dest:
            m20.flow_rate.aspirate /= m20_speed_mod
            m20.flow_rate.dispense /= m20_speed_mod
            m20.pick_up_tip()
            m20.aspirate(2, reagent_source)
            m20.move_to(reagent_source.top(-2))
            ctx.delay(seconds=2)
            # m20.touch_tip(v_offset=-2)
            # m20.move_to(reagent_source.top(-2))
            # m20.aspirate(airgap_library, reagent_source.top())
            # m20.dispense(airgap_library, dest.top())
            m20.dispense(2, dest)
            m20.mix(1, 5, dest)
            ctx.max_speeds['A'] = 100
            ctx.max_speeds['Z'] = 100
            m20.drop_tip()
            del ctx.max_speeds['A']
            del ctx.max_speeds['Z']
            m20.flow_rate.aspirate *= m20_speed_mod
            m20.flow_rate.dispense *= m20_speed_mod
