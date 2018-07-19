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
    for col_num in range(1, 11):
        p300.transfer(182, target_plate['A1'], P2.cols(col_num)[1:7],
                      new_tip='never')
p300.drop_tip()

target_list = []
for col_select in range(2, 5):
    target_list.append(['B' + str(col_select), 'B' + str(col_select + 3),
                        'B' + str(col_select + 6)])

source_list = list(P1.rows(0))

cycle_length = len(target_list)
for source_index, source in enumerate(source_list):
    dest = target_list[source_index % cycle_length]
    plate = targets[source_index // cycle_length]
    m50.pick_up_tip()
    for col in dest:
        m50.transfer(30, source, plate.wells(col), new_tip='never')
    m50.drop_tip()

for plate in targets:
    for num in range(1, 11):
        p300.transfer(8, P3.wells('B2'), plate.rows(1)[num], new_tip='always')
