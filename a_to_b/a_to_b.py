from opentrons import instruments, containers

Container = 'container'  # TODO
Axis = 'axis'  # TODO


def get_alternating_wells(container, number_of_wells):
    # TODO: use number_of_wells!
    alternating_wells = []
    for row in container.rows():
        alternating_wells.append(row.wells('A', length=8, step=2))
        alternating_wells.append(row.wells('B', length=8, step=2))
    return alternating_wells


def run_protocol(
    source_container_type: Container='96-flat',
    destination_container_type: Container='96-flat',
    pipette_size: int=10,  # TODO: 1 / 10 / 20 / 50 / 100 / 200
    pipette_axis: Axis='a',
    pipette_channels: int=1,  # TODO: 1 or 8
    number_of_wells: int=1,
    well_volume: float=10.0
):
    source_container = containers.load(source_container_type, 'E1')
    destination_container = containers.load(destination_container_type, 'C1')

    tiprack1 = containers.load('tiprack-200ul', 'A1', 'p200rack')
    tiprack2 = containers.load('tiprack-200ul', 'B1', 'p200rack')

    trash = containers.load('point', 'C2', 'trash')

    pipette = instruments.Pipette(
        axis=pipette_axis,
        trash_container=trash,
        tip_racks=[tiprack1, tiprack2],
        max_volume=pipette_size,
        min_volume=pipette_size / 10,  # TODO: double-check
        # TODO: validate containers for 8-channel, not all will work!
        channels=pipette_channels,
    )

    source_wells = source_container.wells(length=number_of_wells)
    destination_wells = source_container.wells(length=number_of_wells)

    if pipette_channels == 8:
        source_wells = get_alternating_wells(source_container, number_of_wells)
        destination_wells = get_alternating_wells(
            destination_container, number_of_wells)

    pipette.distribute(well_volume, source_wells, destination_wells)
