from opentrons import containers, instruments


trough = containers.load('trough-12row', 'D2', 'trough')
plate = containers.load('96-PCR-flat', 'C1', 'plate')

p200Mrack = containers.load('tiprack-200ul', 'A1', 'p200M-rack')
trash = containers.load('point', 'B2', 'trash')

p200M = instruments.Pipette(
    name="p200M",
    trash_container=trash,
    tip_racks=[p200Mrack],
    min_volume=20,
    max_volume=200,
    axis="a",
    channels=8
)

dilution_number = 6
sample_volume = 20
diluent_volume = 180

p200M.distribute(
    diluent_volume,
    trough['A1'],
    plate.rows[1:dilution_number + 1]
)

p200M.transfer(
    sample_volume,
    plate.rows[:dilution_number],
    plate.rows[1:dilution_number + 1],
    mix_after=(3, sample_volume)
)
