from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Arcis Blood Extraction and PCR Setup (Multi)',
    'author': 'Chaz <chaz@opentrons.com',
    'source': 'Custom Protocol Request'
}

# create labware
tip1 = labware.load('opentrons_96_tiprack_300ul', '5', 'Tips')
tip2 = labware.load('opentrons_96_tiprack_300ul', '6', 'Tips')
tips = tip1.rows('A') + tip2.rows('A')

trough = labware.load('usascientific_12_reservoir_22ml', '4', 'Reservoir')
cplate = labware.load('corning_96_wellplate_360ul_flat', '1', 'Corning Plate')
bp_name = 'bioplastics_96_wellplate_100ul'
if bp_name not in labware.list():
    labware.create(
        bp_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.07,
        depth=14,
        volume=100
    )
biop1 = labware.load(bp_name, '2', 'Bioplastics Plate 1')
biop2 = labware.load(bp_name, '3', 'Bioplastics Plate 2')

reagent1 = trough.wells(0)
reagent2 = trough.wells(1)
mm = trough.well(2)
sample = trough.wells(3)


def run_custom_protocol(
    p50_multi_mount: StringSelection('left', 'right') = 'left',
    p300_multi_mount: StringSelection('right', 'left') = 'right',
    number_of_samples: int = 48
        ):

    # create specific sample labware and raise exceptions
    pip50 = instruments.P50_Multi(mount=p50_multi_mount)
    pip300 = instruments.P300_Multi(mount=p300_multi_mount)

    if number_of_samples > 88 or number_of_samples < 1:
        raise Exception('Number of Samples should be between 1 and 84.')

    num_cols = math.ceil(number_of_samples/8)

    bp1 = biop1.rows('A')[:num_cols]
    bp2 = biop2.rows('A')[:num_cols]
    cp = cplate.rows('A')[:num_cols]

    tipcount = 0

    def pick_up(pip):
        nonlocal tipcount
        if tipcount == 24:
            pip50.home()
            robot.pause('Out of tips. Please replace tips in slots 5 & 6.')
            tipcount = 0

        if pip == pip50:
            pip50.pick_up_tip(tips[tipcount])
        else:
            pip300.pick_up_tip(tips[tipcount])

        tipcount += 1

    # transfer 150 ul reagent 1

    pick_up(pip300)

    for row in cp:
        pip300.transfer(150, reagent1, row, new_tip='never')

    pip300.drop_tip()

    # transfer 20 ul reagent 2

    pick_up(pip50)

    for row in bp1:
        pip50.transfer(20, reagent2, row, new_tip='never')

    pip50.drop_tip()

    # transfer 30ul of sample to reagent 1

    for row in cp:
        pick_up(pip300)
        pip300.transfer(30, sample, row, new_tip='never')
        pip300.drop_tip()

    # transfer 5ul of sample to reagnet 2

    for src, dest in zip(cp, bp1):
        pick_up(pip50)
        pip50.transfer(5, src, dest, new_tip='never')
        pip50.drop_tip()

    # transfer 20uL mastermix

    pick_up(pip50)

    for row in bp2:
        pip50.transfer(20, mm, row, new_tip='never')

    pip50.transfer(20, mm, biop2.wells('A12'), new_tip='never')

    pip50.drop_tip()

    # tranfer 5uL of samples+reagents to mastermix

    for src, dest in zip(bp1, bp2):
        pick_up(pip50)
        pip50.transfer(5, src, dest, new_tip='never')
        pip50.drop_tip()

    robot.comment('Congratulations. Protocol is now complete.')
