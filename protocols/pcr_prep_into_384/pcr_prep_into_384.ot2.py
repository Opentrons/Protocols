#
#
#
from opentrons import instruments, containers, robot

PCR_plate = containers.load('384-plate', '7')
sample_plate = containers.load('96-PCR-flat', '9')
tiprack = containers.load('tiprack-10ul', '10')
tuberack = containers.load('tube-rack-2ml', '11')
trash = robot.fixed_trash
trough = containers.load('trough-12row', '8')

p10 = instruments.Pipette(
    name='p10',
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=10,
    min_volume=0.5,
    mount='right',
    channels=1,
)

master_volume = 9
dilution_volume = 20
sample_volume = 2
master_mix1 = tuberack['A1']
master_mix2 = tuberack['A2']
H2O_dilute = trough['A1']

dest1 = PCR_plate.rows('A')
dest2 = PCR_plate.rows('C')
dest3 = sample_plate.wells('A1', to='H1')
dest4 = PCR_plate.rows('A')[:3]
dest5 = PCR_plate.rows('C')[:3]
dest6 = PCR_plate.rows('A')[3:6]
dest7 = PCR_plate.rows('C')[3:6]
dest8 = PCR_plate.rows('A')[6:9]
dest9 = PCR_plate.rows('C')[6:9]
dest10 = PCR_plate.rows('A')[9:12]
dest11 = PCR_plate.rows('C')[9:12]
dest12 = PCR_plate.rows('A')[12:15]
dest13 = PCR_plate.rows('C')[12:15]
dest14 = PCR_plate.rows('A')[15:18]
dest15 = PCR_plate.rows('C')[15:18]
dest16 = PCR_plate.rows('A')[18:21]
dest17 = PCR_plate.rows('C')[18:21]
dest18 = PCR_plate.rows('A')[21:24]
dest19 = PCR_plate.rows('C')[21:24]


# Transfers specified uL of master mix from specified tube
# to columns A and B
p10.transfer(
    master_volume,
    master_mix1,
    dest1,
    new_tip='once'
)

# Transfers specified uL of master mix from specified tube
# to columns C and D
p10.transfer(
    master_volume,
    master_mix2,
    dest2,
    new_tip='once'
)


# Dilutes all samples with specified amount of H2O
# from specified location to all samples on
# sample plate
p10.transfer(
    dilution_volume,
    H2O_dilute,
    dest3,
    new_tip='always'
)


# Dispenses specified amount of samples from sample plate to PCR plate.
# Each sample is dispensed to 3 consecutive wells along the column
p10.transfer(
    sample_volume,
    sample_plate.wells('A1'),
    dest4,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('A1'),
    dest5,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('B1'),
    dest6,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('B1'),
    dest7,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('C1'),
    dest8,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('C1'),
    dest9,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('D1'),
    dest10,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('D1'),
    dest11,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('E1'),
    dest12,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('E1'),
    dest13,
    new_tip='always'
)


p10.transfer(
    sample_volume,
    sample_plate.wells('F1'),
    dest14,
    new_tip='always'
)

p10.transfer(
    sample_volume,
    sample_plate.wells('F1'),
    dest15,
    new_tip='always'
)

p10.transfer(
    sample_volume,
    sample_plate.wells('G1'),
    dest16,
    new_tip='always'
)

p10.transfer(
    sample_volume,
    sample_plate.wells('G1'),
    dest17,
    new_tip='always'
)

p10.transfer(
    sample_volume,
    sample_plate.wells('H1'),
    dest18,
    new_tip='always'
)

p10.transfer(
    sample_volume,
    sample_plate.wells('H1'),
    dest19,
    new_tip='always'
)
