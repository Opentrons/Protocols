from opentrons import containers, instruments

# standard, sample, and WR volume
vol = 150   # can change here

# 96 well plate for cells (round)
plate = containers.load('96-PCR-flat', 'B1')

# tip rack for p50 pipette
tip200_rack = containers.load('tiprack-200ul', 'D1')

tuberack = containers.load('tube-rack-2ml', 'C2')

# trash to dispose of tips
trash = containers.load('trash-box', 'A2')

# p200 (20 - 100 uL) (single)
p200single = instruments.Pipette(
    axis='b',
    name='p200single',
    max_volume=200,
    min_volume=20,
    channels=1,
    trash_container=trash,
    tip_racks=[tip200_rack])

standards = tuberack.wells('A1', length=9)
samples = tuberack.wells(9, length=3)
wr = tuberack.wells(12)

# 1.Transfer 150μL of each standard from tube rack to the plate (in triplicate)
for row in range(len(standards)):
    p200single.transfer(vol, standards[row], plate.rows(row + 1)[1:4:])

# 2.Transfer 150μL of each sample from tube rack to the plate (in triplicate)
for row in range(len(samples)):
    p200single.transfer(vol, samples[row], plate.rows(row + 1)[5:8:])

# 3.Add 150μL of the working reagent to each well
for row in range(len(standards)):
    p200single.transfer(vol, wr, plate.rows(row + 1)[1:4:])
for row in range(len(samples)):
    p200single.transfer(vol, wr, plate.rows(row + 1)[5:8:])
