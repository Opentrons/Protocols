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
    'protocolName': 'leChRO-seq Day 1 Part 3: Decapping, 5’ Phosphorylation, \
        and 1st Bead Binding and Enrichment',
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


def wash_with_buffer_twice(buffer_name):
    m300.pick_up_tip()
    reuse_tip = m300.current_tip()
    for wash_index, buffer in enumerate(buffer_name):
        if wash_index == 0:
            m300.distribute(
                100,
                buffer,
                [col[0].top() for col in elution_plate.cols()],
                blow_out=buffer,
                new_tip='never')
            for col in elution_plate.cols():
                if not m300.tip_attached:
                    m300.pick_up_tip()
                m300.mix(5, 50, col)
                m300.return_tip()
            kwarg = {'trash': False}
        else:
            m300.start_at_tip(reuse_tip)
            for col in elution_plate.cols():
                m300.transfer(100, buffer, col, mix_after=(2, 50), trash=False)
            kwarg = {'trash': True}
        # turn on Magnetic Module
        mag_module.engage(height=14.94)
        m300.delay(minutes=5)
        # remove supernatant
        m300.start_at_tip(reuse_tip)
        for col in elution_plate.cols():
            m300.transfer(300, col, liquid_trash.top(), **kwarg)


# labware setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load(deep_well_1ml_name, '1', share=True)
buffer_block = labware.load(deep_well_2ml_name, '2')
temp_module_1 = modules.load('tempdeck', '4')
temp_plate_1 = labware.load(v_bottom_plate_name, '4', share=True)
reagent_plate = labware.load(deep_well_1ml_name, '5')
temp_module_2 = modules.load('tempdeck', '7')
liquid_trash = labware.load(trough_1row_name, '7', share=True).wells('A1')
tipracks_300 = [labware.load(tiprack_300_name, slot)
                for slot in ['10', '11', '8', '9', '6', '3']]

# instruments setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_300)

# reagent setup
depc_water = reagent_plate.cols('1')
rpph_MM = reagent_plate.cols('2')
pnk_MM = reagent_plate.cols('3')
rna_adapter = reagent_plate.cols('4')
ligation_MM = reagent_plate.cols('5')
streptavidin_beads = reagent_plate.cols('6')
high_salt_buffer = buffer_block.cols('1', length=2)
binding_buffer = buffer_block.cols('3', length=2)
low_salt_buffer = buffer_block.cols('5', length=2)

# disenage magnetic module if it is engaged
if mag_module._engaged:
    mag_module.disengage()

temp_module1.set_temperature(65)
temp_module2.deactivate()
temp_module1.wait_for_temp()
if not robot.is_simulating:
    time.sleep(20)
temp_module_1.set_temperature(12)
temp_module_1.wait_for_temp()

elution_plate = temp_plate_1

# transfer RppH MM to elution plate
m300.pick_up_tip()
m300.distribute(
    30,
    rpph_MM,
    [col[0].top() for col in elution_plate.cols()],
    blow_out=rpph_MM,
    new_tip='never')
for col in elution_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.mix(2, 30, col)
    m300.drop_tip()

temp_module1.set_temperature(37)
m300.delay(minutes=60)

# transfer PNK MM to elution plate
m300.pick_up_tip()
m300.distribute(
    30,
    pnk_MM,
    [col[0].top() for col in elution_plate.cols()],
    blow_out=pnk_MM,
    new_tip='never')
for col in elution_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.mix(2, 30, col)
    m300.drop_tip()

robot.pause("Remove the plate on the Temperature Module 1 and place in a \
Thermomixer C to incubate at 37°C for 1 hour. Replenish all Tip Boxes. \
Place a clean V-bottom plate on the Temperature Module 2. Place the plate \
on the Magnetic Module before resuming.")

m300.reset()

elution_plate = mag_plate
elution_plate_2 = temp_plate_1

# transfer Streptavidin beads
m300.pick_up_tip()
reuse_tip = m300.current_tip()
m300.mix(3, 300, streptavidin_beads)
m300.distribute(
    50,
    streptavidin_beads,
    [col[0].top() for col in elution_plate.cols()],
    blow_out=streptavidin_beads,
    new_tip='never')
m300.return_tip()

robot.pause("Remove the plate on the Magnetic Module and place in on a \
Thermomixer C at 25°C for 20 minutes at 600 RPM. Replace the plate back \
on the Magnetic Module before resuming.")

robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# remove supernatant
m300.start_at_tip(reuse_tip)
for col in elution_plate.cols():
    m300.transfer(600, col, liquid_trash.top())

# wash plate with High Salt Buffer twice
wash_with_buffer_twice(high_salt_buffer)

# wash plate with Binding Buffer twice
wash_with_buffer_twice(binding_buffer)

# wash plate with Low Salt Buffer twice
wash_with_buffer_twice(low_salt_buffer)

# wash plate with DEPC Water
m300.pick_up_tip()
reuse_tip = m300.current_tip()
m300.distribute(
    100,
    depc_water,
    [col[0].top() for col in elution_plate.cols()],
    disposal_vol=0,
    new_tip='never')
for col in elution_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.mix(5, 50, col)
    m300.return_tip()
# turn on Magnetic Module
mag_module.engage(height=14.94)
m300.delay(minutes=5)
m300.start_at_tip(reuse_tip)
# remove supernatant
for col in elution_plate.cols():
    m300.transfer(300, col, liquid_trash.top(), trash=False)
# turn off Magnetic Module
mag_module.disengage()

# transfer and mix 5' DNA Adapter
m300.start_at_tip(reuse_tip)
for source, dest in zip(elution_plate.cols(), elution_plate_2.cols()):
    m300.pick_up_tip()
    m300.transfer(10, rna_adapter, source, mix_after=(5, 10), new_tip='never')
    m300.transfer(12, source, dest, new_tip='never')
    m300.drop_tip()

temp_module1.set_temperature(65)
temp_module1.wait_for_temp()
if not robot.is_simulating:
    time.sleep(20)
temp_module1.set_temperature(12)
temp_module1.wait_for_temp()

# distribute Ligation MMM
m300.pick_up_tip()
m300.distribute(
    10,
    ligation_MM,
    [col[0].top() for col in elution_plate_2.cols()],
    blow_out=ligation_MM,
    new_tip='never')
for col in elution_plate_2.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.mix(2, 10)
    m300.drop_tip()
