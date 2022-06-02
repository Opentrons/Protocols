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
    midi_plate_1 = ctx.load_labware('customabnest_96_wellplate_200ul', '2')
    thermo_tubes = temp_1.load_labware('opentrons_96_aluminumblock_generic_pcr'
                                       '_strip_200ul')
    mag_module = ctx.load_module('magnetic module gen2', '4')
    sample_plate = mag_module.load_labware('customabnest_96_wellplate_200ul')
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
    vol_supernatant = 50
    z_mod_value = 5
    a_mod_value = 5
    supernatant_headspeed_modulator = 5
    # protocol

    # move supernatant to MIDI plate

    mag_module.engage(height=10)
    ctx.delay(minutes=5)
    ctx.max_speeds['Z'] = 50
    ctx.max_speeds['A'] = 50
    num_times = 1
    for source, dest in zip(sample_dest_nest, sample_dest_MIDI_1):
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
        m300.dispense(vol_supernatant, dest)
        m300.drop_tip()
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
    ctx.comment('''First half of library cleanup completed. Please move deep'''
                ''' well plate in slot 2 to magnetic module''')

    for c in ctx.commands():
        print(c)
