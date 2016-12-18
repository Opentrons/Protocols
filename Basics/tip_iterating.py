"""
Tip Iterating

This protocol demonstrates attaching tip racks to
a pipette, to allow the pipette to automatically
iterate through tips during a protocol
"""

from opentrons import containers, instruments

# load two 200uL tip rack containers to slots A1 and A2
tip_rack_one = containers.load('tiprack-200ul', 'A1')
tip_rack_two = containers.load('tiprack-200ul', 'A2')

# create a pipette with a list of tip racks attached
pipette_with_tips = instruments.Pipette(
    axis='b',
    tip_racks=[tip_rack_one, tip_rack_two]
)

# command the pipette to pick up the next available tip
pipette_with_tips.pick_up_tip()  # picks up A1
pipette_with_tips.return_tip()
pipette_with_tips.pick_up_tip()  # picks up A2
pipette_with_tips.return_tip()

# use a loop to pick up all remaining tips
for i in range(94 + 96):
    pipette_with_tips.pick_up_tip()
    pipette_with_tips.return_tip()
