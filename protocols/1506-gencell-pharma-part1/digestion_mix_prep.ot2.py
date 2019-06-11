from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Digestion Mix Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        sample_num: StringSelection('4', '8', '12', '16')='4'
        ):

    # labware setup
    mix_rack = labware.load('opentrons-tuberack-2ml-screwcap', '4')
    labware.load('tempdeck', '10')
    temp_rack = labware.load(
        'opentrons-aluminum-block-2ml-eppendorf', '10', share=True)
    sample_plate = labware.load('PCR-strip-tall', '1')

    # reagent setup
    water = temp_rack.wells('A1')
    RE_buffer = temp_rack.wells('A2')
    bsa = temp_rack.wells('A3')
    alu = temp_rack.wells('A4')
    rsa = temp_rack.wells('A5')

    mastermix = mix_rack.wells('A1')
    samples = [well
               for well in sample_plate.wells('A1', length=int(sample_num)*2)]

    tiprack_10 = labware.load('tiprack-10ul', '6')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

    # pipette setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=[tiprack_10])

    p50 = instruments.P50_Single(
        mount='right',
        tip_racks=[tiprack_300])

    # Transfer reagents to mastermix
    volume_dict = {
        '4': {water: 18, RE_buffer: 23.4, bsa: 1.8, alu: 4.5, rsa: 4.5},
        '8': {water: 34, RE_buffer: 44.2, bsa: 3.4, alu: 8.5, rsa: 8.5},
        '12': {water: 50, RE_buffer: 65, bsa: 5, alu: 12.5, rsa: 12.5},
        '16': {water: 66, RE_buffer: 85.8, bsa: 6.6, alu: 16.5, rsa: 16.5}
    }
    vol_dict = volume_dict[sample_num]
    for reagent, volume in vol_dict.items():
        if volume > 10:
            pipette = p50
        else:
            pipette = p10
        pipette.pick_up_tip()
        if reagent == alu or reagent == rsa:
            pipette.mix(5, 8, reagent)
            pipette.blow_out(reagent.top())
        pipette.transfer(volume, reagent, mastermix.top(), new_tip='never')
        pipette.blow_out(mastermix.top())
        pipette.move_to(mastermix.bottom(2))
        pipette.drop_tip()

    # Transfer and master mix in samples
    for sample in samples:
        p50.pick_up_tip()
        p50.transfer(5.8, mastermix, sample, new_tip='never')
        p50.mix(5, 10, sample)
        p50.blow_out(sample)
        p50.drop_tip()
