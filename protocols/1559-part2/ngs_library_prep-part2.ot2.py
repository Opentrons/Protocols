from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NGS Library Prep Part 2',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# custom labware creation
mag_plate_name = 'framestar-96-semi-skirted-PCR'
if mag_plate_name not in labware.list():
    labware.create(
        mag_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=20.2)

temp_plate_name = 'aluminum-block-framestar-96-semi-skited-PCR'
if temp_plate_name not in labware.list():
    labware.create(
        temp_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=20.2)

# labware setup
reagent_plate = labware.load('PCR-strip-tall', '1')
trough = labware.load('trough-12row', '2')
mag_module = modules.load('magdeck', '4')
mag_plate = labware.load(mag_plate_name, '4', share=True)
temp_module = modules.load('tempdeck', '7')
temp_plate = labware.load(temp_plate_name, '7', share=True)

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['3', '6', '9']]
tipracks_300 = [labware.load('tiprack-200ul', slot)
                for slot in ['5', '8', '10', '11']]

# instruments setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_10)
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_300)

# reagent setup
ampure_xp_beads = trough.wells('A1')
resuspension_buffer = trough.wells('A2')
pcr_mastermix = trough.wells('A3')
ethanol_1 = trough.wells('A4', length=2)
ethanol_2 = trough.wells('A6', length=2)
ethanol_3 = trough.wells('A8', length=2)

a_tailling_mix = reagent_plate.cols('1')
ligation_mix = reagent_plate.cols('2')
stop_ligation_buffer = reagent_plate.cols('3')
pcr_primer_cocktail = reagent_plate.cols('4')

# disengage Magnetic Module if it is engaged
if mag_module._engaged:
    mag_module.disengage()

# transfer Resuspension Buffer
m10.transfer(
    2.5, resuspension_buffer, [col[0].top() for col in mag_plate.cols()],
    blow_out=True)

# transfer A-Tailing Mix
for col in mag_plate.cols():
    m10.pick_up_tip()
    m10.transfer(12.5, a_tailling_mix, col[0].top(), new_tip='never')
    m10.mix(3, 10, col)
    m10.blow_out(col)
    m10.drop_tip()

robot.pause("Remove the plate from the Magnetic Module and place on a \
Thermocycler to Ligate Adapters. Put the thawed RNA Adpater Index on the \
Magnetic Module. Place the plate back on the Temperature Module before \
resuming. See Configuration 2.")
m10.reset()

# transfer Resuspension Buffer
m10.transfer(
    2.5, resuspension_buffer, [col[0].top() for col in temp_plate.cols()],
    blow_out=True)

# transfer Ligation Mix
m10.transfer(
    2.5, ligation_mix, [col[0].top() for col in temp_plate.cols()],
    blow_out=True)

# transfer RNA Adpater Index
for source, dest in zip(mag_plate.cols(), temp_plate.cols()):
    m10.transfer(2.5, source, dest, blow_out=True)

temp_module.set_temperature(30)
temp_module.wait_for_temp()
m300.delay(seconds=10)

# transfer Stop Ligation Buffer
for col in temp_plate.cols():
    m10.pick_up_tip()
    m10.transfer(5, stop_ligation_buffer, col, new_tip='never')
    m10.mix(3, 10, col)
    m10.blow_out(col)
    m10.drop_tip()


robot.pause("Place the plate on a Thermocycler to incubate at 85°C for 5 \
minutes. Remove the RNA Adapter Index from the Magnetic Module and replace \
the plate after the incubation. Place a new clean plate on the Temperature \
Module. See Configuration 3.")

# add AMPure XP Beads
for col in mag_plate.cols():
    m300.transfer(42, ampure_xp_beads, col, mix_after=(3, 30))

m300.delay(minutes=15)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# remove supernatant
for col in mag_plate.cols():
    m300.transfer(85, col, m300.trash_container.top())

# wash plate with 80% EtOH twice
for etoh in ethanol_1:
    m300.pick_up_tip()
    m300.transfer(
        200, etoh, [col[0].top() for col in mag_plate.cols()], new_tip='never')
    m300.delay(seconds=30)
    for col in mag_plate.cols():
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.transfer(230, col, m300.trash_container.top(), new_tip='never')
        m300.drop_tip()

robot.comment("Air dry for 15 minutes. During this time, replenish all of the \
tip racks.")
m300.delay(minutes=15)
m300.reset()
m10.reset()

mag_module.disengage()

# transfer resuspension buffer
for col in mag_plate.cols():
    m300.pick_up_tip()
    m300.transfer(52.5, resuspension_buffer, col, new_tip='never')
    m300.mix(3, 30, col)
    m300.blow_out(col)
    m300.drop_tip()

