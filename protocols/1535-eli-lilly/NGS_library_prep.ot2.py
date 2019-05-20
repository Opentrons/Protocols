from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NGS Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
barcode = labware.load('biorad-hardshell-96-PCR',
                       '2',
                       'barcode')
reagent_tuberack = labware.load('opentrons-aluminum-block-2ml-eppendorf',
                                '3',
                                'reagent tubes')
new_tuberack = labware.load('opentrons-aluminum-block-2ml-eppendorf',
                            '5',
                            'new_tubes')
trough = labware.load('trough-12row', '6')
tips10 = [labware.load('tiprack-10ul', str(slot)) for slot in range(7, 9)]
tips300 = [labware.load('tiprack-200ul', str(slot)) for slot in range(10, 12)]

# modules
tempdeck = modules.load('tempdeck', '1')
temp_plate = labware.load('biorad-hardshell-96-PCR',
                          '1',
                          share=True)

magdeck = modules.load('magdeck', '4')
mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)

# pipettes
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=tips10
)

p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tips300
)

# reagent setup
cleantag3 = reagent_tuberack.wells(0)
cleantag5 = reagent_tuberack.wells(1)
RNase_inhibitor = reagent_tuberack.wells(2)
enzyme1 = reagent_tuberack.wells(3)
enzyme2 = reagent_tuberack.wells(4)
buffer1 = reagent_tuberack.wells(5)
buffer2 = reagent_tuberack.wells(6)
water = reagent_tuberack.wells(7)
RT_primer = reagent_tuberack.wells(8)
RT_buffer = reagent_tuberack.wells(9)
RT_enzyme = reagent_tuberack.wells(10)
dNTP = reagent_tuberack.wells(11)
DTT = reagent_tuberack.wells(12)
PCR_mm = reagent_tuberack.wells(13)
forward_primer = reagent_tuberack.wells(14)
supernatant = reagent_tuberack.wells(20)

ethanol = trough.wells('A1')
beads = trough.wells('A2')
waste = trough.wells('A12')


def small_v_dist(vol, source, dests):
    p10.pick_up_tip()
    for d in dests:
        p10.transfer(vol, source, d, new_tip='never')
        p10.blow_out()
        p10.touch_tip(location=d, v_offset=-1)
    p10.drop_tip()


def run_custom_protocol(number_of_samples: int = 24):
    if number_of_samples > 24:
        raise Exception('Please specify 24 or fewer samples to fit in one '
                        'tube rack.')

    # set up sample wells
    temp_samples = [well for well in
                    temp_plate.wells('A1', length=number_of_samples)]
    mag_samples = [well for well in
                   mag_plate.wells('A1', length=number_of_samples)]
    new_tubes = [tube for tube in
                 new_tuberack.wells('A1', length=number_of_samples)]

    small_v_dist(1, cleantag3, temp_samples)
    small_v_dist(1, RNase_inhibitor, temp_samples)
    small_v_dist(1, enzyme1, temp_samples)
    small_v_dist(5, buffer1, temp_samples)

    for s in temp_samples:
        p10.pick_up_tip()
        p10.mix(3, 10, s)
        p10.drop_tip()

    tempdeck.set_temperature(28)
    tempdeck.wait_for_temp()
    p10.delay(minutes=60)
    robot._driver.run_flag.wait()

    tempdeck.set_temperature(65)
    tempdeck.wait_for_temp()
    p10.delay(minutes=20)

    small_v_dist(4, water, temp_samples)
    small_v_dist(1, buffer2, temp_samples)
    small_v_dist(1, RNase_inhibitor, temp_samples)
    small_v_dist(2, enzyme2, temp_samples)
    small_v_dist(1, cleantag5, temp_samples)

    for s in temp_samples:
        p10.pick_up_tip()
        p10.mix(3, 10, s)
        p10.drop_tip()

    tempdeck.set_temperature(28)
    tempdeck.wait_for_temp()
    p10.delay(minutes=60)

    robot._driver.run_flag.wait()
    tempdeck.set_temperature(65)
    tempdeck.wait_for_temp()
    p10.delay(minutes=20)

    small_v_dist(2, RT_primer, temp_samples)

    tempdeck.set_temperature(70)
    tempdeck.wait_for_temp()
    p10.delay(minutes=2)

    small_v_dist(1.92, water, temp_samples)
    small_v_dist(5.76, RT_buffer, temp_samples)
    small_v_dist(1.44, dNTP, temp_samples)
    small_v_dist(2.88, DTT, temp_samples)
    small_v_dist(1, RNase_inhibitor, temp_samples)
    small_v_dist(1, RT_enzyme, temp_samples)

    tempdeck.set_temperature(50)
    tempdeck.wait_for_temp()
    p10.delay(minutes=60)

    p300.distribute(40, PCR_mm, [s.top() for s in temp_samples])
    small_v_dist(2, forward_primer, temp_samples)
    for source, dest in zip(barcode.wells(), temp_samples):
        p10.pick_up_tip()
        p10.transfer(2,
                     source,
                     dest,
                     blow_out=True,
                     new_tip='never')
        p10.touch_tip(location=dest, v_offset=-1)
        p10.drop_tip()

    # external thermocycling
    robot.pause('Remove the samples from the temperature deck for external '
                'PCR. Replace on the temperature deck before resuming.')

    p300.distribute(80, beads, [s.top() for s in temp_samples])
    p300.delay(minutes=10)

    robot.pause('Place the samples on the magnetic deck before resuming.')
    robot._driver.run_flag.wait()
    magdeck.engage()
    p300.delay(minutes=5)
    p300.transfer(300, mag_samples, supernatant, new_tip='always')
    magdeck.disengage()

    p300.distribute(144, beads, [s.top() for s in mag_samples])
    p300.delay(minutes=10)
    robot._driver.run_flag.wait()
    magdeck.engage()
    p300.delay(minutes=5)
    p300.transfer(200, mag_samples, waste, new_tip='always')

    for _ in range(2):
        p300.distribute(500, ethanol, [s.top() for s in mag_samples])
        p300.delay(seconds=30)
        p300.transfer(500, mag_samples, waste, new_tip='always')

    p300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    for s in mag_samples:
        p10.pick_up_tip()
        p10.transfer(17, water, s.top(), new_tip='never')
        p10.mix(5, 10, s)
        p10.drop_tip()

    magdeck.engage()
    p10.delay(minutes=2)
    p10.transfer(15, mag_samples, new_tubes, new_tip='always', blow_out=True)

    magdeck.disengage()
