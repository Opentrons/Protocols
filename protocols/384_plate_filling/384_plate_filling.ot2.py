from opentrons import instruments, labware
from otcustomizers import StringSelection

metadata = {
    'protocolName': '384 Well Plate Filling',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

# trough and 384-well plate
trough = labware.load('trough-12row', '4', 'trough')
plate = labware.load('384-plate', '2', 'plate')

# 8-channel 10uL pipette, with tip rack and trash
tiprack = labware.load('tiprack-200ul', '1', 'p200rack')


def run_custom_protocol(well_volume: float=1.0, pipette_type: StringSelection(
    'p300-Single', 'p50-Single', 'p10-Single',
        'p300-Multi', 'p50-Multi', 'p10-Multi')='p300-Single'):
    pip_name = pipette_type.split('-')  # Check which pipette type

    if pipette_type == 'p300-Single':
        pipette = instruments.P300_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p50-Single':
        pipette = instruments.P50_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p10-Single':
        pipette = instruments.P10_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p300-Multi':
        pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p50-Multi':
        pipette = instruments.P50_Multi(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p10-Multi':
        pipette = instruments.P10_Multi(
            mount='left',
            tip_racks=[tiprack])

    alternating_wells = []
    for column in plate.cols():
        if pip_name[1] == 'Multi':
            alternating_wells.append(column.wells('A'))
            alternating_wells.append(column.wells('B'))
        else:
            alternating_wells.append(column.wells('A', length=8, step=2))
            alternating_wells.append(column.wells('B', length=8, step=2))

    pipette.distribute(well_volume, trough.wells('A1'), alternating_wells)
