from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 8',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
plate = labware.load('biorad-hardshell-96-PCR', '1')
mag_module = modules.load('magdeck', '4')
mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
trough = labware.load('trough-12row', '5')
temp_module = modules.load('tempdeck', '7')
temp_plate = labware.load(
    'opentrons-aluminum-block-96-PCR-plate', '7', share=True)
tuberack = labware.load('opentrons-aluminum-block-2ml-screwcap', '8')
tiprack_50 = labware.load('opentrons-tiprack-300ul', '2')
tiprack_10 = labware.load('opentrons-tiprack-10ul', '3')

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=[tiprack_10])

# reagent setup
pcr_mastermix = tuberack.wells('A1')
primer_mix = tuberack.wells('B1')
cleanup_beads = tuberack.wells('C1')
ethanol = tuberack.wells('D1')
buffer_eb = tuberack.wells('A2')
final_dest = tuberack.wells('D6')
sample = plate.wells('A1')
sample_dest = plate.wells('A2')

# create master mix
p50.transfer(25, pcr_mastermix, sample_dest)
p10.transfer(2.5, primer_mix, sample_dest, blow_out=True)

# transfer captured library DNA to master mix
p50.pick_up_tip()
p50.transfer(22.5, sample, sample_dest, new_tip='never')
p50.mix(15, 25, sample_dest)
p50.blow_out(sample_dest)
p50.drop_tip()

robot.pause('Transfer the PCR plate to the pre-heated thermocycler (98°C) and \
skip to the next step in the program. Place the plate back in slot 1 befor \
resuming the protocol.')

# transfer Target Pure NGS clean-up beads to a clean tube
mag_dest = mag_plate.wells('A1')
p50.pick_up_tip()
p50.mix(15, 50, cleanup_beads)
p50.blow_out(cleanup_beads)
p50.transfer(75, cleanup_beads, mag_dest, new_tip='never')
p50.drop_tip()

# transfer PCR product to beads
p50.pick_up_tip()
p50.transfer(50, sample_dest, mag_dest, new_tip='never')
p50.mix(20, 50, mag_plate)
p50.blow_out(mag_plate)
p50.drop_tip()

p50.delay(minutes=5)
robot._driver.run_flag.wait()
mag_module.engage()
p50.delay(minutes=5)

# remove supernatant
p50.transfer(150, mag_dest, p50.trash_container)

# wash the beads with 80% ethanol twice
for _ in range(2):
    p50.pick_up_tip()
    p50.transfer(200, ethanol, mag_dest.top(), new_tip='never')
    p50.delay(seconds=30)
    p50.transfer(250, mag_dest, p50.trash_container, new_tip='never')
    p50.drop_tip()
p10.transfer(10, mag_dest, p10.trash_container)

p50.delay(minutes=5)
robot._driver.run_flag.wait()
mag_module.disengage()

# resuspend beads with Buffer EB
p50.pick_up_tip()
p50.transfer(32.5, buffer_eb, mag_dest, new_tip='never')
p50.mix(15, 25, mag_dest)
p50.blow_out(mag_dest)
p50.drop_tip()

p50.delay(minutes=2)
robot._driver.run_flag.wait()
mag_module.engage()
p50.delay(minutes=2)

# transfer supernatant to a new clean tube
p50.transfer(30, mag_dest, final_dest)

mag_module.disengage()
