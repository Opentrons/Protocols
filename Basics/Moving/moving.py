"""
Moving

Demonstrates the different ways to control the movement
of the Opentrons liquid handler during a protocol run
"""

from opentrons import robot, containers, instruments

tiprack = containers.load('tiprack-200ul', 'A1')
plate = containers.load('96-flat', 'B1')

pipette = instruments.Pipette(axis='b')

pipette.move_to(tiprack['A1'])

pipette.move_to(tiprack['A2'].bottom())

pipette.move_to(plate['A3'].top())
pipette.delay(2)
pipette.move_to(plate['A4'].bottom(2))
pipette.delay(2)
pipette.move_to(plate['A5'].top(-2))

# robot.home()
robot.home(enqueue=True)
robot.home('z', enqueue=True)
