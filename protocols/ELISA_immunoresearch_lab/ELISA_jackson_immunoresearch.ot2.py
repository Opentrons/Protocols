from opentrons import instruments, labware, robot

# labware definitions
tips_1000 = labware.load('tiprack-1000ul', '1')
samples = labware.load('tube-rack-2ml', '2')
output = labware.load('96-PCR-flat', '3')
tips_50 = labware.load('tiprack-200ul', '4')
trough = labware.load('trough-12row', '5')
deepwell = labware.load('96-deep-well', '6')

# instrument setup
p50 = instruments.P50_Single(
    tip_racks=[tips_50],
    mount='left')

p1000 = instruments.P1000_Single(
    tip_racks=[tips_1000],
    mount='right')

# reagents and variables setup
# setup for samples + initial two dilutions of 1:100 and 1:2500 in 2ml tuberack
buff = trough.wells('A1')  # location of buffer in trough
sam1 = samples.wells('A1')  # location of concentrated sample 1
sam2 = samples.wells('B1')  # location of concetrated sample 2
s1_dil1 = samples.wells('A2')  # location of 1:100 dilution of sample 1
s2_dil1 = samples.wells('B2')  # location of 1:100 dilution of sample 2
s1_dil2 = samples.wells('A3')  # location of 1:2500 dilution of sample 1
s2_dil2 = samples.wells('B3')  # location of 1:2500 dilution of sample 2

dil1_list = [s1_dil1, s2_dil1]  # locations of both 1:100 dilutions
dil2_list = [s1_dil2, s2_dil2]  # locations of both 1:250 dilutions


# ADD BUFFER TO 2ML RACK, DEEPWELL PLATE, AND OUTPUT PLATE
# add buffer to dilution tubes in 2ml rack (wells A2, B2, A3, B3)
p1000.pick_up_tip()
for dil1, dil2 in zip(dil1_list, dil2_list):
    p1000.transfer(495, buff, dil1, new_tip='never')
    p1000.transfer(960, buff, dil2, new_tip='never')

# add buffer to wells in deepwell (for the other dilutions)
p1000.transfer(1080, buff, deepwell.wells('A1', 'E1', 'C1', 'G1'),
               new_tip='never')

for row in ['A', 'E', 'C', 'G']:
    p1000.transfer(800, buff, deepwell.rows(row)[1:11], new_tip='never')

# add 200 uL buffer to last column in output plate (for controls)
for ind in [0, 2, 4, 6]:
    p1000.transfer(200, buff, output.rows(ind)[11], new_tip='never')
p1000.drop_tip()


# ADD SAMPLES TO BUFFER AND TRANSFER DILUTIONS TO OUTPUT PLATE
for sam, dil1, dil2, dest in zip([sam1, sam2], dil1_list, dil2_list, [0, 4]):
    p50.pick_up_tip()
    p50.transfer(5, sam, dil1, new_tip='never', mix_after=(5, 50))
    p50.transfer(40, dil1, dil2, new_tip='never', mix_after=(5, 50))
    p50.drop_tip()

    p1000.pick_up_tip()
    # make 1:25000 dilution in deepwell col 1, row A and E
    p1000.transfer(120, dil2, deepwell.rows(dest)[0],
                   new_tip='never', mix_after=(5, 500))
    # transfer dilution to output plate col 1, row A/B and E/F
    p1000.transfer(200, deepwell.rows(dest)[0], output.rows(dest)[0],
                   new_tip='never')
    p1000.transfer(200, deepwell.rows(dest)[0], output.rows(dest+1)[0],
                   new_tip='never')
    p1000.drop_tip()

dest_list = [2, 6]
for dil1, dest in zip(dil1_list, dest_list):
    p1000.pick_up_tip()
    # make 1:1000 dilution in deepwell col 1, row C and G
    p1000.transfer(120, dil1, deepwell.rows(dest)[0],
                   new_tip='never', mix_after=(5, 500))
    # transfer dilution to output plate col 1, row C/D and G/H
    p1000.transfer(200, deepwell.rows(dest)[0], output.rows(dest)[0],
                   new_tip='never')
    p1000.transfer(200, deepwell.rows(dest)[0], output.rows(dest+1)[0],
                   new_tip='never')
    p1000.drop_tip()

# complete serial dilutions of samples across deepwell plate
for row in [0, 4, 2, 6]:
    p1000.pick_up_tip()
    for ind in range(0, 11):
        p1000.transfer(400, deepwell.rows(row)[ind], deepwell.rows(row)[ind+1],
                       new_tip='never', mix_after=(5, 500))
        # add dilutions to output 96-well plate before making the next dilution
        p1000.transfer(200, deepwell.rows(row)[ind+1], output.rows(row)[ind+1],
                       new_tip='never')
        p1000.transfer(200, deepwell.rows(row)[ind+1],
                       output.rows(row+1)[ind+1], new_tip='never')
    p1000.drop_tip()
