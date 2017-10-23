from opentrons import containers, instruments


p200rack = containers.load('tiprack-200ul', 'A2')
trash = containers.load('trash-box', 'B3')

source_plate = containers.load('96-PCR-flat', 'C2')

dest_plates = [
    containers.load('96-PCR-flat', 'D1'),
    containers.load('96-PCR-flat', 'D2'),
    containers.load('96-PCR-flat', 'E1'),
    containers.load('96-PCR-flat', 'E2'),
    containers.load('96-PCR-flat', 'D3'),
    containers.load('96-PCR-flat', 'E3')
]

p200_multi = instruments.Pipette(
    axis="a",
    name='p200_multi',
    max_volume=200,
    min_volume=10,
    channels=8,
    trash_container=trash,
    tip_racks=[p200rack]
)


def run_custom_protocol(odd_volume: float=45, even_volume: float=90,
                 number_of_destination_plates: int=6):
    if number_of_destination_plates > len(dest_plates):
        raise RuntimeError((
            'Number of destination plates is too high. {} was specified, ' +
            'but the max is {}').format(
                number_of_destination_plates, len(dest_plates)))

    # map odd_volume to all odd rows of all 6 destination plates
    for i in range(0, 12, 2):
        target_rows = [plate.rows(i) for plate in dest_plates]
        p200_multi.distribute(odd_volume, source_plate.rows(i), target_rows)

    # map even_volume to all even rows of all 6 destination plates
    for i in range(1, 12, 2):
        target_rows = [d.rows(i) for d in dest_plates]
        p200_multi.distribute(even_volume, source_plate.rows(i), target_rows)
