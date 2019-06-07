from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

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
trough = labware.load('trough-12row', '1')
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

# sample setup
mag_samples_single = [well for well in mag_plate.wells()]
mag_samples_multi = [well for well in mag_plate.rows('A')]
temp_samples_multi = [well for well in temp_plate.rows('A')]
barcodes_multi = [well for well in barcode_plate.rows('A')]

# reagent setup
spri_beads = reagent_plate.wells('A1')
pbs = reagent_plate.wells('A4')
etoh = trough.wells('A1')


def run_custom_protocol(
        P300_pipette_type: StringSelection('single', 'multi') = 'single'
        ):

    # pipettes
    m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)
    if P300_pipette_type == 'single':
        pipette300 = instruments.P300_Single(mount='left', tip_racks=tips300)
    else:
        pipette300 = instruments.P300_Multi(mount='left', tip_racks=tips300)

    # EtOH wash function
    def etoh_wash(num):
        # transfer EtOH to samples
        pipette300.pick_up_tip(etoh_tips.rows('A')[num])
        if P300_pipette_type == 'single':
            etoh_dests = mag_samples_single
        else:
            etoh_dests = mag_samples_multi
        pipette300.distribute(
            100,
            etoh,
            [s.top() for s in etoh_dests],
            new_tip='never'
            )
        pipette300.drop_tip()

        # remove supernatant
        pipette300.transfer(
            100,
            etoh_dests,
            pipette300.trash_container.top(),
            new_tip='always'
            )

    # transfer SPRI beads
    m10.transfer(10, spri_beads, mag_samples_multi, new_tip='always')

    # incubate for 10 minutes
    m10.delay(minutes=10)

    # engage magnet and incubate for an additional 5 minutes
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m10.delay(minutes=5)

    # remove supernatant
    m10.transfer(
        10,
        mag_samples_multi,
        m10.trash_container.top(),
        new_tip='always'
        )

    # 2 EtOH washes
    etoh_wash(0)
    etoh_wash(1)

    # allow samples to dry for 5 minutes
    m10.delay(minutes=5)

    # remove residue from washes with P10 pipette
    m10.transfer(
        10,
        mag_samples_multi,
        m10.trash_container.top(),
        new_tip='always'
        )

    # prompt user to resplace 10ul tips
    robot.pause('Please replace 10ul tipracks in slots 3, 5, and 6.')
    m10.reset()

    # transfer PBS
    magdeck.disengage()
    m10.transfer(4, pbs, mag_samples_multi, blow_out=True, new_tip='always')

    # engage magnet and incubate for 1 minute
    magdeck.engage(height=18)
    m10.delay(minutes=1)

    # transfer supernatant to plate on tempdeck
    m10.transfer(
        4,
        mag_samples_multi,
        temp_samples_multi,
        blow_out=True,
        new_tip='always'
        )

    # transfer barcodes to new plate
    m10.transfer(
        1,
        barcodes_multi,
        temp_samples_multi,
        blow_out=True,
        new_tip='always'
        )

    magdeck.disengage()
