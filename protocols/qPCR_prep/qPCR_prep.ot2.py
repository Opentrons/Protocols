from opentrons import containers, instruments

# tube rack holding reagents
reagents = containers.load('tube-rack-2ml', '4')
dna = containers.load('tube-rack-2ml', '5')

# 96 well plate
qpcr_plate = containers.load('96-PCR-tall', '6')

# tip rack for p50 pipette and p20 pipette
tip200_rack = containers.load('tiprack-200ul', '1')
tip200_rack2 = containers.load('tiprack-200ul', '2')

# p20 (2 - 20 uL) (single)
p20single = instruments.Pipette(
    mount='right',
    name='p20single',
    max_volume=20,
    min_volume=2,
    channels=1,
    tip_racks=[tip200_rack])

# p50 (5 - 50 uL) (multi)
p50multi = instruments.Pipette(
    mount='left',
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tip200_rack2])

water = reagents.wells('A1')
f_primer = reagents.wells('A2', length=8)
r_primer = reagents.wells('A4', length=8)
mix_2x = reagents.wells('B1')
samples = dna.wells('A1', length=8)

# Use a single channel to transfer 76 uL of water from a 1.5 ml tube to wells
# A1 through H1 ( column 1, 8 samples, same tip).
p20single.transfer(76, water, qpcr_plate.cols(0))

# Use a single channel to add 2 uL of foward primer to each of wells A1
# through H1 (column 1, 8 samples, change tips between primers)
p20single.transfer(2, f_primer, qpcr_plate.cols(0), new_tip='always')

# Use a single channel to add 2 uL of reverse primer to each of wells A1
# through H1 (column 1, 8 samples, change tips between primers)
p20single.transfer(2, r_primer, qpcr_plate.cols(0), new_tip='always')

# Use a single channel to add 120 uL of 2X master mix to each of wells A1
# through H1 (column 1, 8 samples, change tips between samples
p20single.transfer(2, mix_2x, qpcr_plate.cols(0), new_tip='always')

# Using a multi channel pipettor, move 50 uL of column 1 to column 4, 50 uL of
# column 1 to column 7, and 50 uL of column 1 to column 10.
p50multi.transfer(
    50,
    qpcr_plate.cols(0),
    qpcr_plate.cols(3, 6, 9),
    new_tip='always')

# Using a single channel pipettor add 10 uL of DNA from 1.5 ml centrifuge tubes
# to wells A1, A4, A7, A10, B1, B4, B7, B10, etc.
# change tips between each sample.
sample_positions = []
for row in qpcr_plate.rows():
    sample_positions.append(row[0:10:3])

for sample in range(0, 8):
    p20single.distribute(10, samples[sample], sample_positions[sample])

# Using a multi channel pipettor mix column 1 and move 20 uL of
# column 1 to column 2, then 20 uL of column 1 to column 3.
p50multi.transfer(
    20,
    qpcr_plate.cols(0),
    qpcr_plate.cols(1, 2),
    mix_before=(3, 50))

# Replace tip. Using a multi channel pipettor mix column 4 and move 20 uL of
# column 4 to column 5, then 20 uL of column 4 to column 6.
p50multi.transfer(
    20,
    qpcr_plate.cols(3),
    qpcr_plate.cols(4, 5),
    mix_before=(3, 50))

# Replace tip. Using a multi channel pipettor mix column 7 and move 20 uL of
# column 7 to column 8, then 20 uL of column 7 to column 9.
p50multi.transfer(
    20,
    qpcr_plate.cols(6),
    qpcr_plate.cols(7, 8),
    mix_before=(3, 50))

# Replace tip. Using a multi channel pipettor mix column 10 and move 20 uL of
# column 10 to column 11, then 20 uL of column 10 to column 12.
p50multi.transfer(
    20,
    qpcr_plate.cols(9),
    qpcr_plate.cols(10, 11),
    mix_before=(3, 50))
