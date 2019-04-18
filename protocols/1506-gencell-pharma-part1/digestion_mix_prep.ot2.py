from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Digestion Mix Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        sample_num: int=16
        ):

    # labware setup
    mix_rack = labware.load('opentrons-tuberack-2ml-screwcap', '4')
    labware.load('tempdeck', '10')
    temp_rack = labware.load(
        'opentrons-aluminum-block-2ml-eppendorf', '10', share=True)
    samples_plate = labware.load('PCR-strip-tall', '1')

    # reagent setup
    water = temp_rack.wells('A1')
    RE_buffer = temp_rack.wells('A2')
    bsa = temp_rack.wells('A3')
    alu = temp_rack.wells('A4')
    rsa = temp_rack.wells('A5')

    mastermix = mix_rack.wells('A1')
    samples = [well for well in samples_plate.wells('A1', length=sample_num)]
    if sample_num <= 8:
        sample_cols = [samples_plate.cols('1')]
    else:
        sample_cols = samples_plate.cols('1', length=math.ceil(sample_num/8))

    tiprack_10 = labware.load('tiprack-10ul', '6')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

    # pipette setup
    m10 = instruments.P10_Multi(
        mount='left',
        tip_racks=[tiprack_10])

    m50 = instruments.P50_Multi(
        mount='right',
        tip_racks=[tiprack_300])

    # Transfer reagents to mastermix
    m50.transfer(2 * (sample_num + 1), water, mastermix)
    m50.transfer(2.6 * (sample_num + 1), RE_buffer, mastermix)
    m10.pick_up_tip()
    m10.mix(5, 8, bsa)
    m10.transfer(0.2 * (sample_num + 1), bsa, mastermix, new_tip='never')
    m10.drop_tip()
    m10.transfer(0.5 * (sample_num + 1), alu, mastermix, mix_before=(5, 8))
    m10.transfer(0.5 * (sample_num + 1), rsa, mastermix, mix_before=(5, 8))

    # Distribute master mix in samples
    m50.pick_up_tip()
    m50.mix(5, 30, mastermix)
    for sample in samples:
        if m50.current_volume <= 5.8:
            m50.aspirate(mastermix)
        m50.dispense(5.8, sample)
    m50.drop_tip()

    # Mix each column
    for col in sample_cols:
        m10.pick_up_tip()
        m10.mix(5, 10, col)
        m10.blow_out(col[0].top())
        m10.drop_tip()
