from opentrons import containers, instruments


p200rack = containers.load('tiprack-200ul', 'B1', 'tiprack')
trough = containers.load('trough-12row', 'C1', 'trough')
plate = containers.load('96-PCR-flat', 'D1', 'plate')
trash = containers.load('point', 'D2', 'trash')

p200 = instruments.Pipette(
    name="p200",
    axis="b",
    min_volume=20,
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack]
)

p200.distribute(
    50,
    trough['A1'],
    plate.wells(
        'D1', 'E1', 'D2', 'E2', 'D3', 'E3', 'F3', 'G3',
        'H3', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'C5',
        'D5', 'E5', 'F5', 'G5', 'C6', 'D6', 'E6', 'F6',
        'G6', 'C7', 'D7', 'E7', 'F7', 'G7', 'D8', 'E8',
        'F8', 'G8', 'H8', 'E9', 'F9', 'G9', 'H9', 'F10',
        'G11', 'H12', 'F3', 'G3'),
    trash=False)

# deposit to all GREEN wells
p200.distribute(
    50,
    trough['A2'],
    plate.wells(
        'C3', 'B4', 'A5', 'B5', 'B6', 'A7', 'B7',
        'C8', 'C9', 'D9', 'E10', 'E11', 'F11', 'G12'),
    trash=False)
