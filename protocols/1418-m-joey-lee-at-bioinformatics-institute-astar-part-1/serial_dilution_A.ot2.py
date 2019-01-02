from opentrons import labware, instruments

initial_plate = labware.load('96-flat', '1')
resevoir = labware.load('custom-resevoir', '4')
tiprack = labware.load('opentrons-tiprack-300ul', '2')
tiprack10 = labware.load('tiprack-10ul', '5')
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '3')

m300 = instruments.P300_Multi(mount='left', tip_racks=[tiprack])
p10 = instruments.P10_Single(mount='right', tip_racks=[tiprack10])

pipette.pick_up_tip()
pipette.transfer(
    100,
    resevoir,
    initial_plate.columns('3', '4'),
    new_tip='never')
pipette.transfer(
    120,
    resevoir,
    initial_plate.columns('5', '6'),
    new_tip='never')
pipette.transfer(
    100,
    resevoir,
    initial_plate.columns('7', '8'),
    new_tip='never')
pipette.transfer(
    100,
    resevoir,
    initial_plate.columns('7', '8'),
    new_tip='never')
pipette.drop_tip()
