"""
Tips: Dropping

This protocol demonstrates the multiple options
available for removing tips from a pipette
"""

from opentrons import containers, instruments

trash = containers.load('point', 'D2')
tip_rack = containers.load('tiprack-200ul', 'A1')

# create a pipette, and attach the trash containers, allowing
# the pipette to automatically know where to trash tips
pipette = instruments.Pipette(
    axis='b',
    trash_container=trash
)

# grab a tip from position A1, then return it
pipette.pick_up_tip(tip_rack['A1'])
pipette.drop_tip(tip_rack['A1'])

# grab a tip from position A2, then return it using "return_tip"
pipette.pick_up_tip(tip_rack['A2'])
pipette.return_tip()

# grab a tip from position A3, then send it to trash
pipette.pick_up_tip(tip_rack['A3'])
pipette.drop_tip(trash)

# grab a tip from position A4, then send it to trash
pipette.pick_up_tip(tip_rack['A4'])
# no need to specify "trash" container, because it's attached to the pipette
pipette.drop_tip()
