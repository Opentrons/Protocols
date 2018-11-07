from opentrons import labware, instruments
from otcustomizers import StringSelection

"""
Well Pooling
"""


def run_custom_protocol(
        pool_volume: float=50,
        tuberack_type: StringSelection(
            'opentrons-tuberack-2ml-eppendorf',
            'opentrons-tuberack-15ml')='opentrons-tuberack-2ml-eppendorf'):

    # robot setup
    plate = labware.load('96-flat', '1', 'Sample Plate')

    tuberack = labware.load(tuberack_type, '2')

    if pool_volume < 30:
        tiprack = labware.load('tiprack-10ul', '5')
        pipette = instruments.P10_Single(
            mount='left',
            tip_racks=[tiprack])
    else:
        tiprack = labware.load('tiprack-200ul', '5')
        pipette = instruments.P300_Single(
            mount='left',
            tip_racks=[tiprack])

    # transfer each well of the sample plate to tuberack A1
    for well in plate.wells():
        pipette.transfer(
            pool_volume, well, tuberack.wells('A1'), blow_out=True)
