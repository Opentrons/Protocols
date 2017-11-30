from opentrons import containers, instruments, robot
from otcustomizers import StringSelection

robot.reset()

containers.create(
    'septum-plate',  # name of you container
    grid=(7, 8),   # specify amount of (columns, rows)
    spacing=(18, 10),  # distances (mm) between each (column, row)
    diameter=2,       # diameter (mm) of each well on the plate
    depth=10)

"""
Column A
"""
tiprack = containers.load('tiprack-200ul', 'A1')
tuberack = containers.load('tube-rack-2ml', 'A2')

"""
Column B
"""

"""
Column C
"""

trash = containers.load('trash-box', 'C2')
trough = containers.load('trough-12row', 'C1')

"""
Column D
"""
septum = containers.load('septum-plate', 'D1')
"""
Column E
"""

"""
Instruments
"""
p50 = instruments.Pipette(
    axis='a',
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tiprack],
    trash_container=trash)

p100 = instruments.Pipette(
    axis='b',
    name='p100single',
    max_volume=100,
    min_volume=10,
    channels=1,
    tip_racks=[tiprack],
    trash_container=trash)


def run_custom_protocol(
        plate_type: StringSelection('96-Plate', '384-Plate')='96-Plate'):

    """
    Variable initialization/Reagent setup
    """
    multichannel = False
    if plate_type == '96-Plate':
        multichannel = True

    if multichannel:
        pipette = p50
        source = trough
    else:
        pipette = p100
        source = tuberack

    hexane = source.wells('A1')
    work_soln = source.wells('A2')

    """
    Protocol
    """
    # Step 2
    pipette.pick_up_tip()
    pipette.transfer(30, hexane, trash, new_tip='never')

    pipette.aspirate(30, work_soln)
    # Step 4-9
    if multichannel:
        for row in septum.rows():
            # Step 3
            pipette.dispense(20, row)
            pipette.aspirate(20, work_soln)
    else:
        for well in septum.wells():
            pipette.dispense(20, well)
            pipette.aspirate(20, work_soln)

    # Step 10
    pipette.dispense(work_soln)
    pipette.drop_tip()
