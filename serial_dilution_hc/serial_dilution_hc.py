from opentrons import containers, instruments


p1000rack = containers.load('tiprack-1000ul', 'A1')
p200rack = containers.load('tiprack-200ul', 'A2')
trough = containers.load('trough-12row', 'C1')
tube = containers.load('tube-rack-2ml', 'D1')
plate = containers.load('96-PCR-flat', 'D2')
trash = containers.load('trash-box', 'B2')

p200_multi = instruments.Pipette(
    axis="a",
    max_volume=200,
    trash_container=trash,
    tip_racks=[p200rack],
    channels=8
)
p1000 = instruments.Pipette(
    axis="b",
    max_volume=1000,
    trash_container=trash,
    tip_racks=[p1000rack]
)


def run_custom_protocol(buffer_volume: float=300,
                        sample_volume: float=600,
                        diluent_volume: float=200,
                        a_to_d_dilution_volume: float=300,
                        h_to_e_dilution_volume: float=300):
    # distribute buffer to all wells, except columns A and E
    destination_wells = [w for c in plate.cols('B', to='H') for w in c]
    p1000.distribute(buffer_volume, trough.well('A1'), destination_wells)

    # distribute samples in duplicate to columns A and E, 1 tube to 2 wells
    p1000.distribute(
        sample_volume,
        tube.wells('A1', length=12),
        plate.cols('A') + plate.cols('E'))

    # dilute down all rows
    for this_row in plate.rows:
        p1000.distribute(
            a_to_d_dilution_volume,
            this_row.wells('A', length=3),
            this_row.wells('B', length=3),
            mix_after=(3, a_to_d_dilution_volume))
        p1000.distribute(
            h_to_e_dilution_volume,
            this_row.wells('E', length=3),
            this_row.wells('F', length=3),
            mix_after=(3, h_to_e_dilution_volume))

    # dispense diluent to every even row
    if diluent_volume > 0:
        p200_multi.distribute(
            diluent_volume,
            trough.well('A1'),
            plate.rows('2', to='12', step=2))
