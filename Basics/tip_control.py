"""
Tip Control

This protocol demonstrates the multiple options
available for removing tips from a pipette
"""

from opentrons import containers, instruments

trash = containers.load('point', 'D2')
tip_rack = containers.load('tiprack-200ul', 'A1')

pipette = instruments.Pipette(axis='b')

# grab a tip from position A1, then return it
pipette.pick_up_tip(tip_rack['A1'])
pipette.drop_tip(tip_rack['A1'])

# grab a tip from position A2, then return it using "return_tip"
pipette.pick_up_tip(tip_rack['A2'])
pipette.return_tip()

# grab a tip from position A3, then send it to trash
pipette.pick_up_tip(tip_rack['A3'])
pipette.drop_tip(trash)

# grab a tip from position A4, then send it to trash automatically
pipette_with_trash = instruments.Pipette(
    axis='a',
    trash_container=trash
)
pipette_with_trash.pick_up_tip(tip_rack['A4'])
pipette_with_trash.drop_tip()
