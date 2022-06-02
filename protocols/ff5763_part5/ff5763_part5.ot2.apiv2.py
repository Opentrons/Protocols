"""OPENTRONS."""
from opentrons import types
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
    temp_1 = ctx.load_module('tempdeck', '1')
    thermo_tubes = temp_1.load_labware('opentrons_96_aluminumblock_generic_pcr'
                                       '_strip_200ul')
    # can change to whatever plate works better for next off-deck step
    final_plate = ctx.load_labware('nest_96_wellplate_2ml_deep',
                                   '2')
    mag_module = ctx.load_module('magnetic module gen2', '4')
    # may be custom labware from Maurice
    midi_plate_1 = mag_module.load_labware('nest_96_wellplate_2ml_deep')
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '5')
    supernatant_pcr_plate = ('customabnest_96_wellplate_200ul', '8')
    liquid_trash = ctx.load_labware('nest_1_reservoir_195ml', '9')

    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['3']]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                  for slot in ['6', '7', '10', '11']]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2', 'left', tip_racks=tiprack200)

    # reagents
    '''includes reagents used in other steps for housekeeping purposes'''
    master_mix = thermo_tubes.rows()[0][0]
    nf_water = thermo_tubes.rows()[0][2]
    tsb = thermo_tubes.rows()[0][4]
    ipb = thermo_tubes.rows()[0][6]
    rsb = thermo_tubes.rows()[0][8]
    etoh = reagent_resv.wells()[11]
    source_midi_plate_mag = midi_plate_1.rows()[0][6:6+num_cols]
    final_plate_dest = final_plate.rows()[0][:num_cols]
    supernatant_pcr_plate_dest = supernatant_pcr_plate.rows()[0][:num_cols]
    # hard code variables
    vol_supernatant = 45
    z_mod_value = 5
    a_mod_value = 5
    MIDI_plate_mag_height = 9
    # protocol


# transfer 15ul IPB to each empty well second half of MIDI plate
    m20.pick_up_tip()
    for dest in final_plate_dest:
        m20.flow_rate.aspirate /= 4
        m20.flow_rate.dispense /= 4
        m20.flow_rate.blow_out /= 4
        m20.aspirate(15, ipb)
        m20.move_to(ipb.top(-2))
        ctx.delay(seconds=2)
        m20.touch_tip(v_offset=-2)
        m20.move_to(ipb.top(-2))
        m20.aspirate(3, ipb.top(-2))
        m20.dispense(3, dest.top())
        m20.dispense(15, dest)
        m20.flow_rate.aspirate *= 4
        m20.flow_rate.dispense *= 4
        m20.flow_rate.blow_out *= 4
    m20.drop_tip()
# Transfer 125ul supernatant from mag plate to final plate with a 10x mix

    mag_module.engage(height=MIDI_plate_mag_height)
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source, dest in zip(source_midi_plate_mag, final_plate_dest):
        side = 1 if num_times % 2 == 0 else -1
        m300.flow_rate.aspirate /= 5
        m300.pick_up_tip()
        m300.move_to(source.top())
        ctx.max_speeds['Z'] /= z_mod_value
        ctx.max_speeds['A'] /= a_mod_value
        m300.aspirate(
            125, source.bottom().move(types.Point(x=side,
                                                  y=0, z=0.5)))
        m300.move_to(source.top(-2))
        ctx.max_speeds['Z'] *= z_mod_value
        ctx.max_speeds['A'] *= a_mod_value
        ctx.delay(seconds=2)
        m300.touch_tip(v_offset=-2)
        m300.move_to(source.top(-2))
        m300.aspirate(10, source.top(-2))
        m300.dispense(10, dest.top(-2))
        m300.dispense(125, dest)
        m300.flow_rate.aspirate *= 5
        m300.mix(10, 120)
        m300.drop_tip()
        num_times += 1
        print(side)
    mag_module.disengage()
    # Incubate 5 minutes
    ctx.delay(minutes=5)
    # Mag stand engage for 5 minutes
    ctx.pause('Please dispose of deep well plate in magnetic module and move'
              ' plate in slot 2 onto magnetic module. Press "Resume" when'
              ' finished')
    # discard supernatant
    mag_module.engage(height=MIDI_plate_mag_height)
    ctx.delay(minutes=5)
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source in final_plate_dest:
        side = 1 if num_times % 2 == 0 else -1
        m300.flow_rate.aspirate /= 5
        m300.pick_up_tip()
        ctx.max_speeds['Z'] /= z_mod_value
        ctx.max_speeds['A'] /= a_mod_value
        m300.aspirate(
            45, source.bottom().move(types.Point(x=side,
                                                 y=0, z=0.5)))
        ctx.max_speeds['Z'] *= z_mod_value
        ctx.max_speeds['A'] *= a_mod_value
        m300.dispense(45, liquid_trash.wells()[0])
        m300.drop_tip()
        m300.flow_rate.aspirate *= 5
        num_times += 1
        print(side)
    mag_module.disengage()
