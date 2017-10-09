from opentrons import containers, instruments

standard = False  # assign True if robot is needed to make standards
# place standard tubes on new row if needed

first_tip = 'A1'  # well location of the first tip
# note that trash should be placed in A3

# containers
p1000rack = containers.load(
    'tiprack-1000ul-chem',  # container name in opentrons system
    'A1',  # slot of container
    'tiprack',  # name to remember calibrations
)

tubes = containers.load(
    '96-deep-well',
    'A2',
    'a2qubit_tubes',
)

tubes_overflow = containers.load(
    '96-deep-well',
    'B2',
    'b2qubit_tubes',
)

trash = containers.load(
    'point',
    'A3',
    'a3trash',
)

containers.create(
    '15ml-short-tube',
    grid=(1, 1),
    spacing=(20, 20),
    diameter=18,
    depth=105,
)

solution = containers.load(
    '15ml-short-tube',
    'B1',
    '15mltube',
)

standards = containers.load(
    '96-deep-well',
    'B1',
    'b1p5tube',
)

# pipette
p1000 = instruments.Pipette(
    name="p1000",
    axis="b",
    min_volume=100,
    max_volume=1000,
    tip_racks=p1000rack,
    trash_container=trash,
    channels=1,
)


def make_position(number):
    """
    Converts current sample number to corresponding well number on
    96-well plate, if there were 4 samples per row plus a skip row
    in between samples. Restarts when sample number is greater than 24.
    """
    if number > 24:
        number = number - 24
    row = int(number // 4.1)
    return (2 * number - 1) + (row * 8)


def tube_container(number, original=tubes, overflow=tubes_overflow):
    """
    Given current sample number, will return the correct container for tubes.
    """
    if number <= 24:
        return original
    else:
        return overflow
    # THIS WAS NOT COMMENTED OUT ORIGINALLY, BUT IS UNREACHABLE CODE:
    # return correct_container(
    #     number, original=tubes, overflow=tubes_overflow, capacity=24)


def run_protocol(sample_number: int=4, qubit_solution_volume: float=199,
                 standard_volume: float=190, first_sample_number: int=1):
    # p1000.start_at_tip(p1000rack[first_tip])  # start at first tip assigned
    p1000.pick_up_tip(p1000rack[first_tip])  # pick up tip, only 1 tip needed

    # loop through as many times as there are samples
    for i in range(first_sample_number, sample_number + 1):
        if p1000.current_volume < qubit_solution_volume:
            # if volume is low, aspirate qubit solution
            p1000.aspirate(solution['A1'])

        # dispense in qubit tube
        p1000.dispense(
            qubit_solution_volume,
            (tube_container(i)[make_position(i)].bottom(15)))

    if standard:  # if robot is needed to make standards
        while sample_number % 4 != 0:
            sample_number += 1  # starts pipette in a new row

        # loop through for two standards
        for i in range(sample_number+1, sample_number+3):
            if p1000.current_volume < standard_volume:
                # if volume is low, aspirate qubit solution
                p1000.aspirate(solution['A1'])
            # aspirate qubit solution, dispense in qubit tube
            p1000.dispense(
                standard_volume,
                (tube_container(i)[make_position(i)].bottom(15)))
    p1000.dispense(solution['A1']) \
         .drop_tip()  # return leftover solution to tube and drop tip
