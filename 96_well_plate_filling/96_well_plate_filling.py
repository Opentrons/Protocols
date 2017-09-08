from opentrons import containers, instruments

# change well_volume to set the final volume of all wells in the 96-well plate
well_volume = 100

plate = containers.load('96-flat', 'A1')

trough = containers.load('point', 'C1')
source = trough.wells(0)

tiprack = containers.load('tiprack-200ul', 'A2')
trash = containers.load('trash-box', 'C2')

# you may also want to change min and max volume of the pipette
pipette = instruments.Pipette(
    max_volume=200,
    min_volume=20,
    axis='a',
    channels=8,
    tip_racks=[tiprack],
    trash_container=trash)


row_vols = [0 for row in plate.rows()]

pipette.pick_up_tip()

for row_num, destination_row in enumerate(plate.rows()):
    while row_vols[row_num] < well_volume:
        transfer_volume = min(
            pipette.max_volume,
            well_volume-row_vols[row_num])

        pipette.aspirate(transfer_volume, source)
        pipette.dispense(transfer_volume, destination_row)
        pipette.touch_tip(destination_row)
        row_vols[row_num] += transfer_volume

    pipette.blow_out(trash)


pipette.drop_tip()
