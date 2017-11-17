from opentrons import containers, instruments
from otcustomizers import StringSelection


def run_custom_protocol(
  a: int=12,
  b='woo',
  plate_type: StringSelection('96-flat', '96-PCR-flat', '96-PCR-tall')='96-flat'):  # noqa: E501

    p200rack = containers.load(
        'tiprack-200ul',  # container type
        'A1'             # slot
    )

    trough = containers.load(
        'trough-12row',
        'A3',
        'trough'
    )

    trash = containers.load(
        'point',
        'B2',
        'trash'
    )

    p200 = instruments.Pipette(
        trash_container=trash,
        tip_racks=[p200rack],
        min_volume=20,  # actual minimum volume of the pipette
        axis="a",
        channels=8
    )

    p200.transfer(100, trough.wells(0), trough.wells(1))
