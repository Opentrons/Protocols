from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'First Capture (Part 4/8)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tubes = labware.load('tube-rack-2ml', '1')
samples_rack = labware.load('96-deep-well', '2')
wash_rack = labware.load('PCR-strip-tall', '3')
mag_plate = labware.load('biorad-hardshell-96-PCR', '5')
extra_rack = labware.load('PCR-strip-tall', '6')
waste_strip = extra_rack.cols('1')

# set up tip rack to accommodate single transfers with multi-channel pipette
tip_rack10 = labware.load('tiprack-10ul', '11')
tips_temp10 = []
for row in range(7, -1, -1):
    tips_temp10.append(tip_rack10.rows()[row])
tips10 = [well for row in tips_temp10 for well in row]
tip10_counter = 0

tip_rack300 = labware.load('opentrons-tiprack-300ul', '7')
tips_temp300 = []
for row in range(7, -1, -1):
    tips_temp300.append(tip_rack300.rows()[row])
tips300 = [well for row in tips_temp300 for well in row]
tip300_counter = 0

# modules
tempdeck = modules.load('tempdeck', '9')
tempdeck.set_temperature(42)
block = labware.load('opentrons-aluminum-block-96-PCR-plate', '9', share=True)

# pipettes:
m10 = instruments.P10_Multi(
    mount='right'
)
m300 = instruments.P300_Multi(
    mount='left'
)

# reagent setup
beads = tubes.wells('A1')
wash = tubes.wells('A2')
buffer1 = tubes.wells('A3')
HP3 = tubes.wells('A4')
buffer2 = tubes.wells('A5')
waste = tubes.wells('C1')
elution_mix = extra_rack.wells('A6')


