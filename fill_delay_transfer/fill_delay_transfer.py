from opentrons import containers, instruments

#  delay time
delay = 30  # can change here

#  smallest volume
small = 20  # can change here

#  largest volume
large = 55  # can change here

#  volume step
step = 5  # can change here

#  96 well plate1
plate1 = containers.load('96-PCR-flat', 'B1')

#  96 well plate2
plate2 = containers.load('96-PCR-flat', 'C1')

# tip rack for p200 pipette
tip200_rack = containers.load('tiprack-200ul', 'A2')
tip200_rack2 = containers.load('tiprack-200ul', 'E1')

# trash to dispose of tips
trash = containers.load('trash-box', 'A3')

# trough with solutions
trough = containers.load('trough-12row', 'A1')

# p200 (20 - 200 uL) (single)
p200single = instruments.Pipette(
    axis='b',
    name='p200single',
    max_volume=200,
    min_volume=20,
    channels=1,
    trash_container=trash,
    tip_racks=[tip200_rack])

# p300 (50 - 300 uL) (multi)
p300multi = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=300,
    min_volume=50,
    channels=8,
    trash_container=trash,
    tip_racks=[tip200_rack2])

# solution A location
solutionA = trough['A1']  # can change here

# solution B location
solutionB = trough['A5']  # can change here

# volumes into wells
volumes = [v for v in range(small, large + step, step)]

# rows used in the plates
plate1wells = [row for row in plate1.rows('1', to='2')]
plate2wells = [row for row in plate2.rows('1', to='2')]

# transfer 200 uL of solution A into wells A1–H2 of Plate 1 using multi
p300multi.transfer(200, solutionA, plate1wells, new_tip='never')

# transfer 20, 25, 30, 35, 40, 45, 50, and 55 uL of Sample A
# into wells A1-H1 of plate 1 using single
p200single.transfer(volumes, solutionA, plate1wells[0], new_tip='always')

# transfer 20, 25, 30, 35, 40, 45, 50, and 55uL  of Sample B
# into wells A2-H2 of plate 1 using single
p200single.transfer(volumes, solutionB, plate1wells[1], new_tip='always')

# wait 30 minutes
p200single.delay(minutes=delay)

# withdraw all solutions from wells A1–H2 from Plate 1
# and place into wells A1–H2 of Plate 2
p200single.transfer(volumes, plate1wells[0], plate2wells[0], new_tip='always')
p200single.transfer(volumes, plate1wells[1], plate2wells[1], new_tip='always')
