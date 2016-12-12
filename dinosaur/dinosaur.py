from opentrons import robot, containers, instruments

p200rack = containers.load('tiprack-200ul', 'B1')
trough = containers.load('trough-12row', 'C1')
plate = containers.load('96-PCR-flat', 'D1')
trash = containers.load('point', 'D2')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack]
)

sources = {
    1: {
        'source': trough['A1'], # blue food coloring
        'volume': 50
    },
    2: {
        'source': trough['A2'], # green food coloring
        'volume': 50
    }
}

_ = None

plate_image = [
    _, _, _, _, _, _, 2, 1,  # 12
    _, _, _, _, 2, 2, 1, _,  # 11
    _, _, _, _, 2, 1, _, _,  # 10
    _, _, 2, 2, 1, 1, 1, 1,  # 9
    _, _, 2, 1, 1, 1, 1, 1,  # 8
    2, 2, 1, 1, 1, 1, 1, _,  # 7
    _, 2, 1, 1, 1, 1, 1, _,  # 6
    2, 2, 1, 1, 1, 1, 1, _,  # 5
    _, 2, 1, 1, 1, 1, 1, 1,  # 4
    _, _, 2, 1, 1, 1, 1, 1,  # 3
    _, _, _, 1, 1, _, _, _,  # 2
    _, _, _, 1, 1, _, _, _   # 1
]
#   A  B  C  D  E  F  G  H

def spread_sample(key):
    














