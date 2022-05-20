"""OPENTRONS"""
import math

metadata = {
    'protocolName': 'Protocol Title',
    'author': 'AUTHOR NAME <authoremail@company.com>',
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

    # "True" for park tips, "False" for discard tips

    # load modules/labware
    """Step 2 has the sample plate on the mag module in slot 4!"""
    temp_1 = ctx.load_module('tempdeck', '1')
    thermo_tubes = temp_1.load_labware('opentrons_96_aluminumblock_generic_pcr'
                                       '_strip_200ul')
    mag_module = ctx.load_module('magnetic module gen2', '4')
    sample_plate = mag_module.load_labware('nest_96_wellplate_100ul_pcr'
                                           '_full_skirt')
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '5')
    liquid_trash = ctx.load_labware('nest_1_reservoir_195ml', '9')

    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['3']]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                  for slot in ['6']]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2', 'left', tip_racks=tiprack200)

    # reagents
    '''includes reagents used in other steps for housekeeping purposes'''
    master_mix = thermo_tubes.rows()[0][0]
    nf_water = thermo_tubes.rows()[0][1]
    tsb = thermo_tubes.rows()[0][2]
    twb = reagent_resv.wells()[0]
    sample_dest = sample_plate.rows()[0][:num_cols]
    pcr_mix = reagent_resv.wells()[1]

    # protocol

    # Slowly add 10ul TSB (beads) then slowly mix to suspend
    for dest in sample_dest:
        m20.pick_up_tip()
        m20.aspirate(10, tsb)
        m20.flow_rate_dispense = 3
        m20.dispense(10, dest)
        m20.drop_tip()

    for dest in sample_dest:
        m300.pick_up_tip()
        m300.flow_rate_aspirate = 30
        m300.flow_rate_dispense = 30
        m300.mix(10, 55, dest)
        m300.drop_tip()
    ctx.pause("""Please move sample plate from slot 4"""
              """to off-deck thermocycler then return to magnetic module"""
              """in slot 4 for purification. Click 'Resume' when set""")

    """"insert mag module purification base code here"""
    # Incubate on mag stand, 3 minutes

    # Remove supernatant

    # Wash twice like this:
    # disengage mag
    # add 100ul TWB slowly onto beads
    # slowly mix to resuspend
    # engage mag
    # incubate 3 min on mag stand until clear
    # remove supernatant

    # Disengage mag
    # Slowly add 100ul TWB onto beads
    # slowly mix to resuspend

    # End part 2
    for c in ctx.commands():
        print(c)
