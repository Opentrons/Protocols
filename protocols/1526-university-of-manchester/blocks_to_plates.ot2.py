from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Protein Crystallization Screen',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'swissci-crystallography-plate'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.35,
        depth=5.8,
        volume=40,
    )

block_name = 'starlab-96-deep-well-block'
if block_name not in labware.list():
    labware.create(
        block_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.4,
        depth=42.2,
        volume=2200
    )

# load labware
plates = [labware.load(plate_name, slot)
          for slot in ['1', '2', '3', '4', '5', '6', '8', '9', '11']]

block = labware.load(block_name, '7')

tips = labware.load('opentrons-tiprack-300ul', '10')

# load pipette
m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tips]
)
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tips]
)


def run_custom_protocol(
        number_of_full_decks: int = 2,
        volume_of_transfer: float = 30.0,
        pipette_type: StringSelection('P50-Multi', 'P300-Multi') = 'P50-Multi'
        ):
    def perform_deck_transfer(vol):
        for ind, source_col in enumerate(block.cols()):
            source = source_col[0]
            pipette.pick_up_tip(tips.cols(ind))
            for plate in plates:
                pipette.aspirate(vol, source)
                pipette.move_to(source_col[0].top(1))
                pipette.delay(seconds=10)
                offset = source_col[0].from_center(h=0.9, r=1.0, theta=0)
                touch_dest = (source_col[0], offset)
                robot.head_speed(x=50, y=50, z=50, a=50)
                pipette.move_to(touch_dest, strategy='direct')
                robot.head_speed(x=600, y=400, z=125, a=125)
                dest = plate.cols(ind)[0]
                pipette.dispense(vol, dest)
            pipette.drop_tip()

    # select pipette
    if pipette_type == 'P50-Multi':
        pipette = m50
    else:
        pipette = m300
    pipette.set_flow_rate(aspirate=10, dispense=20)

    # perform transfers
    perform_deck_transfer(volume_of_transfer)
    for i in range(number_of_full_decks-1):
        robot.pause("Please replace plates in slots 1, 2, 3, 4, 5, 6, 8, 9, "
                    "and 11, and tip rack in slot 10 before resuming.")
        perform_deck_transfer(volume_of_transfer)        