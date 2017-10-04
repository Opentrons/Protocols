from opentrons import containers, instruments

# number of samples
num_samples = 94  # change here

# 96 well plate 1
plate1 = containers.load('96-PCR-flat', 'C1')

# 96 well plate 2
plate2 = containers.load('96-PCR-flat', 'D1')

# tip rack for p300 pipette and p20 pipette
tip200_rack = containers.load('tiprack-200ul', 'E3')
tip200_rack2 = containers.load('tiprack-200ul', 'D2')
tip200_rack3 = containers.load('tiprack-200ul', 'C3')

# trash to dispose of tips
trash = containers.load('trash-box', 'A3')

# trough with solution A and B
trough = containers.load('trough-12row', 'A1')

# tuberack with neg and pos controls
tuberack = containers.load('tube-rack-2ml', 'B2')

# p20 (1 - 20 uL) (single)
p20single = instruments.Pipette(
    axis='b',
    name='p20single',
    max_volume=20,
    min_volume=2,
    channels=1,
    trash_container=trash,
    tip_racks=[tip200_rack3, tip200_rack2])

# p100 (10 - 100 uL) (multi)
p100multi = instruments.Pipette(
    axis='a',
    name='p100multi',
    max_volume=100,
    min_volume=10,
    channels=8,
    trash_container=trash,
    tip_racks=[tip200_rack])

# locations of solutions in trough
solutionA = trough['A1']  # can change here
solutionB = trough['A2']  # can change here

# locations of controls in tubes
neg_control = tuberack['A1']  # can change here
pos_control = tuberack['A2']  # can change here

# wells to put controls in
neg_dest = plate2.wells('H12')  # can change here
pos_dest = plate2.wells('G12')  # can change here

# plate rows
plate1rows = [row for row in plate1.wells(0, to=num_samples, step=8)]
plate2rows = [row for row in plate2.wells(0, to=num_samples, step=8)]

# plate wells
plate1wells = [well for well in plate1.wells(0, to=num_samples)]
plate2wells = [well for well in plate2.wells(0, to=num_samples)]

# Transfer 100 uL of Solution A to all wells of plate(1) with samples
# (same tips), mix before each transfer
p100multi.transfer(100, solutionA, plate1rows, mix_before=(3, 100))

# Transfer 18 uL of solution B to each well that will hold
# samples + solution A and Solution B of a new 96 well plate (2)
p100multi.transfer(18, solutionB, plate2rows)

# Transfer 2 uL from original plate to 18 uL in plate 2 and mix
p20single.transfer(
    2,
    plate1wells,
    plate2wells,
    mix_before=(3, 10),
    mix_after=(3, 10),
    new_tip='always')

# Transfer 2 uL of + and - control tubes to separate wells of 96 well plate (2)
p20single.transfer(2, neg_control, neg_dest)
p20single.transfer(2, pos_control, pos_dest)
