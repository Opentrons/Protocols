from opentrons import labware, instruments

tiprack_1 = labware.load('tiprack-200ul', 7)
tiprack_2 = labware.load('tiprack-200ul', 8)
tipracks = [tiprack_1, tiprack_2]

trough = labware.load('tube-rack-15_50ml', 9)

P1 = labware.load('96-flat', 1)  # Chemicals
P2 = labware.load('96-flat', 2)  # Plate taking in chemical CP1
P3 = labware.load('96-flat', 3)  # Samples
P4 = labware.load('96-flat', 4)  # Plate taking in chemical CP2
P5 = labware.load('96-flat', 5)  # Plate taking in checmial CP3
P6 = labware.load('96-flat', 6)  # Plate taking in chemical CP4

m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=tipracks)

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=tipracks)

targets = [P2, P4, P5, P6]

p300.pick_up_tip()
for target_plate in targets:
    for i in range(1, 11):
        p300.transfer(182, target_plate['A1'], P2.cols(i)[1:7],
                      new_tip='never')
p300.drop_tip()

target_list = []
for i in range(2, 5):
    target_list.append(['B' + str(i), 'B' + str(i + 3), 'B' + str(i + 6)])

source_list = list(P1.rows(0))

for i in range(len(source_list)):
    if i % 3 == 1:
        dest = target_list[1]
    elif i % 3 == 2:
        dest = target_list[2]
    else:
        dest = target_list[0]
    if i // 3 == 0:
        plate = targets[0]
    elif i // 3 == 1:
        plate = targets[1]
    elif i // 3 == 2:
        plate = targets[2]
    else:
        plate = targets[3]
    m50.pick_up_tip()
    for col in dest:
        m50.transfer(30, source_list[i], plate.wells(col), new_tip='never')
    m50.drop_tip()

for num in range(1, 11):
    p300.transfer(8, P3.wells('B2'), P3.rows(1)[num], new_tip='always')
