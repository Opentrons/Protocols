from opentrons import labware, instruments

# labware setup
plate_deep = labware.load('96-deep-well', '2')
microtiter_plate = labware.load('96-flat', '8')
trough = labware.load('trough-12row', '11')

tiprack_10 = labware.load('tiprack-10ul', '4')
tiprack1_300 = labware.load('tiprack-200ul', '7')
tiprack2_300 = labware.load('tiprack-200ul', '10')

# reagent setup
media = trough.wells('A1')
media_s = trough.wells('A2')

# pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10]
    )

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack1_300, tiprack2_300]
    )

# transfer media to microtiter plate
target_cols = microtiter_plate.cols(
    ['1', '2', '3', '4', '7', '10', '11', '12'])
for col in target_cols:
    m300.transfer(200, media, col, new_tip='always')

m300.start_at_tip(tiprack2_300.cols('1'))

# transfer media + S to microtiter plate
target_cols = microtiter_plate.cols(
    ['1', '2', '3', '5', '6', '8', '9', '10', '11', '12'])
for col in target_cols:
    m300.transfer(200, media_s, col, new_tip='always')

for index, well in enumerate(microtiter_plate.cols('1')[:'H']):
    p10.transfer(2, well, plate_deep.rows(index)[0:3])
    if index == 0:
        p10.transfer(2, well, plate_deep.rows(7)[0:3])

for index, well in enumerate(microtiter_plate.cols('2')):
    p10.transfer(2, well, plate_deep.rows(index)[3:6])

for index, well in enumerate(microtiter_plate.cols('3')):
    p10.transfer(2, well, plate_deep.rows(index)[6:9])

for index, well in enumerate(microtiter_plate.cols('4')['B':'H']):
    p10.transfer(2, well, plate_deep.rows(index+1)[:8:-1])
