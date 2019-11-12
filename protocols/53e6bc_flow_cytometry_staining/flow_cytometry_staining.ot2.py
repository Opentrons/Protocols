from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
from opentrons.legacy_api.modules import tempdeck
import math

metadata = {
    'protocolName': 'Flow Cytometry Staining',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

"""Controlling two of the same module in the protocol:
1. SSH into robot
2. run $ls /dev/tty*
   you are looking for two values with the format /dev/ttyACM*
   you will use those values in lines 82 and 83.
If you need to know which tempdeck is hooked up to which port:
1. unplug one of the modules
2. run $ls /dev/tty* : the results correlates to the module that is plugged in
3. plug the other module in and run ls /dev/tty* again, you will be able to
   know the value of the second module
"""

# create custom labware
rack_5ml_name = 'vwr_15_tuberack_selfstanding_5ml_conical'
if rack_5ml_name not in labware.list():
    labware.create(
        rack_5ml_name,
        grid=(5, 3),
        spacing=(25, 25),
        diameter=14,
        depth=56,
        volume=5000
    )

plate_name = 'vwr_96_wellplate_2.2ml_deep'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=39,
        volume=2200
    )

# load modules and labware
rack_5ml = labware.load(rack_5ml_name, '2', '3x5 5ml tuberack')
tiprack300 = labware.load('opentrons_96_tiprack_300ul', '3')

# reagent setup
mm = rack_5ml.wells()[0]


def run_custom_protocol(
    p300_single_mount: StringSelection('right', 'left') = 'right',
    p300_multi_mount: StringSelection('left', 'right') = 'left',
    number_of_samples: int = 24,
    mastermix_distribution_plate_column: int = 1
):
    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Number of samples must be from 1-96.')
    if p300_single_mount == p300_multi_mount:
        raise Exception('Pipette mounts cannot match.')
    if (
        mastermix_distribution_plate_column < 1 or
        mastermix_distribution_plate_column > 12
       ):
        raise Exception(
            'Choose mastermix distribution column between 1 and 12.')

    # single-channel pipette
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=[tiprack300])

    if number_of_samples > 8:
        # defining two Temperature Modules
        tempdeck1 = tempdeck.TempDeck()
        tempdeck2 = tempdeck.TempDeck()

        tempdeck1._port = '/dev/ttyACM1'
        tempdeck2._port = '/dev/ttyACM2'

        if not robot.is_simulating():
            tempdeck1.connect()
            tempdeck2.connect()

        tempdeck1.set_temperature(4)
        tempdeck2.set_temperature(4)
        robot.comment('Temperature modules reaching temp...')
        tempdeck2.wait_for_temp()
        tempdeck1.wait_for_temp()

        [modules.load('tempdeck', slot) for slot in ['1', '4']]
        sample_plate = labware.load(
            plate_name, '1', 'sample plate', share=True)
        mm_dist_plate = labware.load(
            plate_name, '4', 'plate for mastermix distributions', share=True)

        # multi-channel pipette
        m300 = instruments.P300_Multi(
            mount=p300_multi_mount, tip_racks=[tiprack300])
        # distribute mastermix to plate for distribution
        mm_col = mm_dist_plate.columns()[mastermix_distribution_plate_column-1]
        mm_wells = [mm_col[well % 8] for well in range(number_of_samples)]
        num_cols = math.ceil(number_of_samples/8)
        dests = sample_plate.rows('A')[:num_cols]
        p300.pick_up_tip(tiprack300.wells()[num_cols*8])
        p300.distribute(
            95,
            mm,
            [well.bottom(5) for well in mm_wells],
            new_tip='never',
            disposal_vol=0
        )
        for d in dests:
            m300.pick_up_tip()
            m300.transfer(90, mm_col[0], d.bottom(2), new_tip='never')
            m300.mix(3, 50, d.bottom(2))
            m300.blow_out(d.top(-5))
            m300.drop_tip()
    else:
        tempdeck1 = modules.load('tempdeck', '1')
        tempdeck1.set_temperature(4)
        tempdeck1.wait_for_temp()
        robot.comment('Temperature modules reaching temp...')
        sample_plate = labware.load(
            plate_name, '1', 'sample plate', share=True)
        dests = sample_plate.wells()[:number_of_samples]
        for d in dests:
            p300.pick_up_tip()
            p300.transfer(90, mm.bottom(2), d.bottom(2), new_tip='never')
            p300.mix(3, 50, d.bottom(2))
            p300.blow_out(d.top(-5))
            p300.drop_tip()
