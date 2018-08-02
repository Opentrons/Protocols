from opentrons import containers, instruments

# Modify the name of the container everything you make modifications to the
# defintion below
custom_tray_name = 'new_custom_tray'

"""
Create new container by checking to see if the name is already in the list
https://docs.opentrons.com/ot1/containers.html#create
Refer to the above link to set up your custom container
"""
if custom_tray_name not in containers.list():
    containers.create(
        custom_tray_name,
        grid=(10, 10),  # (num of cols, num of rows)
        spacing=(10, 10),  # spacing between each vial (col, row)
        diameter=10,  # diameter of the vial
        depth=70  # height of the vial
        )

"""
Make sure to update the slots to something like 'A1', 'B1'... depending
on how you would like to set up the deck
"""
tray = containers.load(custom_tray_name, 'A1')  # update slot

tiprack = containers.load('tiprack-10ul', 'B2')  # update slot

trash = containers.load('trash-box', 'C2')  # update slot

p10 = instruments.Pipette(
    axis='b',
    max_volume=10,
    trash_container=trash)

# pipette punctures a vial, holds for 20 minutes, and moves onto the next vial
# until all the vials have been puncture
for each_vial in tray.wells():
    # 10 is the distance in mm from the top of the vial the pipette should go
    p10.move_to(each_vial.top(-10))
    p10.delay(minutes=20)
