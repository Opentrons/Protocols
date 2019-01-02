from opentrons import labware, instruments, modules

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }


def run_custom_protocol(
        tube_height: float=43,
        engage_height: float=14.94):
    rack_name = '1.2mL_96-well_tube_rack'
    if rack_name not in labware.list():
        labware.create(
            rack_name,
            grid=(12, 8),
            spacing=(9, 9),
            diameter=7,
            depth=tube_height,
            volume=1200
            )

    # labware setup
    mag_module = modules.load('magdeck', '1')
    mag_plate = labware.load(rack_name, '1', share=True)
    plate = labware.load('biorad-hardshell-96-PCR', '2')
    tiprack_50 = labware.load('opentrons-tiprack-300ul', '3')
    trough = labware.load('trough-12row', '4')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

    # instruments setup
    m50 = instruments.P50_Multi(
        mount='left',
        tip_racks=[tiprack_50])

    m300 = instruments.P300_Multi(
        mount='right',
        tip_racks=[tiprack_300])

    # reagent setup
    samples = mag_plate.cols('1')
    beads = mag_plate.cols('2')
    buffer_A = trough.wells('A1')
    buffer_B = trough.wells('A2')
    buffer_C = trough.wells('A3')
    buffer_D = trough.wells('A4')
    buffer_E = trough.wells('A5')

    mag_module.disengage()

    m300.pick_up_tip()
    m300.transfer(500, buffer_A, samples[0].top(), new_tip='never')
    m300.mix(5, 250, samples)
    m300.move_to(samples[0].top(10))
    m300.delay(minutes=5)
    m300.mix(5, 250, samples)
    m300.drop_tip()
    m300.delay(minutes=5)

    m300.pick_up_tip()
    m300.transfer(500, buffer_B, samples[0].top(), new_tip='never')
    m300.mix(5, 250, samples)
    m300.transfer(1100, samples, beads, new_tip='never')
    m300.mix(5, 250, beads)
    m300.move_to(beads.top(10))
    m300.delay(minutes=5)
    m300.mix(5, 250, beads)
    m300.drop_tip()
    m300.delay(minutes=5)

    mag_module.engage(height=engage_height)
    m300.delay(minutes=2)

    m300.transfer(1200, beads, m300.trash_container.top())
    mag_module.disengage()

    for _ in range(2):
        m300.pick_up_tip()
        m300.transfer(250, buffer_C, beads, new_tip='never')
        m300.mix(5, 100, beads)
        m300.move_to(beads[0].top(10))
        mag_module.engage(height=engage_height)
        m300.delay(seconds=30)
        m300.transfer(300, beads, m300.trash_container.top(), new_tip='never')
        m300.drop_tip()
        mag_module.disengage()

    for _ in range(2):
        m300.pick_up_tip()
        m300.transfer(250, buffer_D, beads, new_tip='never')
        m300.mix(5, 100, beads)
        m300.move_to(beads[0].top(10))
        mag_module.engage(height=engage_height)
        m300.delay(seconds=30)
        m300.transfer(300, beads, m300.trash_container.top(), new_tip='never')
        m300.drop_tip()
        mag_module.disengage()

    m50.pick_up_tip()
    m50.transfer(20, buffer_E, beads, new_tip='never')
    m50.mix(5, 15, beads)
    m50.move_to(beads[0].top(10))
    mag_module.engage(height=engage_height)
    m50.delay(seconds=30)
    m50.transfer(25, beads, plate.cols('1'), new_tip='never')
    m50.drop_tip()
