from opentrons import containers, instruments


# 96-well plate and tube rack
plate = containers.load('96-PCR-tall', 'C1')
tube_rack = containers.load('tube-rack-2ml', 'D1')

# 1-channel 200uL pipette, with tip rack and trash
p200rack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('point', 'B2')
p200 = instruments.Pipette(
    axis='b',
    name='p200',
    max_volume=200,
    tip_racks=[p200rack],
    trash_container=trash
)

p200.consolidate(20, plate.wells(), tube_rack.wells('A1'))
