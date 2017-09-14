from opentrons import robot, containers, instruments


cooldeck = containers.load('alum-block-pcr-strips', 'D3')
compounds_plate = containers.load('96-PCR-flat', 'E3')
dilution_plate = containers.load('384-plate', 'E2')
assay_plate = containers.load('384-plate', 'C1')
DMSO = containers.load('trough-12row', 'E1')
reagents = containers.load('trough-12row', 'C2')

p1000rack = containers.load('tiprack-1000ul', 'A2')
p20rack = containers.load('tiprack-10ul', 'A1')
trash = containers.load('trash-box', 'A3')

p1000 = instruments.Pipette(   
        axis="b",
        max_volume=1000,
        min_volume=100,
        tip_racks=[p1000rack],
        trash_container=trash
)
p10 = instruments.Pipette(   
        axis="a",
        max_volume=10,
        min_volume=1,
        tip_racks=[p20rack],
        trash_container=trash,
        channels=8
)


# create our list of rows for the 8-channel pipette to step through
alternate_dilution_columns = [
    row.wells(col, length=8, step=2)
    for row in dilution_plate.rows('1', to='22')
    for col in 'AB'
]

alternate_assay_columns = [
    row.wells(col, length=8, step=2)
    for row in dilution_plate.rows('1', to='22')
    for col in 'AB'
]

# transfer to first 22 rows of plate
p10.transfer(10, DMSO.wells('A1'), alternate_dilution_columns)

# add compounds to first row
p10.transfer(
    10,
    compounds_plate.rows('1'),
    dilution_plate.wells('A1', length=8, step=2),
    mix_after=(10, 3))

p10.transfer(
    10,
    compounds_plate.rows('2'),
    dilution_plate.wells('B1', length=8, step=2),
    mix_after=(10, 3))

# dilute compound up the plate's columns
p10.transfer(
    10,
    alternate_dilution_columns[:-2],  # ignore last row
    alternate_dilution_columns[2:],   # ignore first row
    mix_after=(10, 3)
)

# add reagents to assay plate
p1000.distribute(58.8, reagents.wells('A1'), assay_plate.wells('A1', to='P22'))

# add diluted compunds to assay plate
p10.transfer(1.2, alternate_dilution_columns, alternate_assay_columns)

# add reagents to empty row on assay plate
p1000.distribute(60, reagents.wells('A1'), assay_plate.rows('23'))

# add contents of cold deck to final empty row in assay plate
p1000.distribute(60, cooldeck.wells('A1'), assay_plate.rows('24'))
