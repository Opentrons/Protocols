"""
Tips: Basics

This protocol demonstrates automating a 200uL pipette to
pick up a tip from A1 on a tip rack, then immediately
drop the tip back to A1
"""

# load the Opentrons API
from opentrons import containers, instruments

# load a 200uL tip rack container, placing it in the deck slot B1
tip_rack = containers.load('tiprack-200ul', 'B1')

# create a pipette, and attach it to the b axis
pipette = instruments.Pipette(axis='b')

# command the pipette to pick up the tip at A1 of the tip rack
pipette.pick_up_tip(tip_rack['A1'])

# command the pipette to drop the tip back in the same position
pipette.drop_tip(tip_rack['A1'])
