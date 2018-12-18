from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Tube Filling',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}

# labware setup
trough = labware.load('trough-12row', '1')
tiprack = labware.load('tiprack-200ul', '11')

# instruments setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
    number_of_tubes: int=24,
    tuberack: StringSelection(
        'opentrons-tuberack-2ml-eppendorf',
        'opentrons-tuberack-2ml-screwcap')='opentrons-tuberack-2ml-eppendorf',
    transfer_volume: float=300
        ):

    if number_of_tubes > 216:
        raise Exception("Number of tubes cannot exceed 216.")

    number_of_racks = math.ceil(number_of_tubes / 24)
    tuberacks = [labware.load(tuberack, str(slot))
                 for slot in range(2, 11)][:number_of_racks]

    tubes = [well for rack in tuberacks
             for well in rack.wells()][:number_of_tubes]

    p300.pick_up_tip()
    for tube in tubes:
        p300.transfer(
            transfer_volume,
            trough.wells('A1'),
            tube,
            new_tip='never')
    p300.drop_tip()
