from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NGS Library Prep Part 1',
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
rna_beads = trough.wells('A1')
bead_washing_buffer = trough.wells('A2', length=2)
elution_buffer = trough.wells('A4')
bead_binding_buffer = trough.wells('A5')
resuspension_buffer = trough.wells('A6')
fragment_mix = trough.wells('A7')
second_strand_mix = trough.wells('A8')
ampure_xp_beads = trough.wells('A9')
ethanol = trough.wells('A10', length=2)
cdna_mix = reagent_plate.cols('1')

# disengage Magnetic Module if it is engaged
if mag_module._engaged:
    mag_module.disengage()

# transfer RNA Purification Beads
m300.pick_up_tip()
for index in range(3):
    m300.mix(3, 300, rna_beads)
    m300.blow_out(rna_beads)
    m300.distribute(
        50, rna_beads, mag_plate.cols(index * 4, length=4),
        blow_out=rna_beads, new_tip='never')
m300.drop_tip()

# transfer samples
sample_plate = reagent_plate
for source, dest in zip(sample_plate.cols(), mag_plate.cols()):
    m300.transfer(50, source, dest)

robot.pause("Remove the plate on the Magnetic Module and place on a \
Thermocycler for mRNA Denaturation. Replenish the 200 uL tip racks. Remove \
the sample plate and replace with reagnet plate. Place the plate back on the \
Magnetic Module before resuming. Follow Configuration 2.")
m300.reset()

# remove supernatant
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)
for col in mag_plate.cols():
    m300.transfer(120, col, m300.trash_container.top())
mag_module.disengage()

# wash plate with Bead Washing Buffer
m300.pick_up_tip()
reuse_tip = m300.current_tip()
for col in mag_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.transfer(
        200, bead_washing_buffer[0], col, mix_after=(3, 150), trash=False)
mag_module.engage(height=14.94)
m300.delay(minutes=5)
m300.start_at_tip(reuse_tip)
for col in mag_plate.cols():
    m300.transfer(220, col, m300.trash_container.top())
mag_module.disengage()

# transfer Elution Buffer
for col in mag_plate.cols():
    m300.transfer(50, elution_buffer, col, mix_after=(3, 30))

robot.pause("Remove the plate on the Magnetic Module and place on a \
thermocycler for mRNA Elution 1. Replenish the 200 uL tip racks. Place \
the plate back on the Magnetic Module before resuming. Follow Configuration \
2.")
m300.reset()
m300.start_at_tip(m300.tip_racks[0].cols('1'))

# transfer Bead Binding Buffer
m300.pick_up_tip()
reuse_tip = m300.current_tip()
for col in mag_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.transfer(
        50, bead_binding_buffer, col, mix_after=(3, 30), trash=False)
m300.delay(minutes=5)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)
m300.start_at_tip(reuse_tip)
for col in mag_plate.cols():
    m300.transfer(70, col, m300.trash_container.top())
mag_module.disengage()

# wash plate with Bead Washing Buffer
m300.pick_up_tip()
reuse_tip = m300.current_tip()
for col in mag_plate.cols():
    if not m300.tip_attached:
        m300.pick_up_tip()
    m300.transfer(
        200, bead_washing_buffer[1], col, mix_after=(3, 150), trash=False)
mag_module.engage(height=14.94)
m300.delay(minutes=5)
m300.start_at_tip(reuse_tip)
for col in mag_plate.cols():
    m300.transfer(220, col, m300.trash_container.top())
mag_module.disengage()

# transfer Fragment, Prime, Finish Mix
for col in mag_plate.cols():
    m10.pick_up_tip()
    m10.transfer(
        19.5, fragment_mix, col[0].top(), blow_out=True, new_tip='never')
    m10.mix(3, 10, col)
    m10.blow_out(col)
    m10.drop_tip()

# remove supernatant
mag_module.engage(height=14.94)
m300.delay(minutes=5)
for col in mag_plate.cols():
    m10.transfer(17, col, m10.trash_container.top(), blow_out=True)

# transfer First strand cDNA mix
m10.transfer(
    8, cdna_mix, [col[0].top(-5) for col in mag_plate.cols()],
    blow_out=True)

# prepare temperature module for 16°C
temp_module.set_temperature(16)

robot.pause("Place the plate to a Thermocycler for cDNA Synthesis. \
Replenish all of the tip racks. Replace the plate back on the Magnetic \
Module before resuming. Follow Configuration 2.")
for pipette in [m300, m10]:
    pipette.reset()
    pipette.start_at_tip(pipette.tip_racks[0].cols('1'))

# transfer Resuspension Buffer
m10.transfer(
    5, resuspension_buffer, [col[0].top() for col in mag_plate.cols()],
    blow_out=True)

# transfer Second Strand Marking Master Mix
for col in mag_plate.cols():
    m10.pick_up_tip()
    m10.transfer(20, second_strand_mix, col[0].top(-5),
                 blow_out=True, new_tip='never')
    m10.mix(3, 10, col)
    m10.blow_out(col)
    m10.drop_tip()

temp_module.wait_for_temp()

robot.pause("The temperature on the Temperature Module is ready. Place the \
plate on the Temperature Module for 1 hour at 16°C. See Configuration 3. \
After 1 hour, place the plate back on the Magnetic Module before resuming. \
Place a new clean PCR plate on the Temperature Module. Replenish all of the \
tip racks. Follow Configuration 4.")
for pipette in [m300, m10]:
    pipette.reset()
    pipette.start_at_tip(pipette.tip_racks[0].cols('1'))

# transfer AMPure XP beads
for col in mag_plate.cols():
    m300.pick_up_tip()
    m300.transfer(90, ampure_xp_beads, col, mix_after=(3, 100),
                  new_tip='never')
    m300.blow_out(col)
    m300.drop_tip()

# incubate for 15 min at RT before engaging the Mag Module for 5 min
m300.delay(minutes=15)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# remove supernatant
for col in mag_plate.cols():
    m300.transfer(140, col, m300.trash_container.top())

# wash plate with ethanol twice
for etoh in ethanol:
    m300.pick_up_tip()
    m300.transfer(200, etoh, [col[0].top() for col in mag_plate.cols()],
                  new_tip='never')
    m300.delay(seconds=30)
    for col in mag_plate.cols():
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.transfer(200, col, m300.trash_container.top(), new_tip='never')
        m300.drop_tip()

# let dry for 15 min
m300.delay(minutes=15)
mag_module.disengage()

# transfer Resuspension Buffer
for col in mag_plate.cols():
    m10.pick_up_tip()
    m10.transfer(17.5, resuspension_buffer, col[0].top(), new_tip='never')
    m10.mix(3, 10, col)
    m10.blow_out(col)
    m10.drop_tip()

# incubate for 2 min at RT before engaging the Mag Module for 5 min
m300.delay(minutes=2)
robot._driver.run_flag.wait()
mag_module.engage(height=14.94)
m300.delay(minutes=5)

# transfer supernatant to a new plate
for source, dest in zip(mag_plate.cols(), temp_plate.cols()):
    m10.transfer(15, source, dest)
