from opentrons import instruments, labware

# trough and 384-well plate
trough = labware.load('trough-12row', '2', 'trough')
plate = labware.load('384-plate', '3', 'plate')

# 8-channel 10uL pipette, with tip rack and trash
tiprack = labware.load('tiprack-200ul', '1', 'p200rack')
p10 = instruments.P10_Multi(
    mount='left',
    tip_racks=[tiprack],
)


def run_custom_protocol(well_volume: float=1.0):
    alternating_wells = []
    for col in plate.cols():
        alternating_wells.append(col.wells('A', length=8, step=2))
        alternating_wells.append(col.wells('B', length=8, step=2))

    p10.distribute(well_volume, trough.wells('A1'), alternating_wells)