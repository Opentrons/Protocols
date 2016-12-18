"""
Tips: Iterating

This protocol demonstrates attaching tip racks to
a pipette, to allow the pipette to automatically
iterate through tips during a protocol
"""

from opentrons import containers, instruments

# load two 200uL tip rack containers,
# placing them at the deck slots A1 and A1
tip_rack_one = containers.load('tiprack-200ul', 'A1')
tip_rack_two = containers.load('tiprack-200ul', 'A2')

# create a pipette, attach it to the b axis,
# and attach a list of tip racks for it to iterate through
pipette = instruments.Pipette(
    axis='b',
    tip_racks=[tip_rack_one, tip_rack_two]
)

# command the pipette to pick up the next available tip
# (will start at A1 of "tip_rack_one")
pipette.pick_up_tip()

# command the pipette to return the tip back to it's origin at A1
pipette.return_tip()

# calling these commands again will automatically shift to
# the tip at position A2 of "tip_rack_one"
pipette.pick_up_tip()
pipette.return_tip()

# doing this in a loop will command the pipette to pick up
# every remaining tip on the deck (starts at A3 of "tip_rack_one")
for i in range(94 + 96):
    pipette.pick_up_tip()
    pipette.return_tip()
