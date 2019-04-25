from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import tempdeck
import time

"""Controlling two of the same module in the protocol:
1. SSH into robot
2. run $ls /dev/tty*
   you are looking for two values with the format /dev/ttyACM*
   you will use those values in line 23 and 24.

If you need to know which tempdeck is hooked up to which port:
1. unplug one of the modules
2. run $ls /dev/tty* : the results correlates to the module that is plugged in
3. plug the other module in and run ls /dev/tty* again, you will be able to
   know the value of the second module
"""

# defining two Temperature Modules
temp_module1 = tempdeck.TempDeck()
temp_module2 = tempdeck.TempDeck()

temp_module1._port = '/dev/ttyACM3'
temp_module2._port = '/dev/ttyACM2'

if not robot.is_simulating():
    temp_module1.connect()
    temp_module2.connect()


metadata = {
    'protocolName': 'leChRO-seq Day 3 Part 2: Reverse Transcription',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# custom labware definitions
tiprack_300_name = 'tipone-filter-tiprack-300ul'
tiprack_10_name = 'tipone-filter-tiprack-10ul'
for name in [tiprack_10_name, tiprack_300_name]:
    if name not in labware.list():
        labware.create(
            name,
            grid=(12, 8),
            spacing=(9, 9),
            diameter=5,
            depth=60)

deep_well_1ml_name = 'plateone-96-deep-well-1ml'
if deep_well_1ml_name not in labware.list():
    labware.create(
        deep_well_1ml_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=41.3,
        volume=1000)

deep_well_2ml_name = 'plateone-96-deep-well-2ml'
if deep_well_2ml_name not in labware.list():
    labware.create(
        deep_well_2ml_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=41.3,
        volume=2000)

trough_1row_name = 'texan-reservoir-175ml'
if trough_1row_name not in labware.list():
    labware.create(
        trough_1row_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=80,
        depth=28)

v_bottom_plate_name = 'plateone-96-v-bottom'
if v_bottom_plate_name not in labware.list():
    labware.create(
        v_bottom_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=11.3)


# labware setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load(deep_well_1ml_name, '1', share=True)
temp_module_1 = modules.load('tempdeck', '4')
temp_plate_1 = labware.load(v_bottom_plate_name, '4', share=True)
reagent_plate = labware.load(v_bottom_plate_name, '5')
temp_module_2 = modules.load('tempdeck', '7')
liquid_trash = labware.load(trough_1row_name, '9').wells('A1')
tiprack_10 = labware.load(tiprack_10_name, '11')

# instruments setup
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_10])

# reagent setup
rt_MM_1 = reagent_plate.cols('1')
rt_MM_2 = reagent_plate.cols('2')


# turn off Magnetic Module if it is engaged
if mag_module._engaged:
    mag_module.disengage()

# set Temperature Modules to RT
temp_module1.deactivate()
temp_module2.deactivate()

sample_col = temp_plate_1.cols('1')

# transfer RT MM 1 to samples
m10.transfer(3, rt_MM_1, sample_col, mix_after=(5, 10))

temp_module1.set_temperature(65)
temp_module1.wait_for_temp()

if not robot.is_simulating:
    time.sleep(300)

temp_module1.set_temperature(12)
temp_module1.wait_for_temp()

if not robot.is_simulating:
    time.sleep(120)

# transfer RT MM 2 to samples
m10.transfer(7, rt_MM_2, sample_col, mix_after=(5, 10))
