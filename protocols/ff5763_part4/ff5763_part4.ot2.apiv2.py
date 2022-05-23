"""OPENTRONS."""
import math
from opentrons import types

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

    # define allcustom variables above here with descriptions:

    # number of samples
    num_cols = math.ceil(num_samples/8)

    # "True" for park tips, "False" for discard tips

    # load modules/labware
    temp_1 = ctx.load_module('tempdeck', '1')
    # will be custom_from_maurice
    midi_plate_1 = ctx.load_labware('nest_96_wellplate_2ml_deep', '2')
    thermo_tubes = temp_1.load_labware('opentrons_96_aluminumblock_generic_pcr'
                                       '_strip_200ul')
    mag_module = ctx.load_module('magnetic module gen2', '4')
    sample_plate = mag_module.load_labware('nest_96_wellplate_100ul_pcr_'
                                           'full_skirt')
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
    sample_dest_MIDI_1 = midi_plate_1.rows()[0][:num_cols]

    # hard code variables
    vol_supernatant = 45
    z_mod_value = 5
    a_mod_value = 5
    # protocol

    # move supernatant to MIDI plate

    mag_module.engage(height_from_base=10)
    # is this delay needed here? Probs on part 3
    ctx.delay(minutes=5)
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source, dest in zip(sample_dest_nest, sample_dest_MIDI_1):
        side = 1 if num_times % 2 == 0 else -1
        m300.flow_rate.aspirate /= 5
        ctx.max_speeds['Z'] /= z_mod_value
        ctx.max_speeds['A'] /= a_mod_value
        m300.pick_up_tip()
        m300.aspirate(
            vol_supernatant, source.bottom().move(types.Point(x=side,
                                                              y=0, z=0.5)))
        m300.dispense(vol_supernatant, dest)
        m300.drop_tip()
        m300.flow_rate.aspirate *= 5
        ctx.max_speeds['Z'] *= z_mod_value
        ctx.max_speeds['A'] *= a_mod_value
        num_times += 1
        print(side)
    mag_module.disengage()

    # add 40ul NFW to MIDI plate 1
    for dest in sample_dest_MIDI_1:
        m300.pick_up_tip()
        m300.aspirate(40, nf_water)
        m300.dispense(40, dest)
        m300.drop_tip()
    # add 45ul IPB to MIDI plate 1 and mix 10x
    for dest in sample_dest_MIDI_1:
        m300.pick_up_tip()
        m300.aspirate(45, ipb)
        m300.dispense(45, dest)
        m300.mix(10, 100)
        m300.drop_tip()
    # Incubate 5 minutes
    ctx.delay(minutes=5)

    ctx.comment('''First half of library cleanup completed. Please move MIDI'''
                ''' plate in slot 2 to magnetic module and replace with fresh'''
                ''' final MIDI sample plate''')
    # transfer 15ul IPB to each well in MIDI plate 2
    # Transfer 125ul supernatant from MIDI plate 1 to midi plate 2
    # Mix MIDI 2 10x
    # Incubate 5 minutes
    # Move MIDI 2 to mag stand, toss MIDI plate 1
    # Mag stand engage for 5 minutes
    # discard supernatant
    # wash twice: Add 200ul EtOH, wait 30 secs, discard supernatant
    # remove remaining EtOH w/20ul pipette
    # Air dry 5 minutes
    # disengage mag stand
    # add 32ul RSB
    # Mix to resuspend
    # Wait 2 minutes
    # engage mag stand 2 minutes
    # transfer 30 ul from MIDI plate 2 to new 96 well pcr plate
    for c in ctx.commands():
        print(c)
