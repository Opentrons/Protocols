from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
PCR_plate_name = 'FrameStar-96-PCR'
if PCR_plate_name not in labware.list():
    labware.create(
        PCR_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.50,
        depth=15.10,
        volume=200
    )

# labware and modules
magdeck = modules.load('magdeck', '1')
sample_plate = labware.load(PCR_plate_name, '1', 'sample plate', share=True)
fresh_plate = labware.load(PCR_plate_name, '2', 'fresh plate for supernatant')
trough = labware.load('trough-12row', '3')
tips50 = [labware.load('opentrons-tiprack-300ul', slot)
          for slot in ['4', '5', '6', '7']]
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in ['8', '9']]

# pipettes
m50 = instruments.P50_Multi(mount='right', tip_racks=tips50)
m300 = instruments.P300_Multi(mount='left', tip_racks=tips300)

# reagents
beads = trough.wells('A1')
ethanol = [chan for chan in trough.wells('A3', 'A4')]
elution_buffer = trough.wells('A6')
liquid_waste = [chan for chan in trough.wells('A10', to='A12')]


def run_custom_protocol(number_of_sample_columns: int = 12):

    if number_of_sample_columns > 12:
        raise Exception('Please specify 12 or fewer sample columns.')

    samples = [s for s in sample_plate.rows('A')][:number_of_sample_columns]
    elution_wells = [s for s in
                     fresh_plate.rows('A')][:number_of_sample_columns]

    # bead mix and transfer
    m50.pick_up_tip()
    m50.mix(5, 50, beads)
    m50.transfer(25, beads, samples[0], new_tip='never')
    m50.mix(10, 25, samples[0])
    m50.drop_tip()

    for s in samples[1:]:
        m50.pick_up_tip()
        m50.transfer(25, beads, s, blow_out=True, new_tip='never')
        m50.mix(10, 25, s)
        m50.drop_tip()

    # incubate at room temp for 8 minutes
    m50.delay(minutes=8)

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m50.delay(minutes=5)

    # remove supernatant
    m50.transfer(24, samples, liquid_waste[0], new_tip='always')

    # ethanol wash fxn
    def ethanol_wash(eth_source, waste_dest):

        for s in samples:
            m300.pick_up_tip()
            m300.transfer(
                200,
                eth_source,
                s.top(),
                new_tip='never',
                blow_out=True
                )
            m300.delay(seconds=30)
            m300.transfer(210, s, waste_dest, new_tip='never')
            m300.drop_tip()

    # ethanol washes
    ethanol_wash(ethanol[0], liquid_waste[1])
    ethanol_wash(ethanol[1], liquid_waste[2])

    # dry at room temp for 5 minutes
    m300.delay(minutes=5)

    robot._driver.run_flag.wait()
    magdeck.disengage()

    # transfer elution buffer and mix
    for s in samples:
        m50.pick_up_tip()
        m50.transfer(17.5, elution_buffer, s, new_tip='never')
        m50.mix(10, 17.5, s)
        m50.drop_tip()

    # incubate both with magnet disengaged and engaged
    m50.delay(minutes=2)

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)

    m50.delay(minutes=2)

    robot._driver.run_flag.wait()
    robot.pause('Load fresh plate in slot 2 if you have not already done so.')

    # transfer eluted supernatant to fresh plate
    m50.transfer(15, samples, elution_wells, blow_out=True, new_tip='always')
