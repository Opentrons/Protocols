from opentrons import instruments, containers

PCR_plate = containers.load('384-plate', 'C1')
sample_plate = containers.load('96-PCR-flat', 'A2')
tiprack = containers.load('tiprack-10ul', 'A1')
tuberack = containers.load('tube-rack-2ml', 'C2')
trash = containers.load('trash-box', 'A3')
trough = containers.load('trough-12row', 'C3')

p10 = instruments.Pipette(
    name='p10',
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=10,
    min_volume=0.5,
    axis='b',
    channels=1,
)

master_volume = 9
dilution_volume = 20
sample_volume = 2
master_mix1 = tuberack['A1']
master_mix2 = tuberack['A2']
H2O_dilute = trough['A1']

dest1 = [well.bottom() for well in PCR_plate.cols('A')]
dest2 = [well.bottom() for well in PCR_plate.cols('C')]
dest3 = [well.bottom() for well in sample_plate.wells('A1', to='H1')]
dest4 = [well.bottom() for well in PCR_plate.cols('A')[:3]]
dest5 = [well.bottom() for well in PCR_plate.cols('C')[:3]]
dest6 = [well.bottom() for well in PCR_plate.cols('A')[3:6]]
dest7 = [well.bottom() for well in PCR_plate.cols('C')[3:6]]
dest8 = [well.bottom() for well in PCR_plate.cols('A')[6:9]]
dest9 = [well.bottom() for well in PCR_plate.cols('C')[6:9]]
dest10 = [well.bottom() for well in PCR_plate.cols('A')[9:12]]
dest11 = [well.bottom() for well in PCR_plate.cols('C')[9:12]]
dest12 = [well.bottom() for well in PCR_plate.cols('A')[12:15]]
dest13 = [well.bottom() for well in PCR_plate.cols('C')[12:15]]
dest14 = [well.bottom() for well in PCR_plate.cols('A')[15:18]]
dest15 = [well.bottom() for well in PCR_plate.cols('C')[15:18]]
dest16 = [well.bottom() for well in PCR_plate.cols('A')[18:21]]
dest17 = [well.bottom() for well in PCR_plate.cols('C')[18:21]]
dest18 = [well.bottom() for well in PCR_plate.cols('A')[21:24]]
dest19 = [well.bottom() for well in PCR_plate.cols('C')[21:24]]


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
