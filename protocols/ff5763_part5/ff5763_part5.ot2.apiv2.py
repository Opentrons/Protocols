from opentrons import protocol_api
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
    """MIDI from Part 4 is on magnetic module to start, moves to trash at"""
    """ specified step then replaced with MIDI plate in slot 2"""
    temp_1 = ctx.load_module('tempdeck', '1')
    thermo_tubes = temp_1.load_labware('opentrons_96_aluminumblock_generic_pcr'
                                       '_strip_200ul')
    mag_module = ctx.load_module('magnetic module gen2', '4')
    # will be custom labware from Maurice
    midi_plate_1 = mag_module.load_labware('custom_from_maurice')
    midi_plate_2 = ctx.load_labware('custom_from_maurice', '2')
    reagent_resv = ctx.load_labware('nest_12_reservoir_15ml', '5')
    liquid_trash = ctx.load_labware('nest_1_reservoir_195ml', '9')

    # load tipracks
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['3', '8']]
    tiprack200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                  for slot in ['6', '7']]

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2', 'left', tip_racks=tiprack200)

    # reagents
    '''includes reagents used in other steps for housekeeping purposes'''
    master_mix = thermo_tubes.rows()[0][0]
    nf_water = thermo_tubes.rows()[0][1]
    tsb = thermo_tubes.rows()[0][2]
    ipb = thermo_tubes.rows()[0][3]
    sample_dest_nest = sample_plate.rows()[0][:num_cols]
    sample_dest_MIDI_1_pos_1 = midi_plate_1.rows()[0][:num_cols]
    sample_dest_MIDI_2_pos_1 = midi_plate_2.rows()[0][:num_cols]
    sample_dest_MIDI_2_pos_2 = midi_plate_1.rows()[0][:num_cols]
    # hard code variables
    vol_supernatant = 45
    z_mod_value = 5
    a_mod_value = 5
    MIDI_plate_mag_height = 10
    # protocol


# transfer 15ul IPB to each empty well in MIDI plate 2
    m20.pick_up_tip()
    for dest in sample_dest_MIDI_2_pos_1:
        m20.aspirate(15, ipb)
        m20.dispense(15, dest)
    m20.drop_tip()
# Transfer 125ul supernatant from MIDI plate 1 to midi plate 2 with a 10x mix

    mag_module.engage(height_from_base=10)
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source, dest in zip(sample_dest_MIDI_1_pos_1,
                            sample_dest_MIDI_2_pos_1):
        side = 1 if num_times % 2 == 0 else -1
        m300.flow_rate.aspirate /= 5
        ctx.max_speeds['Z'] /= z_mod_value
        ctx.max_speeds['A'] /= a_mod_value
        m300.pick_up_tip()
        m300.aspirate(
            125, source.bottom().move(types.Point(x=side,
                                                  y=0, z=0.5)))
        m300.dispense(125, dest)
        m300.flow_rate.aspirate *= 5
        m300.mix(10, 120)
        m300.drop_tip()
        ctx.max_speeds['Z'] *= z_mod_value
        ctx.max_speeds['A'] *= a_mod_value
        num_times += 1
        print(side)
    mag_module.disengage()
    # Incubate 5 minutes
    ctx.delay(minutes=5)
# Move MIDI 2 to mag stand, toss MIDI plate 1
    ctx.pause('''Please remove MIDI plate on the magnetic module from the'''
              ''' robot and discard. Move the MIDI plate in slot 2, now full'''
              ''' of liquid, to the magnetic module. Click resume'''
              ''' when complete''')
    # Mag stand engage for 5 minutes
    # discard supernatant
    mag_module.engage(height_from_base=MIDI_plate_mag_height)
    ctx.delay(minutes=5)
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source in sample_dest_MIDI_2_pos_2:
        side = 1 if num_times % 2 == 0 else -1
        m300.flow_rate.aspirate /= 5
        ctx.max_speeds['Z'] /= z_mod_value
        ctx.max_speeds['A'] /= a_mod_value
        m300.pick_up_tip()
        m300.aspirate(
            45, source.bottom().move(types.Point(x=side,
                                                 y=0, z=0.5)))
        m300.dispense(45, liquid_trash.wells()[0])
        m300.drop_tip()
        m300.flow_rate.aspirate *= 5
        ctx.max_speeds['Z'] *= z_mod_value
        ctx.max_speeds['A'] *= a_mod_value
        num_times += 1
        print(side)
    mag_module.disengage()
# wash twice: Add 200ul EtOH, wait 30 secs, discard supernatant
# remove remaining EtOH w/20ul pipette
# Air dry 5 minutes
# disengage mag stand
# add 32ul RSB
# Mix to resuspend
# Wait 2 minutes
# engage mag stand 2 minutes
# transfer 30 ul from MIDI plate 2 to new 96 well pcr plate
