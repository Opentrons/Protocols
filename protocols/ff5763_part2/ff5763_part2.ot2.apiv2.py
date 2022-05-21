"""OPENTRONS."""
import math
from opentrons.types import Point
metadata = {
    'protocolName': 'Illumina DNA Prep Part 2, Post-Tagmentation Clean-up',
    'author': 'AUTHOR NAME <authoremail@company.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'   # CHECK IF YOUR API LEVEL HERE IS UP TO DATE
                         # IN SECTION 5.2 OF THE APIV2 "VERSIONING"
}

TEST_MODE = False


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
    twb = reagent_resv.rows()[0][0]
    pcr_mix = reagent_resv.rows()[0][1]

    sample_dest = sample_plate.rows()[0][:num_cols]

    radius = sample_dest[0].diameter/2
    x_offset_beads = 0.85*radius
    z_offset_beads = 3
    supernatant_headspeed_modulator = 5
    supernatant_flowrate_modulator = 5

    # protocol

    # Steps 1-2
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
    # Step 4-5
    # Incubate on mag stand, 3 minutes

    # Remove supernatant
    m300.flow_rate.aspirate /= supernatant_flowrate_modulator
    ctx.max_speeds['A'] /= supernatant_headspeed_modulator
    ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
    for s in sample_dest:
        m300.pick_up_tip()
        # going to break transfer func up for better control
        m300.transfer(65, s.bottom(1), liquid_trash[0], air_gap=20,
                      new_tip='never')
        m300.blow_out()
        m300.drop_tip()
    m300.flow_rate.aspirate *= supernatant_flowrate_modulator
    ctx.max_speeds['A'] *= supernatant_headspeed_modulator
    ctx.max_speeds['Z'] *= supernatant_headspeed_modulator

    # Step 6

    # Wash twice like this:
    # disengage mag
    # add 100ul TWB slowly onto beads
    # slowly mix to resuspend
    # engage mag, incubate 3 min on mag stand until clear
    # remove supernatant

    # Step 7
    # Disengage mag
    # Slowly add 100ul TWB onto beads
    # slowly mix to resuspend

    def bead_mix(reps, vol, well, angle, pip=m300):
        dispense_loc = well.bottom().move(
            Point(x=x_offset_beads*angle, y=0, z=z_offset_beads))
        for _ in range(reps):
            pip.aspirate(vol, well.bottom(1))
            pip.dispense(vol, dispense_loc)

    count = 0
    total_twb = 100
    for wash in range(3):
        mag_module.disengage()

        # resuspend beads in TWB
        for i, s in sample_dest:
            # I don't know what ind is and at this point I'm afraid to ask
            ind = (count*len(twb))//total_twb
            count += 1

            side = i % 2
            angle = 1 if side == 0 else -1
            disp_loc = s.bottom().move(
                Point(x=x_offset_beads*angle, y=0, z=z_offset_beads))
            m20.pick_up_tip()
            m20.aspirate(10, twb[ind])
            m20.move_to(s.center())
            m20.flow_rate.aspirate /= supernatant_flowrate_modulator
            m20.flow_rate.dispense /= supernatant_flowrate_modulator
            m20.dispense(10, disp_loc)
            m20.drop_tip()
            # m300.mix(10, 80, disp_loc)
            m300.pick_up_tip()
            bead_mix(10, 80, s, angle)
            m300.drop_tip()
            m20.flow_rate.aspirate *= supernatant_flowrate_modulator
            m20.flow_rate.dispense *= supernatant_flowrate_modulator

        mag_module.engage(height=18)
        # steps 4-
        if wash < 2:
            if TEST_MODE:
                ctx.comment('Incubating beads on magnet for 3 minutes')
            else:
                ctx.delay(
                    minutes=3, msg='Incubating beads on magnet for 3 minutes')
            # remove and discard supernatant
            m300.flow_rate.aspirate /= supernatant_flowrate_modulator
            ctx.max_speeds['A'] /= supernatant_headspeed_modulator
            ctx.max_speeds['Z'] /= supernatant_headspeed_modulator
            for s in sample_dest:
                m300.pick_up_tip()
                # What is the volume we need to aspirate here, removing super?
                m300.aspirate(120, s.bottom(1))
                m300.move_to(s.top())
                m300.aspirate(20, s.top())  # air gap
                m300.dispense(20, liquid_trash.top())
                m300.dispense(120, liquid_trash[wash])
                # m300.transfer(
                #     120, s.bottom(1), liquid_trash[wash], air_gap=20,
                #     new_tip='never')
                m300.blow_out()
                m300.drop_tip()
            m300.flow_rate.aspirate *= supernatant_flowrate_modulator
            ctx.max_speeds['A'] *= supernatant_headspeed_modulator
            ctx.max_speeds['Z'] *= supernatant_headspeed_modulator

    # End part 2
    for c in ctx.commands():
        print(c)
