from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cleanup PCR 2 (Part 8/8)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
wash_rack = labware.load('96-PCR-tall', '1')
samples_rack = labware.load('96-deep-well', '2')
tube_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '3')
waste_rack = labware.load('PCR-strip-tall', '4')

# set up tip rack to accommodate single transfers with multi-channel pipette
tip_rack = labware.load('opentrons-tiprack-300ul', '10')
tips_temp = []
for row in range(7, -1, -1):
    tips_temp.append(tip_rack.rows()[row])
tips = [well for row in tips_temp for well in row]
tip_counter = 0

# modules
tempdeck = modules.load('tempdeck', '5')
block = labware.load('opentrons-aluminum-block-96-PCR-plate', '5', share=True)
magdeck = modules.load('magdeck', '6')
mag_plate = labware.load('96-deep-well', '6', share=True)

# pipettes
m50 = instruments.P50_Multi(mount='right')

m300 = instruments.P300_Multi(mount='left')


def run_custom_protocol(
        number_of_pools: StringSelection('1', '2', '3', '4') = '4'):
    global tip_counter

    # reagent setup
    beads = tube_rack.wells('A1')
    buffer = tube_rack.wells('A2')
    etanol = tube_rack.wells('A3', to='A4')

    number_of_pools = int(number_of_pools)
    pools = samples_rack.wells('E6', length=number_of_pools)
    mag_pools = mag_plate.wells('E6', length=number_of_pools)

    # mix and transfer magnetic beads to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.mix(10, 300, beads)
    m300.drop_tip()
    tip_counter += 1
    for pool in pools:
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(90,
                      beads,
                      pool,
                      disposal_volume=5,
                      mix_after=(10, 120),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 10 minutes
    m300.delay(minutes=10)

    robot.pause("Place the sample rack on the magnetic module before "
                "resuming. The magdeck will engage for 2 minutes before the "
                "protocol resumes.")
    magdeck.engage(height=18)
    m300.delay(minutes=2)

    # transfer out supernatant from samples
    for i, pool in enumerate(mag_pools):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(140,
                      pool.bottom(2),
                      waste_rack.wells(i),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute ethanol to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200,
                    etanol[0],
                    [p.top() for p in mag_pools],
                    disposal_volume=10,
                    new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(seconds=30)

    # transfer out supernatant from samples
    for i, sample in enumerate(mag_pools):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(200,
                      sample.bottom(2),
                      waste_rack.wells(i+4),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute etanol to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200,
                    etanol[1],
                    [p.top() for p in mag_pools],
                    disposal_volume=10,
                    new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(seconds=30)

    # transfer out supernatant from samples
    for i, sample in enumerate(mag_pools):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(200,
                      sample.bottom(2),
                      waste_rack.wells(8+i),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 10 minutes
    m300.delay(minutes=10)

    magdeck.disengage()
    robot.pause("Remove the sample rack from the magnetic module.")

    # distribute buffer to samples
    for i, sample in enumerate(pools):
        m50.pick_up_tip(tips[tip_counter])
        m50.transfer(32.5,
                     buffer,
                     sample,
                     mix_after=(15, 20),
                     new_tip='never')
        m50.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 2 minutes
    m300.delay(minutes=2)

    robot.pause("Place the sample rack on the magnetic module before "
                "resuming. The magdeck will engage for 2 minutes before the "
                "protocol resumes.")
    magdeck.engage(height=18)
    m300.delay(minutes=2)

    # transfer out supernatant from samples in 2 steps
    for _ in range(2):
        for i, sample in enumerate(mag_pools):
            m50.pick_up_tip(tips[tip_counter])
            m50.transfer(15,
                         sample.bottom(2),
                         waste_rack.wells(48+i),
                         new_tip='never')
            m50.drop_tip()
            tip_counter += 1
