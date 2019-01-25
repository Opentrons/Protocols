from opentrons import labware, instruments, robot

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

# labware setup
reservior = labware.load(reservoir_name, '6').wells('A1')
tiprack = labware.load(tiprack_name, '9')

# instruments setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
        tip_column: str=1,
        number_of_plates: int=9):

    plates = [labware.load('384-plate', slot)
              for slot in ['1', '2', '3', '4', '5', '7', '8', '10', '11']][
              :number_of_plates]

    m50.pick_up_tip(tiprack.cols(tip_column))
    for plate in plates:
        for col in plate.cols():
            for index in range(2):
                m50.transfer(50, reservior, col[index], new_tip='never')
    m50.retract()

    robot.pause('Insert plates into light cabinet. Remove solution and wash \
    plates. Dry plate and place the plates back in the robot. Make sure to \
    load reagent 2 in slot 6.')

    for plate in plates:
        for col in plate.cols():
            for index in range(2):
                m50.transfer(50, reservior, col[index], new_tip='never')
    m50.retract()

    robot.pause('Insert plates into light cabinet. Remove solution and wash \
    plates. Dry plate and place the plates back in the robot. Make sure to \
    load reagent 3 in slot 6.')

    for plate in plates:
        for col in plate.cols():
            for index in range(2):
                m50.transfer(50, reservior, col[index], new_tip='never')
    m50.drop_tip()
