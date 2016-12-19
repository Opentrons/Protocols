"""
Hello Opentrons
"""

# load the Opentrons API
from opentrons import containers, instruments

# load a 200uL tip rack container, placing it in the deck slot A1
tiprack = containers.load('tiprack-200ul', 'A1')

# load a 96 well plate, and place it in the deck slot B1
plate = containers.load('96-flat', 'B1')

# create a pipette, and attach it to the b axis
pipette = instruments.Pipette(axis='b', max_volume=200)

# pick up the tip at A1 of the tip rack
pipette.pick_up_tip(tiprack['A1'])

# transfer 100uL from plate:A1 to plate:A2
pipette.aspirate(100, plate['A1'])
pipette.dispense(100, plate['A2'])

# drop the tip back to the tip rack
pipette.drop_tip(tiprack['A1'])