m300.delay(minutes=2)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# transfer supernatant to new plate
reuse_tip = m300.get_next_tip()
for source, dest in zip(mag_plate.cols(), temp_plate.cols()):
    m300.transfer(50, source, dest, blow_out=True, trash=False)

# distribute AMPure XP beads
m300.pick_up_tip()
m300.mix(5, 300, ampure_xp_beads)
m300.blow_out(ampure_xp_beads)
m300.distribute(
    50, ampure_xp_beads, [col[0].top() for col in temp_plate.cols()],
    blow_out=ampure_xp_beads)
new_tip = m300.get_next_tip()

# mix plate
m300.start_at_tip(reuse_tip)
for col in temp_plate.cols():
    m300.pick_up_tip()
    m300.mix(3, 80, col)
    m300.blow_out(col)
    m300.drop_tip()

robot.pause("Remove the plate on the Magnetic Module. Transfer the plate from \
the Temperature Module to the Magnetic Module. Place a new plate on the \
Temperature Module. Replenish all tip racks before resuming. See \
Configuration 4.")
for pipette in [m300, m10]:
    pipette.reset()
    pipette.start_at_tip(pipette.tip_racks[0].cols('1'))

robot._driver.run_flag.wait()
m300.delay(minutes=15)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# remove supernatant
for col in mag_plate.cols():
    m300.transfer(100, col, m300.trash_container.top())

# wash plate with 80% EtOH twice
for etoh in ethanol_2:
    m300.pick_up_tip()
    m300.transfer(
        200, etoh, [col[0].top() for col in mag_plate.cols()], new_tip='never')
    m300.delay(seconds=30)
    for col in mag_plate.cols():
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.transfer(230, col, m300.trash_container.top(), new_tip='never')
        m300.drop_tip()

m300.delay(minutes=15)
mag_module.disengage()

# transfer resuspension buffer
for col in mag_plate.cols():
    m10.pick_up_tip()
    m10.transfer(22.5, resuspension_buffer, col[0].top(), new_tip='never')
    m10.mix(3, 10, col)
    m10.blow_out(col)
    m10.drop_tip()

m300.delay(minutes=2)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# transfer supernatant to a new plate
for source, dest in zip(mag_plate.cols(), temp_plate.cols()):
    m10.transfer(20, source, dest, blow_out=True)

mag_module.disengage()

# transfer PCR Primer Cocktail
m10.pick_up_tip()
m10.transfer(
    5, pcr_primer_cocktail, [col[0].top() for col in temp_plate.cols()],
    blow_out=True, new_tip='never')

# transfer PCR Master Mix
for col in mag_plate.cols():
    if not m10.tip_attached:
        m10.pick_up_tip()
    m10.transfer(25, pcr_mastermix, col[0].top(), new_tip='never')
    m10.mix(3, 10, col)
    m10.blow_out(col)
    m10.drop_tip()

robot.pause("Place the plate on a Thermocycler for Amp PCR. Replenish all \
tip racks. Place a new plate on the Temperature Module. Replace the plate on \
the Magnetic Module before resuming. See Configuration 5.")
for pipette in [m300, m10]:
    pipette.reset()
    pipette.start_at_tip(pipette.tip_racks[0].cols('1'))

# transfer AMPure XP Beads
for col in mag_plate.cols():
    m300.pick_up_tip()
    m300.mix(3, 50, ampure_xp_beads)
    m300.transfer(50, ampure_xp_beads, col, new_tip='never')
    m300.mix(3, 50, col)
    m300.blow_out(col)
    m300.drop_tip()

m300.delay(minutes=15)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# wash plate with 80% EtOH twice
for etoh in ethanol_3:
    m300.pick_up_tip()
    m300.transfer(
        200, etoh, [col[0].top() for col in mag_plate.cols()], new_tip='never')
    m300.delay(seconds=30)
    for col in mag_plate.cols():
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.transfer(300, col, m300.trash_container.top(), new_tip='never')
        m300.drop_tip()

robot.comment("Air dry for 15 minutes. During this time, replenish all of the \
tip racks.")
m300.delay(minutes=15)
m300.reset()
mag_module.disengage()

# transfer resuspension buffer
for col in mag_plate.cols():
    m300.pick_up_tip()
    m300.transfer(32.5, resuspension_buffer, col, new_tip='never')
    m300.mix(3, 30, col)
    m300.blow_out(col)
    m300.drop_tip()

m300.delay(minutes=2)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# transfer supernatant to a new plate
for source, dest in zip(mag_plate.cols(), temp_plate.cols()):
    m300.transfer(30, source, dest, blow_out=True)
