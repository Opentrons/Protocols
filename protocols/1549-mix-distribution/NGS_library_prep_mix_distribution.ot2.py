from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Library Prep: Mix Distribution',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

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

# modules
temp_deck = modules.load('tempdeck', '1')
temp_plate = labware.load(plate_name, '1', share=True)
if not robot.is_simulating():
    temp_deck.set(4)
    temp_deck.wait_for_temp()


def run_custom_protocol(
        transfer_volume: float = 10,
        mix_strip_column: StringSelection('1', '2', '3', '4', '5', '6', '7',
                                          '8', '9', '10', '11', '12') = '1',
        destination_columns_start: StringSelection('1', '2', '3', '4', '5',
                                                   '6', '7', '8', '9', '10',
                                                   '11', '12') = '1',
        number_of_columns_to_fill: int = 1,
        mix_after: StringSelection('yes', 'no') = 'yes'):

    if int(destination_columns_start) + number_of_columns_to_fill > 13:
        raise Exception('Invalid destination column selection.')

    # choose pipette and tips
    if transfer_volume > 10:
        tips = labware.load('opentrons-tiprack-300ul', '4')
        pipette = instruments.P10_Multi(mount='right', tip_racks=[tips])
    else:
        tips = labware.load('tiprack-10ul', '4')
        pipette = instruments.P50_Multi(mount='left', tip_racks=[tips])

    # reagent setup
    mix = strips.columns(mix_strip_column)

    # destination setup
    dests = temp_plate.columns(destination_columns_start,
                               length=number_of_columns_to_fill)
    if number_of_columns_to_fill == 1:
        dests = [dests]

    # transfer random priming mix to sample plate
    source = mix[0]
    for dest in dests:
        pipette.pick_up_tip()
        pipette.transfer(transfer_volume,
                         source,
                         dest[0],
                         new_tip='never')
        if mix_after == 'yes':
            pipette.mix(8, pipette.max_volume, dest)
        pipette.drop_tip()
