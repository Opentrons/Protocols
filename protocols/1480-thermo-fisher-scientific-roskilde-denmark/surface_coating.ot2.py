from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Surface Coating Protocol',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

tiprack_name = 'finntip-tiprack-300ul'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=52)

reservoir_name = 'nalgene-diposable-300ml-reservior'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=86,
        depth=43)

plate_name_96 = 'Nunc-96-well'
if plate_name_96 not in labware.list():
    labware.create(
        plate_name_96,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=11.3)

# labware setup
reservior = labware.load(reservoir_name, '6').wells('A1')
tiprack = labware.load(tiprack_name, '9')


def run_custom_protocol(
        pipette_type: StringSelection(
            'P300-Single', 'P50-Multi', 'P300-Multi') = 'P300-Multi',
        pipette_mount: StringSelection('left', 'right') = 'left',
        starting_tip: str = 'A1',
        plate_type: StringSelection('96-well', '384-well') = '384-well',
        number_of_plates: int = 9,
        volume: float = 50):

    # instruments setup
    pipette_args = {'mount': pipette_mount, 'tip_racks': [tiprack]}

    if pipette_type == 'P300-Single':
        pipette = instruments.P300_Single(**pipette_args)
    elif pipette_type == 'P50-Multi':
        pipette = instruments.P50_Multi(**pipette_args)
    else:
        pipette = instruments.P300_Multi(**pipette_args)

    mode = pipette_type.split('-')[1]

    if plate_type == '384-well':
        name = '384-plate'
    else:
        name = plate_name_96
    plates = [labware.load(name, slot)
              for slot in ['1', '2', '3', '4', '5', '7', '8', '10', '11']][
              :number_of_plates]

    if mode == 'Single':
        pipette.start_at_tip(tiprack.wells(starting_tip))
        dests = [well for plate in plates for well in plate]
    else:
        starting_col = starting_tip[1:]
        pipette.start_at_tip(tiprack.cols(starting_col))
        if plate_type == '384-well':
            dests = [well for plate in plates for letter in ['A', 'B']
                     for well in plate.rows(letter)]
        else:
            dests = [well for plate in plates for well in plate.rows('A')]

    pipette.pick_up_tip()
    pipette.distribute(volume,
                       reservior,
                       dests,
                       disposal_vol=0,
                       new_tip='never')
    pipette.retract()

    robot.pause('Insert plates into light cabinet. Remove solution and wash \
    plates. Dry plate and place the plates back in the robot. Make sure to \
    load reagent 2 in slot 6.')

    pipette.distribute(volume,
                       reservior,
                       dests,
                       disposal_vol=0,
                       new_tip='never')
    pipette.retract()

    robot.pause('Insert plates into light cabinet. Remove solution and wash \
    plates. Dry plate and place the plates back in the robot. Make sure to \
    load reagent 3 in slot 6.')

    pipette.distribute(volume,
                       reservior,
                       dests,
                       disposal_vol=0,
                       new_tip='never')
    pipette.drop_tip()
