from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import tempdeck

"""Controlling two of the same module in the protocol:
1. SSH into robot
2. run $ls /dev/ttyACM*
   you are looking for two values with the format /dev/ttyACM*
   you will use those values in line 23 and 24.
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
    'protocolName': 'leChRO-seq Day 1 Part 1: Run-on Reaction and Cleanup of \
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


# labware setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load(deep_well_1ml_name, '1', share=True)
ethanol = labware.load(trough_1row_name, '2').wells('A1')
temp_module_1 = modules.load('tempdeck', '4')
romm2_block = labware.load(deep_well_1ml_name, '4', share=True)
reagent_plate = labware.load(deep_well_2ml_name, '5')
tiprack_10 = labware.load(tiprack_10_name, '6')
temp_module_2 = modules.load('tempdeck', '7')
samples = labware.load(deep_well_1ml_name, '7', share=True)
tipracks_300 = [labware.load(tiprack_300_name, slot)
                for slot in ['10', '11', '8', '3']]
halogenated_trash = labware.load(trough_1row_name, '9').wells('A1')

# instruments setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_300)
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_10])

# reagent setup
trizol_LS = reagent_plate.cols('1')
direct_zol_binding_buffer = reagent_plate.cols('2')
mag_beads = reagent_plate.cols('3')
dnase_I_MM = reagent_plate.cols('4')

# disengage magnet if it is engaged
if mag_module._engaged:
    mag_module.disengage()

# warm up solutions
temp_module1.set_temperature(37)
temp_module2.set_temperature(37)
temp_module1.wait_for_temp()
temp_module2.wait_for_temp()
m300.delay(minutes=5)

# transfer 2xROMM to samples
for source, dest in zip(romm2_block.cols(), samples.cols()):
    m300.transfer(25, source, dest)

temp_module1.deactivate()
temp_module2.deactivate()

robot.pause("Remove sample plate and place on the Thermomixer C at 37°C \
for 5 minutes at 500 RPM. Return the plate on the Magnetic Module in slot \
1 before resuming the protocol.")

# distribute TRIzol LS to samples
m300.pick_up_tip()
m300.distribute(
    150,
    trizol_LS,
    [well.top() for well in samples.rows('A')],
    disposal_vol=0,
    new_tip='never')
# mix samples
for col in mag_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.mix(3, 50, col)
    m300.blow_out(col[0].top())
    m300.drop_tip()

# transfer Direct-zol Binding Buffer to samples
m300.pick_up_tip()
m300.distribute(
    150,
    direct_zol_binding_buffer,
    [well.top() for well in samples.rows('A')],
    disposal_vol=0,
    new_tip='never')
# mix samples
for col in mag_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.mix(3, 50, col)
    m300.blow_out(col[0].top())
    m300.drop_tip()


# transfer MagBinding Beads to samples
m10.pick_up_tip()
m10.mix(3, 10, mag_beads)
m10.transfer(
    7.2,
    mag_beads,
    [well.top() for well in samples.rows('A')],
    blow_out=True,
    new_tip='never')
m10.drop_tip()

robot.pause("Place the sample plate on the Mini-Tube Rotator for 10 \
minutes to mix. Replenish all of the 300 uL tip racks. Place the sample \
plate back on the Magnetic Moulde before resuming.")
m300.reset()

robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m10.delay(minutes=5)


# remove supernatant
for col in mag_plate.cols():
    m300.transfer(600, col, halogenated_trash.top())

mag_module.disengage()

# wash samples with Ethanol twice
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
    m10.delay(minutes=5)
    # remove supernatant
    m300.start_at_tip(reuse_tip)
    for well in mag_plate.rows('A'):
        m300.transfer(800, well, m300.trash_container.top())
    # turn off Magnetic Module
    mag_module.disengage()

# transfer DNase I MM to samples
m300.distribute(
    50,
    dnase_I_MM,
    [well.top() for well in mag_plate.rows('A')],
    disposal_vol=0)
