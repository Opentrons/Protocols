from opentrons import containers, instruments

plate = containers.load('96-flat', 'B1')

# to move liquide, first create a pipette with a maximum volume
pipette = instruments.Pipette(
    axis='b',
    max_volume=200
)

pipette.aspirate(50, plate['A1'])
pipette.aspirate(50)
pipette.aspirate(plate['A2'])

pipette.dispense(50, plate['B1'])
pipette.dispense(50)
pipette.dispense(plate['B2'])
