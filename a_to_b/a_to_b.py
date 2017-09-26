from opentrons import instruments, containers
from opentrons.containers.placeable import Container
import math


def get_alternating_wells(container, number_of_wells):
    # TODO: use number_of_wells!
    alternating_wells = []
    for row in container.rows():
        alternating_wells.append(row.wells('A', length=8, step=2))
        alternating_wells.append(row.wells('B', length=8, step=2))
    return alternating_wells


def run_protocol(
    source_container_type: Container = '96-flat',
    destination_container_type: Container = '96-flat',
    pipette_model: [1, 5, 10, 20, 50, 100, 200] = 100,
    pipette_axis: ['a', 'b'] = 'a',
    pipette_channels: [1, 8] = 1,
    number_of_samples: int = 1,
    transfer_volume: float = 10.0
):
    # HACK: Doing `container_var or 'point'` so deck map parsing works
    source_container = containers.load(source_container_type or 'point', 'E1')
    destination_container = containers.load(
        destination_container_type or 'point', 'C1')

    tiprack1 = containers.load('tiprack-200ul', 'A1', 'p200rack')
    tiprack2 = containers.load('tiprack-200ul', 'B1', 'p200rack')

    trash = containers.load('trash-box', 'C2')

    pipette = instruments.Pipette(
        axis=pipette_axis,
        trash_container=trash,
        tip_racks=[tiprack1, tiprack2],
        max_volume=pipette_model,
        min_volume=math.ceil(pipette_model / 10),
        # TODO: validate containers for 8-channel, not all will work!
        channels=pipette_channels,
    )

    source_wells = source_container.wells(length=number_of_samples)
    destination_wells = source_container.wells(length=number_of_samples)

    if pipette_channels == 8:
        source_wells = get_alternating_wells(
            source_container, number_of_samples)

        destination_wells = get_alternating_wells(
            destination_container, number_of_samples)

    pipette.distribute(transfer_volume, source_wells, destination_wells)
