from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'DNA Denaturation and Fragmentation',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}


def run_custom_protocol(sample_num: int=16):

    # labware setup
    labware.load('tempdeck', '10')
    temp_rack = labware.load(
        'opentrons-aluminum-block-2ml-eppendorf', '10', share=True)
    samples_plate = labware.load('PCR-strip-tall', '1')
    tiprack_10 = labware.load('tiprack-10ul', '6')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

    # pipette setup
    m10 = instruments.P10_Multi(
        mount='left',
        tip_racks=[tiprack_10])

    m50 = instruments.P50_Multi(
        mount='right',
        tip_racks=[tiprack_300])

    # reagent setup
    randomprim = temp_rack.wells('A1')
    samples = [well for well in samples_plate.wells('A1', length=sample_num)]
    if sample_num <= 8:
        sample_cols = [samples_plate.cols('1')]
    else:
        sample_cols = samples_plate.cols('1', length=math.ceil(sample_num/8))

    # Transfer random primer
    m50.pick_up_tip()
    m50.mix(5, 30, randomprim)
    for sample in samples:
        if m50.current_volume <= 5:
            m50.aspirate(randomprim)
        m50.dispense(5, sample)
    m50.drop_tip()

    # mix samples
    for col in sample_cols:
        m10.pick_up_tip()
        m10.mix(5, 10, col)
        m10.blow_out(col[0].bottom(5))
        m10.drop_tip()
