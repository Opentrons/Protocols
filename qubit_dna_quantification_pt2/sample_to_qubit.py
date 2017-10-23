from opentrons import containers, instruments

# TODO: adjustable speed

standard = False  # assign True if robot is needed to make standards

# row of first tip (first row is row 0, second row is row 1, etc.)
first_tip_row = 0

stloc = 'A1'  # row where standards are located

# due to bug that default offset is not (0, 0, 0) when run on the robot
offset_d = (3, 3, -.4)

gap = 2  # volume of air gap in ul, to minimize errors

# make sure tip container has 4 tips per row,
# alternating a space in between with the first column (A) empty
# if
# note that trash should be placed in slot D3

# allows file in speed_dir to control speed of the robot


# containers
p10rack = containers.load(
    'tiprack-10ul',  # container name in opentrons system
    'E1',  # slot of container
    'tiprack',  # name to remember calibrations
)

samples = containers.load(
    '96-PCR-tall',
    'D1',
    'sample_tubes',
)

tubes = containers.load(
    '96-deep-well',
    'D2',
    'd2qubit_tubes_spaced'
)

tubes_overflow = containers.load(
    '96-deep-well',
    'E2',
    'e2qubit_tubes_spaced'
)

standards = containers.load(
    '96-deep-well',
    'E3',
    'e3qubit_tubes',
)

trash = containers.load(
    'point',
    'D3',
    'trash',
)

# pipette
p10 = instruments.Pipette(
    axis='a',
    max_volume=10,
    min_volume=0.5,
    tip_racks=p10rack,
    trash_container=trash,
    channels=8,
    name='p10',
)


def tip_position(number, first=first_tip_row):
    """
    Converts current sample number to string of the
    corresponding row if there were 4 samples per row.
    """
    row = number // 4 + 1 + first
    return 'A' + str(row)


def sample_position(number):
    """
    Converts current sample number to a string of the corresponding row
    if there were 8 samples per row, plus a skip row in between samples.
    """
    row = (number // 8) * 2 + 1
    return 'A' + str(row)


def tube_position(number):
    """
    Converts current sample number to a string of the corresponding row
    if there were 4 samples per row, plus a skip row in between samples.
    Restarts when sample number is greater than 24.
    """
    row = 2 * (number // 4) + 1
    if row <= 12:
        return 'A' + str(row)
    else:
        return 'A' + str(row-12)


def offset_d(number, default=offset_d):
    """
    Converts current sample number to a tuple that alternates
    between an offset of 1 sample for the first half of the row,
    and the default offset for the second half of the rows.
    """
    remainder = number % 8
    if remainder <= 4:
        return (default[0] - 9, default[1], default[2])
    else:
        return default


def tube_container(number, original=tubes, overflow=tubes_overflow):
    """
    Given current sample number, will return the correct container for tubes.
    """
    if number <= 24:
        return original
    else:
        return overflow


def run_custom_protocol(number_of_samples: int=4, standard_volume: float=10,
                 first_sample_number: int=1, aspirate_volume: float=1):
    # loop through as many times as there are samples
    for i in range(first_sample_number, number_of_samples + 1, 4):
        # pick up tip, aspirate sample, dispense in qubit tube, drop tip
        p10.pick_up_tip(p10rack[tip_position(i)]) \
           .air_gap(gap) \
           .move_to((samples[sample_position(i)], offset_d(i))) \
           .aspirate(aspirate_volume) \
           .dispense(
               aspirate_volume+gap,
               (tube_container(i)[tube_position(i)].bottom(5))) \
           .drop_tip()

    if standard:  # if robot is needed to make standards
        while i % 4 != 0:
            i += 1  # starts pipette on a new row

        # pick up tip, aspirate standard solution,
        # dispense in qubit tube, drop tip
        p10.pick_up_tip(p10rack[tip_position(number_of_samples+1)]) \
           .aspirate(standard_volume, standards[stloc]) \
           .dispense(
               standard_volume,
               (tube_container(i)[tube_position(i)].bottom(5))) \
           .drop_tip()