def run_custom_protocol(number_of_pools: int = 4):
    global tip10_counter
    global tip300_counter

    # setup sample pools
    pools = samples_rack.wells('A1', length=number_of_pools)
    mag_pools = mag_plate.wells('A1', length=number_of_pools)

    # mix and distribute magnetic beads to samples
    m300.pick_up_tip(tips300[tip300_counter])
    m300.mix(10, 300, beads)
    m300.drop_tip()
    tip300_counter += 1
    for s in pools:
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(250, beads, s, new_tip='never')
        m300.mix(10, 250, s)
        m300.drop_tip()
        tip300_counter += 1

    robot.pause("Vortex sample plate at 1200rpm for 5 minutes before "
                "resuming.")

    # incubate at room temperature for 25 minutes
    m300.delay(minutes=25)

    robot.pause("Place the sample rack on the magnetic stand before resuming. "
                "Once resumed, the process will delay 2 minutes.")
    m300.delay(minutes=2)

    # transfer out supernatant from samples
    for s in mag_pools:
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(340, s.bottom(2), waste, new_tip='never')
        m300.drop_tip()
        tip300_counter += 1

    robot.pause("Remove the sample rack from the magnetic stand before "
                "resuming.")

    # distribute wash solution to samples and mix to resuspend
    for s in pools:
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(200, wash, s, new_tip='never')
        m300.mix(30, 180, s)
        m300.drop_tip()
        tip300_counter += 1

    # transfer samples to wash rack
    wash_dests = [wash_rack.wells(i*2+4, length=2)
                  for i in range(number_of_pools)]
    for pool, wash_dest in zip(pools, wash_dests):
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(100, pool, wash_dest, new_tip='never')
        m300.drop_tip()
        tip300_counter += 1

    robot.pause("Place the sample rack on the magnetic stand. Also, place the "
                "wash rack on tempdeck before resuming. Once the protocol is "
                "resumed, the process will pause for 30 minutes to allow the "
                "plate to incubate at 42˚C.")
    m300.delay(minutes=30)

    # consolidate samples from wash rack to samples rack
    new_samples_loc = mag_plate.wells('E1', length=number_of_pools)
    wash_dests_temp = [block.wells(i*2+4, length=2)
                       for i in range(number_of_pools)]
    for wash_set, s_dest in zip(wash_dests_temp, new_samples_loc):
        m300.pick_up_tip(tips300[tip300_counter])
        m300.consolidate(100, wash_set, s_dest, new_tip='never')
        m300.drop_tip()
        tip300_counter += 1

    # incubate at room temperature for 2 minutes
    m300.delay(minutes=2)

    # transfer samples from samples rack to extra rack
    for i, s in enumerate(new_samples_loc):
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(100, s, extra_rack.wells(i), new_tip='never')
        m300.drop_tip()
        tip300_counter += 1

    robot.pause("Remove the sample rack from the magnetic stand before "
                "resuming.")

    # distribute wash solution to samples and resuspend
    new_samples_loc = samples_rack.wells('E1', length=number_of_pools)
    for s in new_samples_loc:
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(200, wash, s, new_tip='never')
        m300.mix(30, 180, s)
        m300.drop_tip()
        tip300_counter += 1

    # transfer samples to wash rack
    wash_dests_temp = [block.wells(i*2+12, length=2)
                       for i in range(number_of_pools)]
    for s, dest in zip(new_samples_loc, wash_dests_temp):
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(100, s, dest, new_tip='never')
        m300.drop_tip()
        tip300_counter += 1

    robot.pause("Place the sample rack on the magnetic stand before resuming.")

    # consolidate samples from wash rack to sample rack
    new_samples_loc = mag_plate.wells('A2', length=number_of_pools)
    for wash_set, s in zip(wash_dests_temp, new_samples_loc):
        m300.pick_up_tip(tips300[tip300_counter])
        m300.consolidate(100, wash_set, s, new_tip='never')
        m300.drop_tip()
        tip300_counter += 1

    # incubate at room temperature for 2 minutes
    m300.delay(minutes=2)

    # transfer samples from sample rack to extra rack
    for s in new_samples_loc:
        m300.pick_up_tip(tips300[tip300_counter])
        m300.transfer(200, s, extra_rack.wells(i+4), new_tip='never')
        m300.drop_tip()
        tip300_counter += 1

    robot.pause("Remove the sample rack from the magnetic stand before "
                "resuming.")

    # distribute elution buffer to elution mix
    m300.pick_up_tip(tips300[tip300_counter])
    m300.transfer(31.35*number_of_pools, buffer1, elution_mix, new_tip='never')
    m300.drop_tip()
    tip300_counter += 1

    # transfer HP3 to elution mix
    m10.pick_up_tip(tips10[tip10_counter])
    m10.transfer(1.65*number_of_pools, HP3, elution_mix, new_tip='never')
    m10.drop_tip()
    tip10_counter += 1

    # mix elution mix
    m300.pick_up_tip(tips300[tip300_counter])
    m300.mix(5, 30, elution_mix)
    m300.drop_tip()
    tip300_counter += 1

    # distribute elution mix to samples and mix
    for s in samples_rack.wells('A2', length=number_of_pools):
        m10.pick_up_tip(tips10[tip10_counter])
        m10.transfer(23.5, elution_mix, s, new_tip='never')
        m10.mix(30, 10, s)
        m10.drop_tip()
        tip10_counter += 1

    # incubate at room temperature for 2 minutes
    m10.delay(minutes=2)

    robot.pause("Place the sample rack on the magnetic stand before resuming. "
                "Once the protocol is resumed, the robot will pause for 2 "
                "minutes to allow the plate to incubate at room temperature.")
    m10.delay(minutes=2)

    # transfer supernatant from sample rack to wash rack in 2 steps
    samples_mag = mag_plate.wells('A2', length=number_of_pools)
    wash_dests_temp = block.wells('E3', length=number_of_pools)
    for _ in range(2):
        for s, w in zip(samples_mag, wash_dests_temp):
            m10.pick_up_tip(tips10[tip10_counter])
            m10.transfer(10.5, s.bottom(2), w, new_tip='never')
            m10.drop_tip()
            tip10_counter += 1

    # transfer target buffer2 to wash rack
    m10.pick_up_tip(tips10[tip10_counter])
    m10.distribute(4, buffer2, wash_dests_temp, new_tip='never')
    m10.drop_tip()
    tip10_counter += 1
