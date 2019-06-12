from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'DNA Denaturation and Fragmentation',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}


def run_custom_protocol(
        sample_num: StringSelection('4', '8', '12', '16')='4'
        ):

    sample_num = int(sample_num)

    # labware setup
    eppendorf_rack = labware.load('opentrons-tuberack-2ml-screwcap', '4')
    sample_plate = labware.load('PCR-strip-tall', '1')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '9')

    # pipette setup
    p50 = instruments.P50_Single(
        mount='right',
        tip_racks=[tiprack_300])

    # reagent setup
    randomprim = eppendorf_rack.wells('A1')

    samples = [well
               for well in sample_plate.wells('A1', length=sample_num*2)]

    # Transfer random primer
    p50.pick_up_tip()
    p50.mix(10, 30, randomprim)
    for sample in samples:
        if not p50.tip_attached:
            p50.pick_up_tip()
        p50.transfer(5, randomprim, sample, new_tip='never')
        p50.mix(5, 10, sample)
        p50.blow_out(sample)
        p50.drop_tip()
