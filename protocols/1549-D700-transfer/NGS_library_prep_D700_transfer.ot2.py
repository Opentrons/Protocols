from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Library Prep: D700 Transfer',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'MicroAmp-96-PCR'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.49,
        depth=20.1,
        volume=200)

# labware
strips = labware.load('opentrons-aluminum-block-PCR-strips-200ul', '2')
tips10 = labware.load('tiprack-10ul', '5')

# modules
temp_deck = modules.load('tempdeck', '1')
temp_plate = labware.load(plate_name, '1', share=True)
if not robot.is_simulating():
    temp_deck.set_temperature(4)
    temp_deck.wait_for_temp()

# pipettes
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tips10]
)


def run_custom_protocol(transfer_volume: float = 5,
                        D700_strip_column: StringSelection('1', '2', '3', '4',
                                                           '5', '6', '7', '8',
                                                           '9', '10', '11',
                                                           '12') = '6',
                        destination_column: StringSelection('1', '2', '3', '4',
                                                            '5', '6', '7', '8',
                                                            '9', '10', '11',
                                                            '12') = '1'):

    # reagent setup
    D700 = strips.columns(D700_strip_column)
    dest = temp_plate.columns(destination_column)

    # transfer D700 to correct column of plate on temp deck
    m10.transfer(transfer_volume, D700, dest)
