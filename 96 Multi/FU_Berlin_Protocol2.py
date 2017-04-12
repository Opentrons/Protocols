from opentrons import containers, instruments


p200rack = containers.load('tiprack-200ul', 'D2')
trash = containers.load('trash-box', 'E2')
trough = containers.load('trough-12row', 'C2')
plate1 = containers.load('96-PCR-flat', 'A1')
plate2 = containers.load('96-PCR-flat', 'A2')
plate3 = containers.load('96-PCR-flat', 'B1')
plate4 = containers.load('96-PCR-flat', 'B2')
plate5 = containers.load('96-PCR-flat', 'C1')
plate6 = containers.load('96-PCR-flat', 'D1')
plate7 = containers.load('96-PCR-flat', 'E1')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    tip_racks=[p200rack],
    trash_container=trash
)

plate_slots = ['A1', 'A2', 'B1', 'B2', 'C1', 'D1', 'E1']
plate_type = '96-PCR-flat'

plate = [containers.load(plate_type, slot) for slot in plate_slots]

# dispense 100 uL from trough to plate
for plate in plates:
    p200.transfer(
        100,
        trough.wells('A1'),
        plate.wells('A1', length=12),
        new_tips='once'
    )