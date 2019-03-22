from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Clean-Up PCR 1 (Part 3/8)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tubes = labware.load('tube-rack-2ml', '1')
samples_rack = labware.load('96-PCR-tall', '2')
waste_rack = labware.load('PCR-strip-tall', '3')

# set up tip rack to accommodate single transfers with multi-channel pipette
tip_rack300 = labware.load('opentrons-tiprack-300ul', '7')
tips_temp = []
for row in range(7, -1, -1):
    tips_temp.append(tip_rack300.rows()[row])
tips = [well for row in tips_temp for well in row]
tip_counter = 0

# modules
magdeck = modules.load('magdeck', '6')
mag_plate = labware.load('biorad-hardshell-96-PCR', '6', share=True)

# pipettes:
m50 = instruments.P50_Multi(
    mount='right'
)
m300 = instruments.P300_Multi(
    mount='left'
)


def run_custom_protocol(number_of_samples: int = 4):
    global tip_counter

    samples = samples_rack.wells('A4', length=number_of_samples)
    mag_samples = mag_plate.wells('A4', length=number_of_samples)
    etanol = [well for row in tubes.rows()
              for well in row][2:int(2+number_of_samples/2)]
    beads = tubes.wells('A1')
    buffer = tubes.wells('A2')

    # mix and distribute magnetic beads to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.mix(10, 300, beads)
    m300.drop_tip()
    tip_counter += 1
    for s in samples:
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(90, beads, s, disposal_vol=5, new_tip='never')
        m300.mix(10, 120, s)
        m300.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 10 minutes
    m300.delay(minutes=10)

    robot.pause("Place the sample rack on the magnetic module before "
                "resuming. The magdeck will engage for 2 minutes before the "
                "protocol resumes.")
    magdeck.engage()
    m300.delay(minutes=2)

    # transfer out supernatant from samples
    for i, s in enumerate(mag_samples):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(140, s.bottom(2), waste_rack.wells(i), new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute ethanol to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200, etanol[0], mag_samples, new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(seconds=30)

    # transfer out supernatant from samples
    for i, s in enumerate(mag_samples):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(200,
                      s.bottom(2),
                      waste_rack.wells(i+number_of_samples),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute ethanol to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200, etanol[1], mag_samples, new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(seconds=30)

    # transfer out supernatant from samples
    for i, s in enumerate(mag_samples):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(200,
                      s.bottom(2),
                      waste_rack.wells(i+number_of_samples*2),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 10 minutes
    m300.delay(minutes=10)

    magdeck.disengage()
    robot.pause("Remove the sample rack from the magnetic module before "
                "resuming.")

    # distribute resuspension buffer to samples and mix
    for s in samples:
        m50.pick_up_tip(tips[tip_counter])
        m50.transfer(27.5, buffer, s, disposal_vol=5, new_tip='never')
        m50.mix(15, 20, s)
        m50.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 2 minutes
    m300.delay(minutes=2)

    robot.pause("Place the sample rack on the magnetic module before "
                "resuming. The magdeck will engage for 2 minutes before the "
                "protocol resumes.")
    magdeck.engage()
    m300.delay(minutes=2)

    # transfer out supernatant from samples in two steps
    for _ in range(2):
        for i, s in enumerate(mag_samples):
            m50.pick_up_tip(tips[tip_counter])
            m50.transfer(12.5,
                         s.bottom(2),
                         waste_rack.wells(i+48),
                         new_tip='never')
            m50.drop_tip()
            tip_counter += 1
