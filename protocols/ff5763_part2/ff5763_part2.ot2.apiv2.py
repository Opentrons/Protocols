"""OPENTRONS."""
import math
from opentrons import types
metadata = {
    'protocolName': 'Illumina DNA Prep Part 2, Post-Tagmentation Clean-up',
    'author': 'AUTHOR NAME <authoremail@company.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}

TEST_MODE = False


def run(ctx):
    """PROTO COL."""
    [num_samples
     ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "num_samples")

    # define all custom variables above here with descriptions:

    # number of samples
    num_cols = math.ceil(num_samples/8)

    # "True" for park tips, "False" for discard tips

    # load modules/labware
    """Step 2 has the sample plate on the mag module in slot 4!"""
    temp_1 = ctx.load_module('tempdeck', '1')
    starting_tray = ctx.load_labware('customabnest_96_wellplate_200ul', '2')
    thermo_tubes = temp_1.load_labware('opentrons_96_aluminumblock_generic_pcr'
                                       '_strip_200ul')
    mag_module = ctx.load_module('magnetic module gen2', '4')
    sample_plate = mag_module.load_labware('nest_96_wellplate_2ml_deep')
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '5')
    liquid_trash = ctx.load_labware('nest_1_reservoir_195ml', '9')

    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['3']]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                  for slot in ['6', '7', '8', '10']]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2', 'left', tip_racks=tiprack200)

    # reagents
    '''includes reagents used in other steps for housekeeping purposes'''
    master_mix_tag = thermo_tubes.rows()[0][0]
    nf_water = thermo_tubes.rows()[0][1]
    tsb = thermo_tubes.rows()[0][2]
    twb = reagent_resv.rows()[0][0]
    pcr_mix = reagent_resv.rows()[0][1]

    starting_dest = starting_tray.rows()[0][:num_cols]
    sample_dest = sample_plate.rows()[0][:num_cols]

    supernatant_headspeed_modulator = 5
    vol_supernatant = 40
    nest_96_mag_engage_height = 10
    # protocol

    # Steps 1-2
    # Slowly add 10ul TSB (beads) then slowly mix to suspend
    ctx.comment("""adding beads""")
    for dest in starting_dest:
        m20.pick_up_tip()
        m20.flow_rate.aspirate = 3
        m20.flow_rate.dispense = 3
        m20.aspirate(10, tsb)
        m20.dispense(10, dest)
        m20.drop_tip()
    ctx.comment('''mixing beads''')
    for dest in starting_dest:
        m300.pick_up_tip()
        m300.flow_rate.aspirate /= 4
        m300.flow_rate.dispense /= 4
        m300.mix(10, 55, dest)
        m300.flow_rate.aspirate *= 4
        m300.flow_rate.dispense *= 4
        m300.drop_tip()
    ctx.pause("""Please move sample plate from slot 2"""
              """ to off-deck thermocycler then return to slot 2."""
              """Click 'Resume' when set""")

    # Mid-protocol transfer to mag module
    ctx.comment('moving samples from slot 2 to slot 4')
    for source, dest in zip(starting_dest, sample_dest):
        m300.pick_up_tip()
        m300.flow_rate.aspirate = 3
        m300.flow_rate.dispense = 3
        m300.aspirate(50, source)
        m300.move_to(source.top(-2))
        ctx.delay(seconds=2)
        m300.aspirate(10, source.top(-2))
        m300.move_to(dest.top(10))
        m300.move_to(dest.top(-2))
        m300.dispense(10, dest.top(-2))
        m300.dispense(50, dest)
        m300.blow_out(dest.top())
        m300.drop_tip()

    """"insert mag module purification base code here"""
    # Step 4
    # Incubate on mag stand, 3 minutes
    ctx.comment('''incubate 3 minutes''')
    mag_module.engage(height_from_base=nest_96_mag_engage_height)
    ctx.delay(minutes=3)
    # Step 5
    # Discard supernatant
    ctx.comment('''discarding supernatant''')
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source in sample_dest:
        side = 1 if num_times % 2 == 0 else -1
        m300.flow_rate.aspirate /= 5
        m300.flow_rate.dispense /= 5
        m300.pick_up_tip()
        m300.move_to(source.top())
        ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
        ctx.max_speeds['A'] /= supernatant_headspeed_modulator
        m300.aspirate(
            vol_supernatant, source.bottom().move(types.Point(x=side,
                                                              y=0, z=0.5)))
        m300.move_to(source.top())
        ctx.max_speeds['Z'] *= supernatant_headspeed_modulator
        ctx.max_speeds['A'] *= supernatant_headspeed_modulator
        m300.flow_rate.aspirate *= 5
        m300.flow_rate.dispense *= 5
        m300.dispense(vol_supernatant, liquid_trash.wells()[0])
        m300.drop_tip()
        num_times += 1
    mag_module.disengage()

    # Step 6, TWB wash twice removing super each time
    ctx.comment('''twb wash twice, removing supernatant each time''')
    for _ in range(2):
        m300.flow_rate.aspirate /= 5
        m300.flow_rate.dispense /= 5
        for dest in sample_dest:
            m300.pick_up_tip()
            m300.aspirate(100, twb)
            m300.dispense(100, dest)
            m300.mix(3, 120)
            m300.drop_tip()
        m300.flow_rate.aspirate *= 5
        m300.flow_rate.dispense *= 5

        mag_module.engage(height_from_base=nest_96_mag_engage_height)

        ctx.delay(minutes=3)
        # remove super
        ctx.max_speeds['Z'] = 50
        ctx.max_speeds['A'] = 50
        num_times = 1
        m300.flow_rate.aspirate /= 5
        for source in sample_dest:
            side = 1 if num_times % 2 == 0 else -1
            m300.pick_up_tip()
            m300.flow_rate.aspirate /= 5
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
            m300.return_tip()
            num_times += 1
            print(side)
        mag_module.disengage()
    # Step 7, add twb and mix, leave TWB and incubate on mag stand until step 3
    m300.flow_rate.aspirate /= 5
    m300.flow_rate.dispense /= 5
    for dest in sample_dest:
        m300.pick_up_tip()
        m300.aspirate(100, twb)
        m300.dispense(100, dest)
        m300.mix(3, 120)
        m300.drop_tip()
    m300.flow_rate.aspirate *= 5
    m300.flow_rate.dispense *= 5

    mag_module.engage(nest_96_mag_engage_height)
    ctx.comment('''Clean up complete, please move on to part 3 of the'''
                ''' protocol, leaving the plate engaged on the'''
                ''' magnetic module''')

    # End part 2
    for c in ctx.commands():
        print(c)
