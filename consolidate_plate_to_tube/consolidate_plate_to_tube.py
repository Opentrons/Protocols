# Explanation:
# Pull 20 uL from each well in a 96 well plate
# and consolidate in one 1.5 mL tube.
# No need to change tips when picking up from a new well.
from opentrons import containers, instruments


plate = containers.load('96-PCR-tall', 'C1')
tube_rack = containers.load('tube-rack-2ml', 'D1')
p200rack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('trash-box', 'B2')

p200 = instruments.Pipette(
    axis='b',
    name='p200',
    max_volume=200,
    tip_racks=[p200rack],
    trash_container=trash
)


def run_custom_protocol(consolidate_volume: float=20.0):
    p200.consolidate(consolidate_volume, plate.wells(), tube_rack.wells('A1'))
