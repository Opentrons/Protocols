from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
output_plate = labware.load('96-PCR-tall', '2')
trough = labware.load('trough-12row', '4')

tiprack_50 = labware.load('tiprack-200ul', '3')

# instrument setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack_50])

# reagent setup
magnetic_beads = trough.wells('A1')
ethanol = trough.wells('A2')
water = trough.wells('A3')
liquid_waste = trough.wells('A12')

samples = mag_plate.cols('1')

# add beads to samples
m50.pick_up_tip()
m50.mix(3, 20, magnetic_beads)
m50.blow_out(magnetic_beads.top())
m50.transfer(16, magnetic_beads, samples, new_tip='never')
m50.mix(30, 16, samples)
m50.blow_out(samples[0].top())
m50.drop_tip()

# incubate for 2 minutes before removing supernatant
m50.delay(minutes=2)
robot._driver.run_flag.wait()
mag_module.engage()
m50.delay(minutes=1)
m50.transfer(50, samples, m50.trash_container.top())

# wash beads with 70% ethanol twice
for _ in range(2):
    m50.pick_up_tip()
    m50.transfer(200, ethanol, samples, air_gap=5, new_tip='never')
    m50.retract()
    m50.delay(seconds=30)
    m50.transfer(200, samples, m50.trash_container.top(), new_tip='never')
    m50.drop_tip()

# dry beads for 50 minutes
m50.delay(minutes=5)
robot._driver.run_flag.wait()
mag_module.disengage()

# resuspend beads in water
m50.pick_up_tip()
m50.transfer(20, water, samples, mix_after=(5, 15), new_tip='never')
m50.blow_out(samples[0].top())
m50.drop_tip()
m50.delay(minutes=5)

# transfer supernatant to new plate
robot._driver.run_flag.wait()
mag_module.engage()
m50.delay(minutes=1)
m50.transfer(20, samples, output_plate.cols('1'))

mag_module.disengage()
