from opentrons import containers, instruments


p1000rack = containers.load('tiprack-1000ul', 'A1')
vialrack = containers.load('wheaton_vial_rack', 'D1')
plate = containers.load('96-deep-well', 'B1')
trash = containers.load('trash-box', 'B2')

p1000 = instruments.Pipette(
    axis='b',
    min_volume=100,
    max_volume=1000,
    trash_container=trash,
    tip_racks=[p1000rack]
)

row_length = len(plate.rows(0))


# Distribute 48 samples to 96 well plate (2 wells at a time up the columns)
def run_custom_protocol(transfer_volume: float=300):
    for i in range(48):
        dest_index = (i % row_length) + (int(i / row_length) * row_length * 2)
        p1000.distribute(
            transfer_volume,
            vialrack.wells(i),
            plate.wells(dest_index, length=2, skip=8))
