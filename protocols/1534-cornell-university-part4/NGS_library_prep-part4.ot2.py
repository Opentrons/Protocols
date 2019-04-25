from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import tempdeck

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
    'protocolName': 'leChRO-seq Day 2: 2nd Bead Wash & Enrichment',
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
buffer_plate = labware.load(deep_well_2ml_name, '5')
temp_module_2 = modules.load('tempdeck', '7')
liquid_trash = labware.load(trough_1row_name, '9').wells('A1')
tipracks_300 = [labware.load(tiprack_300_name, slot)
                for slot in ['10']]

# instruments setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_300)

# reagent setup
high_salt_buffer = buffer_plate.cols('1')
binding_buffer = buffer_plate.cols('2')
low_salt_buffer = buffer_plate.cols('3')
depc_water = buffer_plate.cols('4')

temp_module1.deactivate()
temp_module2.deactivate()

sample_col = mag_plate.cols('1')

# turn on Magnetic Module
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# remove supernatant
m300.transfer(600, sample_col[0].top(), liquid_trash.top())

# turn off Magnetic Module
mag_module.disengage()

# wash column with High Salt Buffer twice
for _ in range(2):
    m300.pick_up_tip()
    m300.transfer(500, high_salt_buffer, sample_col, new_tip='never')
    m300.mix(30, 300, sample_col)
    m300.retract()
    # turn on Magnetic Module
    mag_module.engage(height=14.94)
    m300.delay(minutes=5)
    # remove supernatant
    m300.transfer(600, sample_col, liquid_trash.top(), new_tip='never')
    m300.drop_tip()
    # turn off Magnetic Module
    mag_module.disengage()

# wash column with Binding buffer twice
for _ in range(2):
    m300.pick_up_tip()
    m300.transfer(500, binding_buffer, sample_col, new_tip='never')
    m300.mix(30, 300, sample_col)
    m300.retract()
    # turn on Magnetic Module
    mag_module.engage(height=14.94)
    m300.delay(minutes=5)
    # remove supernatant
    m300.transfer(600, sample_col, liquid_trash.top(), new_tip='never')
    m300.drop_tip()
    # turn off Magnetic Module
    mag_module.disengage()

# wash column with Low Salt Buffer
m300.pick_up_tip()
m300.transfer(500, low_salt_buffer, sample_col, new_tip='never')
m300.mix(30, 300, sample_col)
m300.retract()
# turn on Magnetic Module
mag_module.engage(height=14.94)
m300.delay(minutes=5)
# remove supernatant
m300.transfer(600, sample_col, liquid_trash.top(), new_tip='never')
m300.drop_tip()
# turn off Magnetic Module
mag_module.disengage()

# wash column with DEPC water
m300.pick_up_tip()
m300.transfer(500, depc_water, sample_col, new_tip='never')
m300.mix(30, 300, sample_col)
m300.retract()
# turn on Magnetic Module
mag_module.engage(height=14.94)
m300.delay(minutes=5)
# remove supernatant
m300.transfer(600, sample_col, liquid_trash.top(), new_tip='never')
m300.drop_tip()
# turn off Magnetic Module
mag_module.disengage()
