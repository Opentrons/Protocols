from opentrons import containers, instruments


p200rack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('trash-box', 'A2')
sample_tubes = containers.load('tube-rack-2ml', 'C2')
plate = containers.load('384-plate', 'C1')

p200 = instruments.Pipette(
    axis="b",
    max_volume=200,
    tip_racks=[p200rack],
    trash_container=trash
)


def run_custom_protocol(number_of_tubes: int=24, transfer_volume: int=40):
    if number_of_tubes > len(sample_tubes):
        print(
            'Number of samples is too high: {}. The max is {}'.format(
                number_of_tubes, len(sample_tubes)))

    # dispense from tube to plate, for all tubes
    p200.transfer(
        transfer_volume,
        sample_tubes.wells('A1', length=number_of_tubes),
        plate.wells('A1', length=number_of_tubes),
        new_tips='always'
    )
