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
    'protocolName': 'leChRO-seq Day 1 Part 2: Run-on Reaction and Cleanup of \
        Biotin-11 Run-on Reaction Part 2',
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
ethanol = labware.load(trough_1row_name, '2').wells('A1')
prewash_block = labware.load(deep_well_2ml_name, '3')
temp_module_1 = modules.load('tempdeck', '4')
romm2_block = labware.load(deep_well_1ml_name, '4', share=True)
reagent_plate = labware.load(deep_well_2ml_name, '5')
temp_module_2 = modules.load('tempdeck', '7')
elution_plate = labware.load(v_bottom_plate_name, '7', share=True)
tipracks_300 = [labware.load(tiprack_300_name, slot)
                for slot in ['10', '11', '8', '9', '6']]

# instruments setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_300)

# reagent setup
trizol_LS = reagent_plate.cols('1')
direct_zol = reagent_plate.cols('2')
mag_beads = reagent_plate.cols('3')
dnase_I_MM = reagent_plate.cols('4')
water = reagent_plate.cols('5')
prewash = prewash_block.cols('1')

# disenage magnetic module if it is engaged
if mag_module._engaged:
    mag_module.disengage()

# prewash samples twice
for wash_index in range(2):
    # transfer Direct-zol MagBead Pre-Wash to sample
    m300.pick_up_tip()
    for source, dests in zip(
            prewash_block.cols(wash_index * 3, length=3),
            [mag_plate.cols(index * 4, length=4) for index in range(3)]):
        for dest in dests:
            m300.transfer(500, source, dest[0].top(), new_tip='never')
    m300.home()
    robot.pause("Place the plate on the Mini-Tube Rotator for 10 minutes to \
    resuspend the beads. Place the plate back on the Magnetic Module.")
    # turn on Magnetic Module
    robot._driver.run_flag.wait()
    mag_module.engage(height=14.94)
    m300.delay(minutes=5)
    # remove supernatant
    for sources, dest in zip(
            [mag_plate.cols(index * 4, length=4) for index in range(3)],
            prewash_block.cols(11 - (wash_index * 3), length=-3)):
        for source in sources:
            if not m300.tip_attached:
                m300.pick_up_tip()
            m300.transfer(600, source, dest[0].top(), new_tip='never')
            m300.drop_tip()
    # turn off Magnetic Module
    mag_module.disengage()

# wash with Ethanol twice
for wash in range(2):
    m300.pick_up_tip()
    reuse_tip = m300.current_tip()
    for well in mag_plate.rows('A'):
        m300.transfer(750, ethanol, well.top(), new_tip='never')
    # mix ethanol + samples
    for well in mag_plate.rows('A'):
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.mix(3, 50, well)
        m300.return_tip()
    # turn on Magnetic Module
    mag_module.engage(height=14.94)
    m300.delay(minutes=5)
    # remove supernatant
    m300.start_at_tip(reuse_tip)
    for well in mag_plate.rows('A'):
        m300.transfer(800, well, m300.trash_container.top())
    # turn off Magnetic Module
    mag_module.disengage()

robot.pause("Remove the plate on the Magnetic Module and place in a \
Thermomixer at 55°C for 15 minutes at 0 RPM. Place the plate back on the \
Magnetic Module before resuming.")

# transfer DNase/RNase-free water
m300.pick_up_tip()
reuse_tip = m300.current_tip()
m300.distribute(
    20,
    water,
    [col[0].top() for col in mag_plate.cols()],
    disposal_vol=0,
    new_tip='never')
for col in mag_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.mix(2, 20)
    m300.return_tip()
mag_module.engage(height=14.94)
m300.delay(minutes=5)
m300.start_at_tip(reuse_tip)
# transfer sample to elution plate
for source, dest in zip(mag_plate.cols(), elution_plate.cols()):
    m300.transfer(20, source, dest)
