from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
tips10_name = 'custom_tips_P10'
if tips10_name not in labware.list():
    labware.create(
        tips10_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60,
    )

tips300_name = 'custom_tips_P300'
if tips300_name not in labware.list():
    labware.create(
        tips300_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60,
    )

deepwell_name = 'Greiner-Masterblock-2ml-deepwell'
if deepwell_name not in labware.list():
    labware.create(
        deepwell_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=40,
        volume=2000
    )

strips_name = 'Greiner-Sapphire-PCR-strips'
if strips_name not in labware.list():
    labware.create(
        strips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.7,
        depth=20.2,
        volume=200
    )

# load modules and labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(deepwell_name, '1', share=True)
pcr_plate = labware.load(deepwell_name, '2', 'original PCR plate')
strips = labware.load(strips_name, '3', 'reagent strips')
trough = labware.load('trough-12row', '4')
tips10 = labware.load(tips10_name, '5')
tips300 = [labware.load(tips300_name, slot) for slot in ['6', '7', '8', '9']]

# pipettes
m10 = instruments.P10_Multi(mount='right', tip_racks=[tips10])
m300 = instruments.P300_Multi(mount='left', tip_racks=tips300)

# reagents
beads = strips.wells('A1')
propanol = trough.wells('A1')
etoh = trough.wells('A2')
eb = trough.wells('A3')
liquid_trash = trough.wells('A12')


def run_custom_protocol(
        number_of_sample_columns: int = 12
):
    if number_of_sample_columns < 1 or number_of_sample_columns > 12:
        raise Exception('Invalid number of sample columns.')

    if number_of_sample_columns % 4:
        num_pools = (number_of_sample_columns//4)+1
    else:
        num_pools = number_of_sample_columns//4

    # pool PCR reactions
    sources = [pcr_plate.rows('A')[4*i:4*i+4] for i in range(num_pools)]
    mag_locs = mag_plate.rows('A')[0:num_pools]
    for s, d in zip(sources, mag_locs):
        m300.consolidate(
            50,
            s,
            d,
            blow_out=True
        )

    # mix and transfer beads
    m10.pick_up_tip()
    m10.mix(5, 10, beads)
    m10.blow_out(beads.top())
    for d in mag_locs:
        if not m10.tip_attached:
            m10.pick_up_tip()
        m10.transfer(
            5,
            beads,
            d,
            blow_out=True,
            new_tip='never'
        )
        m10.drop_tip()

    # transfer propanol
    m300.transfer(
        200,
        propanol,
        [d.top() for d in mag_locs],
        blow_out=True
    )

    # incubate and mix
    for _ in range(5):
        for d in mag_locs:
            m300.pick_up_tip()
            m300.mix(3, 150, d)
            m300.drop_tip()
        m300.delay(minutes=3)

    # remove supernatant
    magdeck.engage(height=16)
    m300.delay(minutes=2)
    m300.transfer(
        220,
        mag_locs,
        liquid_trash,
        blow_out=True,
        new_tip='always'
    )

    # EtOH washes
    for _ in range(2):
        magdeck.disengage()
        for loc in mag_locs:
            offset = loc.from_center(r=0.8, h=-0.9, theta=0)
            dest = (loc, offset)
            m300.pick_up_tip()
            m300.transfer(
                900,
                etoh,
                dest,
                new_tip='never'
            )
            m300.mix(5, 300, loc)
            m300.drop_tip()
        magdeck.engage(height=16)
        m300.delay(minutes=2)
        m300.transfer(
            1000,
            mag_locs,
            liquid_trash,
            blow_out=True,
            new_tip='always'
        )

    # remove any excess supernatant
    m10.transfer(
        20,
        mag_locs,
        liquid_trash,
        blow_out=True,
        new_tip='always'
    )

    robot.comment('Airdrying beads 10 minutes...')
    robot._driver.run_flag.wait()
    m10.delay(minutes=10)
    # remove any excess supernatant
    m10.transfer(
        20,
        mag_locs,
        liquid_trash,
        blow_out=True,
        new_tip='always'
    )
    robot.comment('Airdrying beads 5 minutes...')
    robot._driver.run_flag.wait()
    m10.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.disengage()
    # transfer and mix EB
    for loc in mag_locs:
        offset = loc.from_center(r=0.8, h=-0.9, theta=0)
        dest = (loc, offset)
        m300.pick_up_tip()
        m300.transfer(
            55,
            eb,
            dest,
            new_tip='never'
        )
        m300.mix(5, 50, loc)
        m300.blow_out(loc.top())
        m300.drop_tip()
