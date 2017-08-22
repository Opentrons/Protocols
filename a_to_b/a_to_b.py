from opentrons import instruments, containers
from opentrons.containers.placeable import Container
import math
from enum import Enum


class PipetteAxis(Enum):
    A = 'a'
    B = 'b'
    __name__ = 'PipetteAxis'


class PipetteModel(Enum):
    P1 = '1'
    P5 = '5'
    P10 = '10'
    P20 = '20'
    P50 = '50'
    P100 = '100'
    P200 = '200'
    __name__ = 'PipetteModel'

    def max_volume(self):
        return int(self.value)

    def min_volume(self):
        return math.ceil(int(self.value) / 10)


class PipetteChannels(Enum):
    ONE = '1'
    EIGHT = '8'
    __name__ = 'PipetteChannels'


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
    pipette_model: PipetteModel=PipetteModel('10'),
    pipette_axis: PipetteAxis=PipetteAxis('a'),
    pipette_channels: PipetteChannels = PipetteChannels('1'),
    number_of_wells: int=1,
    well_volume: float=10.0
):
    source_container = containers.load(source_container_type, 'E1')
    destination_container = containers.load(destination_container_type, 'C1')

    tiprack1 = containers.load('tiprack-200ul', 'A1', 'p200rack')
    tiprack2 = containers.load('tiprack-200ul', 'B1', 'p200rack')

    trash = containers.load('trash-box', 'C2')

    pipette = instruments.Pipette(
        axis=pipette_axis.value,
        trash_container=trash,
        tip_racks=[tiprack1, tiprack2],
        max_volume=pipette_model.max_volume(),
        min_volume=pipette_model.min_volume(),
        # TODO: validate containers for 8-channel, not all will work!
        channels=int(pipette_channels.value),
    )

    source_wells = source_container.wells(length=number_of_wells)
    destination_wells = source_container.wells(length=number_of_wells)

    if int(pipette_channels.value) == 8:
        source_wells = get_alternating_wells(source_container, number_of_wells)
        destination_wells = get_alternating_wells(
            destination_container, number_of_wells)

    pipette.distribute(well_volume, source_wells, destination_wells)
