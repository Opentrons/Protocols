# pipette: p10; 
# p10rack (A1); PCR sample container: 96-PCR-flat (C2); 
# sample volume: 3ul; number of samples: n; 
# PCR reaction container: 96-PCR-flat (C1); 
# sample loading: duplicated, in the order of A1, A2.....A12, B1....B12. C1.....until n samples loaded into the plate; 
# then continue the same loading for testing another gene; 
# touch tip and change tip each time. Let me know if I miss anything. Thanks for your help.

from opentrons import robot, containers, instruments
from math import ceil

PCR_samples = containers.load('96-PCR-flat','C2','PCR_samples')
reaction_plate = containers.load('96-PCR-flat','C1','reaction_plate')
tiprack = containers.load('tiprack-10ul','A1','tiprack')
trash = containers.load('point','A2','trash')

p10 = instruments.Pipette(
    max_volume = 10,
    min_volume = 1,
    axis = "b",
    name = "p10",
    tip_racks = [tiprack],
    trash_container = trash,
    channels=1
)

num_samples = 15

count = 0
for i in range(8):
    for j in range(12):
        p10.pick_up_tip()
        p10.aspirate(3, PCR_samples.cols[i][j])
        p10.dispense(reaction_plate.cols[i][j]).touch_tip()
        p10.drop_tip()
        count = count + 1
        print(count)
        if count == num_samples:
            break
    if count == num_samples:
            break
            
