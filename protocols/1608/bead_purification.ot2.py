from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Bead Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'Abgene-96-deepwell'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.0,
        depth=27,
        volume=800
    )

# load labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(
    'biorad-hardshell-96-PCR',
    '1',
    'magdeck plate',
    share=True
    )
sample_plate = labware.load(plate_name, '2', 'sample plate')
new_plate = labware.load(plate_name, '3', 'new plate')
ethanol_plate = labware.load(plate_name, '4', 'ethanol plate')
trough = labware.load('trough-12row', '5')
tips10 = [labware.load('tiprack-10ul', slot) for slot in ['6', '7', '8']]
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in ['9', '10']]

# instruments
m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)
m300 = instruments.P300_Multi(mount='left', tip_racks=tips300)

# reagent setup
mq = trough.wells('A1')
idte = trough.wells('A2')


def run_custom_protocol(
        number_of_sample_columns: int = 12
):
    # check input
    if number_of_sample_columns < 1 or number_of_sample_columns > 12:
        raise Exception('Please enter a valid number of sample columns to '
                        'process (1-12).')

    # sample setup
    samples = sample_plate.rows('A')[0:number_of_sample_columns]
    mag_samples = mag_plate.rows('A')[0:number_of_sample_columns]
    new_samples = new_plate.rows('A')[0:number_of_sample_columns]
    ethanol = ethanol_plate.rows('A')[0:number_of_sample_columns]

    # transfer samples to mag plate
    m10.transfer(
        8,
        samples,
        mag_samples,
        blow_out=True,
        new_tip='always'
    )

    # transfer MQ to mag plate
    for m in mag_samples:
        m10.pick_up_tip()
        m10.transfer(2, mq, m, new_tip='never')
        m10.mix(10, 5, m)
        m10.blow_out(m)
        m10.drop_tip()

    m10.delay(minutes=5)
    robot._driver.run_flag.wait()

    # remove supernatant
    magdeck.engage(height=18)
    m10.delay(minutes=2)
    m10.transfer(
        10,
        mag_samples,
        m10.trash_container.top(),
        blow_out=True,
        new_tip='always'
    )

    # 2 ethanol washes
    for _ in range(2):
        m300.pick_up_tip()
        m300.transfer(
            200,
            ethanol,
            [m.top() for m in mag_samples],
            new_tip='never'
        )
        m300.delay(seconds=30)

        for m in mag_samples:
            if not m300.tip_attached:
                m300.pick_up_tip()
            m300.transfer(
                300,
                mag_samples,
                m10.trash_container.top(),
                blow_out=True,
                new_tip='never'
            )
            m300.drop_tip()

    # incubate 15 minutes and disengage magnet
    m300.delay(minutes=15)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    for m in mag_samples:
        m10.pick_up_tip()
        m10.transfer(
            20,
            idte,
            m.top(),
            blow_out=True,
            new_tip='never'
        )
        m10.mix(10, 10, m)
        m10.drop_tip()

    m10.delay(minutes=2)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m10.delay(minutes=2)

    m10.transfer(
        20,
        mag_samples,
        new_samples,
        blow_out=True,
        new_tip='always'
    )
    magdeck.disengage()
