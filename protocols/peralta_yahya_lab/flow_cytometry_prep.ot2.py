from opentrons import labware, instruments

# labware setup
tiprack_1 = labware.load('tiprack-200ul', '7')
tiprack_2 = labware.load('tiprack-200ul', '8')
tipracks = [tiprack_1, tiprack_2]

trough = labware.load('tube-rack-15_50ml', '9')

P1 = labware.load('96-flat', '1')  # Chemicals
P2 = labware.load('96-flat', '2')  # Plate taking in chemical CP1
P3 = labware.load('96-deep-well', '3')  # Samples
P4 = labware.load('96-flat', '4')  # Plate taking in chemical CP2
P5 = labware.load('96-flat', '5')  # Plate taking in checmial CP3
P6 = labware.load('96-flat', '6')  # Plate taking in chemical CP4

# pipette setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=tipracks)

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=tipracks)


targets = [P2, P4, P5, P6]

# Transfer media to all of the target plates
p300.pick_up_tip()
for target_plate in targets:
    for col_num in range(1, 11):
        p300.transfer(182, trough['A1'], target_plate.cols(col_num)[1:7],
                      new_tip='never')
p300.drop_tip()

# Add destinations of chemical 1(x), 2(x+1), 3(x+2), 4(x)...12(x+2)
target_list = []
for plate in targets:
    # chemical x: Col B2, B5, B8
    target_list.append(plate.rows('B')('2', to='8', step=3))
    # chemcal x+1: Col B3, B6, B9
    target_list.append(plate.rows('B')('3', to='9', step=3))
    # chemical x+2: Col B4, B7, B10
    target_list.append(plate.rows('B')('4', to='10', step=3))


source_list = list(P1.rows(0))

# Transfer chemicals from each column of the chemical plate to
# the destination defined by the target_list
for source, target_plate in zip(source_list, target_list):
    m50.pick_up_tip()
    m50.aspirate(30, source)
    for target_column in target_plate:
        m50.dispense(10, target_column)
    m50.drop_tip()

# Deposit cells to the target plates
for plate in targets:
    for num in range(1, 11):
        p300.transfer(8, P3.wells('B2'), plate.rows(1)[num], new_tip='always')
