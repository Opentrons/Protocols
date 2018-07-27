from opentrons import instruments, labware

plate_96 = labware.load('96-flat', 1)

plate_384 = labware.load('384-plate', 4)

tiprack_10ul = labware.load('tiprack-10ul', 5)
tiprack_300ul = labware.load('opentrons-tiprack-300ul', 2)

tuberack = labware.load('tube-rack-2ml', 3)

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_10ul]
)

s50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_300ul]
)

for i in range(0, 2):
    m10.distribute(3, plate_96(i), plate_384.rows(i))

target = {}

for i in range(0, 8):
    target[i] = []
    for j in range(0, 16*3):
        target_well = plate_384.wells(j+16*3*i)
        target[i].append((target_well, target_well.from_center(x=1, y=0, z=0)))

count = 0
for i in range(0, 8):
    s50.pick_up_tip()
    for j in target[i]:
        if count == 0: 
            s50.aspirate(42, tuberack.wells(i))           
            count += 1
        elif count == 5: 
            count = 0
        else:   
            count += 1
        s50.dispense(7, j)
    s50.drop_tip()