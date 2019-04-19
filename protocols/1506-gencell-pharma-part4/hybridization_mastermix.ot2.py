from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Hybridization Master Mix',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(sample_num: int=8):

    # labware setup
    mix_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '4')
    labware.load('tempdeck', '10')
    temp_rack = labware.load('opentrons-aluminum-block-2ml-eppendorf', '10',
                             share=True)
    samples_plate = labware.load('PCR-strip-tall', '1')

    tiprack_50 = labware.load('opentrons-tiprack-300ul', '6')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

    # pipette setup
    m300 = instruments.P300_Multi(
        mount='left',
        tip_racks=[tiprack_300])

    m50 = instruments.P50_Multi(
        mount='right',
        tip_racks=[tiprack_50])

    # reagent setup
    cot = temp_rack.wells('A1')
    blockagent = temp_rack.wells('A2')

    mix_dest = mix_rack.wells('A1')
    hyb_buf = mix_rack.wells('A3')
    samples = [well for well in samples_plate.wells('A1', length=sample_num)]
    if sample_num <= 8:
        sample_cols = [samples_plate.cols('1')]
    else:
        sample_cols = samples_plate.cols('1', length=math.ceil(sample_num/8))

    s_factor = sample_num + 1

    # Transfer reagents to mastermixes
    m50.transfer(s_factor * 5, cot, mix_dest)
    m300.transfer(s_factor * 11, blockagent, mix_dest)
    m300.pick_up_tip()
    m300.mix(5, 200, hyb_buf)
    m300.transfer(s_factor * 55, hyb_buf, mix_dest, new_tip='never')
    m300.mix(5, 300, mix_dest)
    m300.drop_tip()

    m300.pick_up_tip()
    for sample in samples:
        if m300.current_volume <= 71:
            m300.aspirate(mix_dest)
        m300.dispense(71, sample)
    m300.drop_tip()

    for col in sample_cols:
        m300.pick_up_tip()
        m300.mix(5, 50, col)
        m300.drop_tip()
