from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Prep: Tagmentation and Clean-up (Part 1/8)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tubes = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
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
tempdeck = modules.load('tempdeck', '5')
tempdeck.set_temperature(58)
tempdeck.wait_for_temp()
block = labware.load('opentrons-aluminum-block-96-PCR-plate', '5', share=True)

magdeck = modules.load('magdeck', '6')
mag_plate = labware.load('biorad-hardshell-96-PCR', '6', share=True)

# pipettes:
m50 = instruments.P50_Multi(
    mount='right'
)

m300 = instruments.P300_Multi(
    mount='left'
)

# reagent setup
tagbuffer = tubes.wells('A1')
tagenzyme = tubes.wells('A2')
stopbuffer = tubes.wells('A3')
beads = tubes.wells('A4')
resusbuffer = tubes.wells('A5')
water = tubes.well('A6')
etanol1 = tubes.wells('B1')
etanol2 = tubes.wells('B2')


def run_custom_protocol(
    number_of_samples: StringSelection('3', '4', '6', '8',
                                       '9', '12', '16') = '4'):
    global tip_counter

    # set up pools based on sample number
    number_of_samples = int(number_of_samples)
    if number_of_samples in [3, 6, 9]:
        num_pools = int(number_of_samples/3)
        pools = [samples_rack.wells(i*3, length=3) for i in range(num_pools)]
        mag_pools = [mag_plate.wells(i*3, length=3) for i in range(num_pools)]
    else:
        num_pools = int(number_of_samples/4)
        pools = [samples_rack.wells(i*4, length=4) for i in range(num_pools)]
        mag_pools = [mag_plate.wells(i*4, length=4) for i in range(num_pools)]
    all_samples = [s for pool in pools for s in pool]
    all_mag_samples = [s for pool in mag_pools for s in pool]

    # distribute tagbuffer to samples
    m50.pick_up_tip(tips[tip_counter])
    m50.distribute(25,
                   tagbuffer,
                   [s.top() for s in all_samples],
                   disposal_vol=5,
                   new_tip='never')
    m50.drop_tip()
    tip_counter += 1

    # distribute tagenzyme to samples
    for s in all_samples:
        m50.pick_up_tip(tips[tip_counter])
        m50.distribute(15,
                       tagenzyme,
                       s,
                       disposal_vol=3,
                       new_tip='never')
        m50.mix(10, 35, s)
        m50.drop_tip()
        tip_counter += 1

    robot.pause("Place samples on tempdeck before resuming. Once the protocol "
                "is resumed, the process will pause for 10 minutes to allow "
                "samples to incubate at 58˚C")
    m50.delay(minutes=10)

    # distribute stopbuffer to samples
    for s in all_samples:
        m50.pick_up_tip(tips[tip_counter])
        m50.distribute(15,
                       stopbuffer,
                       s,
                       disposal_vol=5,
                       new_tip='never')
        m50.mix(15, 45, s)
        m50.drop_tip()
        tip_counter += 1

    robot.pause("Remove samples from the tempdeck before resuming. Once the "
                "protocol is resumed, the process will pause for 4 minutes "
                "to allow samples to incubate at room temperature.")

    # incubate at room temperature for 4 minutes
    m50.delay(minutes=4)

    # mix and distribute magnetic beads to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.mix(10, 300, beads)
    m300.drop_tip()
    for s in all_samples:
        m300.pick_up_tip(tips[tip_counter])
        m300.distribute(65,
                        beads,
                        s,
                        disposal_vol=5,
                        new_tip='never')
        m300.mix(10, 100, s)
        m300.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 8 minutes
    m300.delay(minutes=8)

    robot.pause("Place the sample rack on the magnetic module before "
                "resuming. The magdeck will engage for 2 minutes before the "
                "protocol resumes.")
    magdeck.engage()
    m300.delay(minutes=2)

    # transfer out supernatant from samples
    for i, s in enumerate(all_mag_samples):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(130, s.bottom(2), waste_rack.wells(i), new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute ethanol1 to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200,
                    etanol1,
                    [s.top() for s in all_mag_samples],
                    disposal_vol=10,
                    new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate for 30 seconds
    m300.delay(seconds=30)

    # transfer out supernatant from samples
    for i, s in enumerate(all_mag_samples):
        m300.pick_up_tip(tips[tip_counter])
        m300.transfer(200,
                      s.bottom(2),
                      waste_rack.wells(i+number_of_samples),
                      new_tip='never')
        m300.drop_tip()
        tip_counter += 1

    # distribute ethanol2 to samples
    m300.pick_up_tip(tips[tip_counter])
    m300.distribute(200,
                    etanol2,
                    all_mag_samples,
                    disposal_vol=10,
                    new_tip='never')
    m300.drop_tip()
    tip_counter += 1

    # incubate at room temperature for 30 seconds
    m300.delay(seconds=30)

    for i, s in enumerate(all_mag_samples):
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

    # distribute resuspension buffer to samples
    for s in all_samples:
        m50.pick_up_tip(tips[tip_counter])
        m50.transfer(22.5,
                     resusbuffer,
                     s,
                     disposal_vol=5,
                     new_tip='never')
        m50.mix(15, 18, s)
        m50.drop_tip()
        tip_counter += 1

    # incubate at room temperature for 2 minutes
    m50.delay(minutes=2)

    robot.pause("Place the sample rack on the magnetic module before "
                "resuming. The magdeck will engage for 2 minutes before the "
                "protocol resumes.")
    magdeck.engage()
    m50.delay(minutes=2)

    # transfer out supernatant from samples in two steps
    for _ in range(2):
        for i, s in enumerate(all_mag_samples):
            m300.pick_up_tip(tips[tip_counter])
            m300.transfer(200,
                          s.bottom(2),
                          waste_rack.wells(i+24),
                          new_tip='never')
            m300.drop_tip()
            tip_counter += 1
