from opentrons import labware, instruments, modules, robot
import math

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# create custom plate
plate_name = 'Eppendorf-twintec-96-PCR'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.46,
        depth=14.6,
        volume=200
    )

# load labware
tubes50 = labware.load('opentrons-tuberack-50ml', '1')
barcode_plate = labware.load(plate_name, '2', 'barcode plate')
reagent_plate = labware.load(plate_name, '4', 'reagent plate')
magdeck = modules.load('magdeck', '7')
mag_plate = labware.load(plate_name, '7', share=True)
tempdeck = modules.load('tempdeck', '11')
temp_plate = labware.load(plate_name, '11', share=True)
if not robot.is_simulating():
    tempdeck.set_temperature(4)
    tempdeck.wait_for_temp()
tips10 = [labware.load('tiprack-10ul', slot) for slot in ['3', '5', '6']]
etoh_tips = labware.load('opentrons-tiprack-300ul', '8')
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in ['9', '10']]

# pipettes
m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)
p300 = instruments.P300_Single(mount='left', tip_racks=tips300)

# sample setup
mag_samples_single = [well for well in mag_plate.wells()]
mag_samples_multi = [well for well in mag_plate.rows('A')]
temp_samples_multi = [well for well in temp_plate.rows('A')]
barcodes_multi = [well for well in barcode_plate.rows('A')]

# reagent setup
spri_beads = reagent_plate.wells('A1')
pbs = reagent_plate.wells('A4')
etoh = tubes50.wells('A1')

# variables for height tracking
h_track = -15
r_cyl = 13.4


# EtOH height tracking function
def etoh_track(vol):
    global h_track

    # update height from which to aspirate
    dh = vol/(math.pi*(r_cyl**2))
    h_track -= dh


# EtOH wash function
def etoh_wash(num):
    # transfer EtOH to samples
    p300.pick_up_tip(etoh_tips.wells(num))
    for s in mag_samples_single:
        etoh_track(100)
        p300.transfer(100, etoh.top(h_track), s.top(), new_tip='never')
    p300.drop_tip()

    # remove supernatant
    for s in mag_samples_single[0:95]:
        p300.pick_up_tip()
        p300.aspirate(100, s)
        p300.dispense(100, p300.trash_container.top())
        p300.drop_tip(home_after=False)
    p300.pick_up_tip()
    p300.aspirate(100, mag_samples_single[95])
    p300.dispense(100, p300.trash_container.top())
    p300.drop_tip()


# transfer SPRI beads
for s in mag_samples_multi[0:11]:
    m10.pick_up_tip()
    m10.aspirate(10, spri_beads)
    m10.dispense(10, s)
    m10.drop_tip(home_after=False)
m10.pick_up_tip()
m10.aspirate(10, spri_beads)
m10.dispense(10, mag_samples_multi[11])
m10.drop_tip()

# incubate for 10 minutes
m10.delay(minutes=10)

# engage magnet and incubate for an additional 5 minutes
robot._driver.run_flag.wait()
magdeck.engage(height=18)
m10.delay(minutes=5)

# remove supernatant
for s in mag_samples_multi[0:11]:
    m10.pick_up_tip()
    m10.aspirate(10, s)
    m10.dispense(10, m10.trash_container.top())
    m10.drop_tip(home_after=False)
m10.pick_up_tip()
m10.aspirate(10, mag_samples_multi[11])
m10.dispense(10, m10.trash_container.top())
m10.drop_tip()

# 2 EtOH washes
etoh_wash(0)
etoh_wash(1)

# allow samples to dry for 5 minutes
m10.delay(minutes=5)

# remove residue from washes with P10 pipette
for s in mag_samples_multi[0:11]:
    m10.pick_up_tip()
    m10.aspirate(10, s)
    m10.dispense(10, m10.trash_container.top())
    m10.drop_tip(home_after=False)
m10.pick_up_tip()
m10.aspirate(10, mag_samples_multi[11])
m10.dispense(10, m10.trash_container.top())
m10.drop_tip()

# prompt user to resplace 10ul tips
robot.pause('Please replace 10ul tipracks in slots 3, 5, and 6.')
m10.reset()

# transfer PBS
magdeck.disengage()
for s in mag_samples_multi[0:11]:
    m10.pick_up_tip()
    m10.aspirate(4, pbs)
    m10.dispense(4, s)
    m10.blow_out(s)
    m10.drop_tip(home_after=False)
m10.pick_up_tip()
m10.aspirate(4, pbs)
m10.dispense(mag_samples_multi[11])
m10.blow_out(mag_samples_multi[11])
m10.drop_tip()

# engage magnet and incubate for 1 minute
magdeck.engage(height=18)
m10.delay(minutes=1)

# transfer supernatant to plate on tempdeck
for s, t in zip(mag_samples_multi[0:11], temp_samples_multi[0:11]):
    m10.pick_up_tip()
    m10.aspirate(4, s)
    m10.dispense(4, t)
    m10.blow_out(t)
    m10.drop_tip(home_after=False)
m10.pick_up_tip()
m10.aspirate(4, mag_samples_multi[11])
m10.dispense(4, temp_samples_multi[11])
m10.blow_out(temp_samples_multi[11])
m10.drop_tip()

# transfer barcodes to new plate
for b, t in zip(barcodes_multi[0:11], temp_samples_multi[0:11]):
    m10.pick_up_tip()
    m10.aspirate(1, b)
    m10.dispense(1, t)
    m10.blow_out(t)
    m10.drop_tip(home_after=False)
m10.pick_up_tip()
m10.aspirate(1, barcodes_multi[11])
m10.dispense(1, temp_samples_multi[11])
m10.blow_out(temp_samples_multi[11])
m10.drop_tip()

magdeck.disengage()
