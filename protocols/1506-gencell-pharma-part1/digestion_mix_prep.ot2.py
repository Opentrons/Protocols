from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Digestion Mix Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        sample_num: StringSelection('4', '8', '12', '16')='4'
        ):

    sample_num = int(sample_num)

    # labware setup
    screwcap_rack = labware.load('opentrons-tuberack-2ml-screwcap', '4')
    eppendorf_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
    sample_plate = labware.load('PCR-strip-tall', '1')

    # reagent setup
    water = screwcap_rack.wells('D1')
    RE_buffer = screwcap_rack.wells('D2')
    bsa = screwcap_rack.wells('D3')
    alu = screwcap_rack.wells('D4')
    rsa = screwcap_rack.wells('D5')
    mastermix = eppendorf_rack.wells('A1')

    samples = [well
               for well in sample_plate.wells('A1', length=sample_num*2)]

    tiprack_10 = labware.load('tiprack-10ul', '6')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '9')

    # pipette setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=[tiprack_10])

    p50 = instruments.P50_Single(
        mount='right',
        tip_racks=[tiprack_300])

    # Transfer reagents to mastermix
    volume_dict = {
        4: {water: 18, RE_buffer: 23.4, bsa: 1.8, alu: 4.5, rsa: 4.5},
        8: {water: 34, RE_buffer: 44.2, bsa: 3.4, alu: 8.5, rsa: 8.5},
        12: {water: 50, RE_buffer: 65, bsa: 5, alu: 12.5, rsa: 12.5},
        16: {water: 66, RE_buffer: 85.8, bsa: 6.6, alu: 16.5, rsa: 16.5}
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
            pipette.blow_out(reagent)
        pipette.transfer(
            volume, reagent, mastermix, blow_out=True, new_tip='always')

    # Transfer and master mix in samples
    for sample in samples:
        p50.pick_up_tip()
        p50.transfer(5.8, mastermix, sample, new_tip='never')
        p50.mix(5, 10, sample)
        p50.blow_out(sample)
        p50.drop_tip()
