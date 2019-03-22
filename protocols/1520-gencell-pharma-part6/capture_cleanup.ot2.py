from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Capture Clean-Up (Part 6/8)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tubes = labware.load('tube-rack-2ml', '1')
samples_rack = labware.load('96-deep-well', '2')
wash_rack = labware.load('96-PCR-tall', '3')
waste = labware.load('PCR-strip-tall', '5')

# set up tip rack to accommodate single transfers with multi-channel pipette
tip_rack300 = labware.load('opentrons-tiprack-300ul', '7')
tips_temp = []
for row in range(7, -1, -1):
    tips_temp.append(tip_rack300.rows()[row])
tips = [well for row in tips_temp for well in row]
tip_counter = 0

# modules
magdeck = modules.load('magdeck', '6')
mag_plate = labware.load('96-deep-well', '6', share=True)

# pipettes
m50 = instruments.P50_Multi(
    mount='right'
)
m300 = instruments.P300_Multi(
    mount='left'
)

# reagent setup
beads = tubes.wells('A1')
buffer = tubes.wells('A2')
etanol = tubes.wells('A3', length=2)


def run_custom_protocol(number_of_pools: int = 4):
    global tip_counter

    # set up samples
    pools = samples_rack.wells('A6', length=number_of_pools)
    mag_pools = mag_plate.wells('A6', length=number_of_pools)

    # mix and distribute magnetic beads to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.mix(10, 300, beads)
    m300.drop_tip()
    tip_counter += 1
    for s in pools:
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(45, beads, s, new_tip='never')
        m300.mix(10, 50, s)
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
    for i, s in enumerate(mag_pools):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(70, s.bottom(2), waste.wells(i), new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute etanol to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200,
                    etanol[0],
                    mag_pools,
                    disposal_vol=10,
                    new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(seconds=30)

    # transfer out supernatant from samples
    for i, s in enumerate(mag_pools):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(200,
                      s.bottom(2),
                      waste.wells(i+number_of_pools),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute ethanol to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200,
                    etanol[0],
                    mag_pools,
                    disposal_vol=10,
                    new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(seconds=30)

    # transfer out supernatant from samples
    for i, s in enumerate(mag_pools):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(200,
                      s.bottom(2),
                      waste.wells(i+number_of_pools*2),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(minutes=10)

    magdeck.disengage()
    robot.pause("Remove the sample rack from the magnetic module before "
                "resuming.")

    # distribute buffer to samples and mix
    for s in pools:
        m50.pick_up_tip(tips[tip_counter])
        m50.transfer(27.5, buffer, s, new_tip='never')
        m50.mix(15, 20, s)
        m50.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 2 minutes
    m50.delay(minutes=2)

    robot.pause("Place the sample rack on the magnetic module before "
                "resuming. The magdeck will engage for 2 minutes before the "
                "protocol resumes.")
    magdeck.engage(height=18)
    m300.delay(minutes=2)

    # transfer out supernatant from samples in 2 steps
    for _ in range(2):
        for i, s in enumerate(mag_pools):
            m50.pick_up_tip(tips[tip_counter])
            m50.transfer(12.5, s.bottom(2), waste.wells(i+44))