# wash twice: Add 200ul EtOH (let's try 100), wait 30 secs, discard supernatant
    for _ in range(2):
        for dest in final_plate_dest:
            m300.pick_up_tip()
            m300.aspirate(100, etoh)
            m300.dispense(100, dest)
            m300.drop_tip()
        ctx.delay(seconds=30)
        # discard supernatant
        mag_module.engage(height=MIDI_plate_mag_height)
        ctx.delay(minutes=5)
        ctx.max_speeds['Z'] = 50
        ctx.max_speeds['A'] = 50
        num_times = 1
        for source in final_plate_dest:
            side = 1 if num_times % 2 == 0 else -1
            m300.flow_rate.aspirate /= 5
            m300.pick_up_tip()
            ctx.max_speeds['Z'] /= z_mod_value
            ctx.max_speeds['A'] /= a_mod_value
            m300.aspirate(
                100, source.bottom().move(types.Point(x=side,
                                                      y=0, z=0.5)))
            ctx.max_speeds['Z'] *= z_mod_value
            ctx.max_speeds['A'] *= a_mod_value
            m300.dispense(100, liquid_trash.wells()[0])
            m300.drop_tip()
            m300.flow_rate.aspirate *= 5
            num_times += 1
            print(side)

# remove remaining EtOH w/20ul pipette
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source in final_plate_dest:
        side = 1 if num_times % 2 == 0 else -1
        m20.flow_rate.aspirate /= 5
        m20.pick_up_tip()
        ctx.max_speeds['Z'] /= z_mod_value
        ctx.max_speeds['A'] /= a_mod_value
        m20.aspirate(
            15, source.bottom().move(types.Point(x=side,
                                                 y=0, z=0.5)))
        ctx.max_speeds['Z'] *= z_mod_value
        ctx.max_speeds['A'] *= a_mod_value
        m20.dispense(15, liquid_trash.wells()[0])
        m20.drop_tip()
        m20.flow_rate.aspirate *= 5
        num_times += 1
        print(side)
# Air dry 5 minutes
    ctx.delay(minutes=5)
# disengage mag stand
    mag_module.disengage()
# add 32ul RSB, mix to resuspend
    for dest in final_plate_dest:
        m300.pick_up_tip()
        m300.aspirate(32, rsb)
        m300.dispense(32, dest)
        m300.mix(10, 40)
        m300.drop_tip()
# Wait 2 minutes
    ctx.delay(minutes=2)
# engage mag stand 2 minutes
    mag_module.engage(height=MIDI_plate_mag_height)
# transfer 30 ul from MIDI plate 2 to new 96 well pcr plate
    """IS THIS NEEDED?"""
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source, dest in zip(final_plate_dest, supernatant_pcr_plate_dest):
        side = 1 if num_times % 2 == 0 else -1
        m300.flow_rate.aspirate /= 5
        m300.pick_up_tip()
        ctx.max_speeds['Z'] /= z_mod_value
        ctx.max_speeds['A'] /= a_mod_value
        m300.aspirate(
            30, source.bottom().move(types.Point(x=side,
                                                 y=0, z=0.5)))
        ctx.max_speeds['Z'] *= z_mod_value
        ctx.max_speeds['A'] *= a_mod_value
        m300.dispense(30, dest)
        m300.drop_tip()
        m300.flow_rate.aspirate *= 5
        num_times += 1
        print(side)

    for c in ctx.commands():
        print(c)
