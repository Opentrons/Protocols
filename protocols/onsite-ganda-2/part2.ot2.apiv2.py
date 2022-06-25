"""OPENTRONS."""
import math

metadata = {
    'protocolName': 'rhAmpSeq Library Prep Part 1 - PCR 1',
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
    if m20_mount == 'right':
        m300_mount = 'left'
    else:
        m300_mount = 'right'
    num_cols = math.ceil(num_samples/8)
    num_etoh_wells = math.ceil((0.4*num_samples)/15)
    m20_speed_mod = 4
    airgap_library = 5
    # load modules
    mag_module = ctx.load_module('magnetic module gen2', '1')

    # load labware
    sample_plate = mag_module.load_labware('nest_96_wellplate'
                                           '_100ul_pcr_full_skirt')
    reagent_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                     '2')
    reagent_resv = ctx.load_labware('', '3')
    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul',
                                  str(slot))
                 for slot in [4, 5]]
    tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul',
                                   str(slot))
                  for slot in [6, 7, 8, 9, 10, 11]]
    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tiprack300)
    # pipette functions   # INCLUDE ANY BINDING TO CLASS

    # helper functions

    # reagents
    library_mix = reagent_plate.rows()[0][0]
    pcr_forward = reagent_plate.rows()[0][1]
    pcr_reverse = reagent_plate.rows()[0][2]
    beads_1 = reagent_plate.rows()[0][3]
    beads_2 = reagent_plate.rows()[0][4]
    idte = reagent_plate.rows()[0][5]
    # well volume tracking is better solution for this
    etoh_1 = reagent_resv.rows()[0][0]
    etoh_2 = reagent_resv.rows()[0][1]
    etoh_3 = reagent_resv.rows()[0][2]
    etoh_4 = reagent_resv.rows()[0][3]
    liquid_trash_1 = reagent_resv.rows()[0][8]
    liquid_trash_2 = reagent_resv.rows()[0][9]
    liquid_trash_3 = reagent_resv.rows()[0][10]
    liquid_trash_4 = reagent_resv.rows()[0][11]
    # plate, tube rack maps
    sample_dest = sample_plate.rows()[0][:num_cols]
    # protocol
    for dest in sample_dest:
        m20.flow_rate.aspirate /= m20_speed_mod
        m20.flow_rate.dispense /= m20_speed_mod

        m20.flow_rate.aspirate *= m20_speed_mod
        m20.flow_rate.dispense *= m20_speed_mod

    for c in ctx.commands():
        print(c)
