from opentrons import instruments, containers
from otcustomizers import StringSelection

# trough and 384-well plate
trough = containers.load('trough-12row', 'E1', 'trough')
plate = containers.load('384-plate', 'C1', 'plate')

# 8-channel 10uL pipette, with tip rack and trash
tiprack = containers.load('tiprack-200ul', 'A1', 'p200rack')
trash = containers.load('trash-box', 'B2', 'trash')


def run_custom_protocol(well_volume: float=1.0, pipette_type: StringSelection(
    'p300-Single', 'p50-Single', 'p10-Single',
        'p300-Multi', 'p50-Multi', 'p10-Multi')='p50-Multi'):
    pip_name = pipette_type.split('-')  # Check which pipette type
    chan = 1  # Number of channels
    if pip_name[1] == 'Multi':
        chan = 8
    vol = int(pip_name[0][1::])
    pipette = instruments.Pipette(
        max_volume=vol,
        tip_racks=[tiprack],
        channels=chan,
        trash_container=trash)

    alternating_wells = []
    for row in plate.rows():
        if pip_name[1] == 'Multi':
            alternating_wells.append(row.wells('A'))
            alternating_wells.append(row.wells('B'))
        else:
            alternating_wells.append(row.wells('A', length=8, step=2))
            alternating_wells.append(row.wells('B', length=8, step=2))

    pipette.distribute(
        well_volume,
        trough.wells('A1'),
        alternating_wells,
        mix_before=(5, pipette.max_volume))
