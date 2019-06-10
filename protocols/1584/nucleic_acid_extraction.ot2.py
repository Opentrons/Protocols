from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Nucleic Acid Extraction',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'MidSci-96-Well'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=21,
        volume=200
    )

# labware
trough = labware.load('trough-12row', '2', 'trough')
fresh_plate = labware.load(plate_name, '3', 'fresh plate')
tips = [labware.load('opentrons-tiprack-300ul', str(slot))
        for slot in range(4, 10)]

# modules
magdeck = modules.load('magdeck', '1')
sample_plate = labware.load(plate_name, '1', share=True)

# instruments
m300 = instruments.P300_Multi(mount='right', tip_racks=tips)

# reagent setup
buffer_B = trough.wells('A1')
wash_buffer = trough.wells('A2')
nuclease_free_h2o = trough.wells('A3')
liquid_waste = trough.wells('A12')


def run_custom_protocol(number_of_sample_columns: int = 12):
    if number_of_sample_columns > 12:
        raise Exception("Please specify a valid number of sample columns.")

    def wash(vol):
        magdeck.disengage()

        # transfer wash buffer and mix
        for s in samples:
            m300.pick_up_tip()
            m300.transfer(vol, wash_buffer, s, new_tip='never')
            m300.mix(15, vol, s)
            m300.drop_tip()

        magdeck.engage(height=18)

        # incubate for 1.5 minutes
        m300.delay(minutes=1, seconds=30)

        # discard supernatant
        m300.transfer(vol, samples, liquid_waste, new_tip='always')

    samples = sample_plate.rows('A')[0:number_of_sample_columns]

    # transfer buffer B and mix
    for s in samples:
        m300.pick_up_tip()
        m300.transfer(60, buffer_B, s, new_tip='never')
        m300.mix(15, 185, s)
        m300.drop_tip()

    # incubate for 3 minutes
    m300.delay(minutes=3)

    for s in samples:
        m300.pick_up_tip()
        m300.mix(10, 185, s)
        m300.drop_tip()

    # incubate for 2 minutes
    m300.delay(minutes=2)

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)

    # incubate for 1.5 minutes
    m300.delay(minutes=1, seconds=30)

    # discard supernatant
    m300.transfer(170, samples, liquid_waste, new_tip='always')

    # perform washes
    wash(150)
    wash(100)

    # incubate for 6 minutes
    m300.delay(minutes=6)

    robot._driver.run_flag.wait()
    magdeck.disengage()

    # transfer nuclease-free water and mix
    for s in samples:
        m300.pick_up_tip()
        m300.transfer(50, nuclease_free_h2o, s, new_tip='never')
        m300.mix(20, 50, s)
        m300.drop_tip()

    # incubate for 5 minutes
    m300.delay(minutes=5)

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)

    # incubate for 1.5 minutes
    m300.delay(minutes=1, seconds=30)

    # transfer samples to a fresh plate
    dests = fresh_plate.rows('A')[0:number_of_sample_columns]
    m300.transfer(45, samples, dests, new_tip='always')
