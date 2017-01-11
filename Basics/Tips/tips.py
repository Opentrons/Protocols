"""
Tips

This protocol demonstrates the multiple options
available for controlling tips
"""

from opentrons import containers, instruments

trash = containers.load('point', 'D2')
tip_rack_1 = containers.load('tiprack-200ul', 'B1')
tip_rack_2 = containers.load('tiprack-200ul', 'B2')
tip_rack_3 = containers.load('tiprack-200ul', 'B3')

pipette = instruments.Pipette(axis='a')

pipette.pick_up_tip(tip_rack_1['A1'])  # pick up <tip_rack_1:A1>
pipette.drop_tip(tip_rack_1['A1'])     # drop tip <tip_rack_1:A1>

pipette.pick_up_tip(tip_rack_1['A2'])  # pick up tip_rack_1:A2
pipette.return_tip()                   # return to tip_rack_1:A2

pipette.pick_up_tip(tip_rack_1['A3'])  # pick up tip_rack_1:A3
pipette.drop_tip(trash)                # drop tip in trash

pipette.pick_up_tip(tip_rack_1['A4'])  # pick up tip_rack_1:A4
pipette.move_to(trash)                 # move pipette to the trash
pipette.drop_tip()                     # drop tip at current position

"""
    Automatically iterate through tips and drop tip in trash
    by attaching containers to a pipette
"""

pipette_B = instruments.Pipette(
    axis='b',
    tip_racks=[tip_rack_2, tip_rack_3],
    trash_container=trash
)

pipette_B.pick_up_tip()  # picks up tip_rack_2:A1
pipette_B.return_tip()
pipette_B.pick_up_tip()  # picks up tip_rack_2:A2
pipette_B.drop_tip()     # automatically drops in trash

# use loop to pick up tips tip_rack_2:A3 through tip_rack_3:H12
for i in range(94 + 96):
    pipette_B.pick_up_tip()
    pipette_B.return_tip()
