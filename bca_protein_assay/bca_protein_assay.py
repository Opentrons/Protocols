from opentrons import containers, instruments

# solutions in trough
trough = containers.load('trough-12row', 'A2')

# tube racks holding reagents
standards_unknowns = containers.load('tube-rack-.75ml', 'A1')
solutions = containers.load('tube-rack-15_50ml', 'A3')

# 96 well plate
plate = containers.load('96-PCR-flat', 'C1')

# tip rack for p10 and p50 pipette
tip200_rack = containers.load('tiprack-200ul', 'E3')
tip200_rack2 = containers.load('tiprack-200ul', 'C2')

# trash to dispose of tips
trash = containers.load('trash-box', 'C3')

# p20 (2 - 20 uL) (single)
p20single = instruments.Pipette(
    axis='b',
    name='p20',
    max_volume=20,
    min_volume=2,
    channels=1,
    trash_container=trash,
    tip_racks=[tip200_rack2])

# p300 (50 - 300 uL) (multi)
p300multi = instruments.Pipette(
    axis='a',
    name='p300',
    max_volume=300,
    min_volume=50,
    channels=8,
    trash_container=trash,
    tip_racks=[tip200_rack])

# reagent locations
water = trough['A1']
buffer = trough['A2']
unknownA = standards_unknowns.wells(7)
unknownB = standards_unknowns.wells(8)
BCA = solutions.wells('A1')

# list of where to pipette standards A-G (7)
standard_wells = []
for standard in range(0, 7):
    standard_wells.append(plate.wells(standard, length=2, step=8))

# wells A3-D3 and A4-D4
wells3_4 = []
wells3_4.append(plate.wells('A3', length=4))
wells3_4.append(plate.wells('A4', length=4))

# add 15uL of H2O from trough into 96plate wells A3-D3, A4-D4
p20single.transfer(15, water, wells3_4)

# add 10uL of Buffer from trough into 96plate wells A1-H1, A2-H2
p300multi.transfer(10, buffer, plate.rows(0, length=2))

# add 8uL of Buffer from trough into 96plate wells A3-D3
p20single.transfer(8, buffer, wells3_4[0])

# add 5uL of Buffer from trough into 96plate wells A4-D4
p20single.transfer(5, buffer, wells3_4[1])

# add 15ul of standard A from 0.75mL tube rack into 96plate wells A1-2
# add 15ul of standard B from 0.75mL tube rack into 96plate wells B1-2
# add 15ul of standard C from 0.75mL tube rack into 96plate wells C1-2
# add 15ul of standard D from 0.75mL tube rack into 96plate wells D1-2
# add 15ul of standard E from 0.75mL tube rack into 96plate wells E1-2
# add 15ul of standard F from 0.75mL tube rack into 96plate wells F1-2
# add 15ul of standard G from 0.75mL tube rack into 96plate wells G1-2
for standard in range(0, 7):
    p20single.transfer(
        15, standards_unknowns.wells(standard), standard_wells[standard])

# add 2uL of Unknown A from 0.75mL tube rack into 96plate wells A-3, B-3
p20single.transfer(2, unknownA, wells3_4[0][0:2])
# add 5uL of Unknown A from 0.75mL tube rack into 96plate wells A-4, B-4
p20single.transfer(2, unknownA, wells3_4[1][0:2])
# add 5uL of Unknown B from 0.75mL tube rack into 96plate wells C-4, D-4
p20single.transfer(2, unknownB, wells3_4[1][2:4])
# add 2uL of Unknown B from 0.75mL tube rack into 96plate wells C-3, D-3
p20single.transfer(2, unknownB, wells3_4[0][2:4])

# add 200uL of BCA solution from 15mL tube tube rack
# into 96plate wells A1 through H4
for row in range(0, 4):
    p20single.transfer(200, BCA, plate.rows(row))
