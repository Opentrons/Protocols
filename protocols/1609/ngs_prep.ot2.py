from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
pcr_name = 'Greiner-Sapphire-PCR-96'
if pcr_name not in labware.list():
    labware.create(
        pcr_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.65,
        depth=15,
        volume=200
    )

strips_name = 'Greiner-Sapphire-PCR-strips'
if strips_name not in labware.list():
    labware.create(
        strips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.69,
        depth=20.19,
        volume=200
    )

# load modules and labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(pcr_name, '1', share=True)
dna_plate = labware.load(pcr_name, '2', 'DNA plate')
strips = labware.load(strips_name, '3', 'reagent strips')
tempdeck = modules.load('tempdeck', '4')
temp_strips = labware.load(strips_name, '4', share=True)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
trough = labware.load('trough-12row', '5', 'reagent reservoir')
index_plate = labware.load(pcr_name, '6', 'index plate')
tips10 = [labware.load('tiprack-10ul', str(slot)) for slot in range(7, 10)]
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in range(10, 12)]

# pipettes
m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)
m300 = instruments.P300_Multi(mount='left', tip_racks=tips300)

# reagent setup
mq = trough.wells('A1')
twb = trough.wells('A2')
etoh = [chan for chan in trough.wells('A3', length=2)]
resus_buffer = trough.wells('A5')
liquid_waste = trough.wells('A12')

blt = strips.wells('A1')
tb1 = strips.wells('A2')
cleanngs_beads = strips.wells('A3')

tsb = temp_strips.wells('A1')
epm = temp_strips.wells('A2')


def run_custom_protocol(
        number_of_sample_columns: int = 6,
        index_start_column: int = 1
):
    # check valid sample column input
    if number_of_sample_columns < 1 or number_of_sample_columns > 6:
        raise Exception('Invalid number of sample columns.')
    if number_of_sample_columns + index_start_column > 13:
        raise Exception('Invalid index start column.')

    dna_samples = [well for well in
                   dna_plate.rows('A')[:number_of_sample_columns]]
    mag_samples1 = [well for well in
                    mag_plate.rows('A')[:number_of_sample_columns]]
    mag_samples2 = [well for well in
                    mag_plate.rows('A')[6:6+number_of_sample_columns]]
    index_start_ind = int(index_start_column-1)
    indexes = [well for well in
               index_plate.rows('A')[index_start_ind:
                                     index_start_ind+number_of_sample_columns]
               ]

    # small volume transfer function
    def small_vol_transfer(vol,
                           reagent,
                           samples=mag_samples1,
                           touch=True,
                           mix_after=True,
                           mix_before=False
                           ):
        m10.pick_up_tip()
        for s in mag_samples1:
            if mix_before:
                m10.mix(3, 9, reagent)
                m10.blow_out(reagent.top())
            m10.transfer(vol, reagent, s, new_tip='never')
            m10.blow_out(s)
            if mix_after:
                m10.mix(5, 9, s)
                m10.blow_out(s.top())
            if touch:
                offset = (s, s.from_center(r=1, theta=0, h=0))
                m10.move_to(offset)
        m10.drop_tip()

    # create initial mix
    small_vol_transfer(10, mq)
    small_vol_transfer(4, blt, mix_before=True)
    small_vol_transfer(4, tb1)

    # transfer and mix DNA samples
    for source, dest in zip(dna_samples, mag_samples1):
        m10.pick_up_tip()
        offset = (source, source.from_center(r=1, theta=0, h=0.9))
        m10.aspirate(2, source)
        m10.move_to(offset)
        m10.dispense(2, dest)
        m10.mix(5, 9, dest)
        m10.blow_out(dest.bottom(5))
        m10.drop_tip()

    robot.pause('Perform manual steps. Resume when finished.')

    # add TSB
    for s in mag_samples1:
        m10.pick_up_tip()
        offset = (tsb, tsb.from_center(r=1, theta=0, h=0.9))
        m10.aspirate(4, tsb)
        m10.move_to(offset)
        m10.dispense(4, s)
        m10.mix(5, 9, s)
        m10.blow_out(s.bottom(5))
        m10.drop_tip()

    robot.pause('Perform manual steps. Resume when finished.')

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m10.delay(minutes=3)

    for wash in range(2):
        sup_vol = 20 if wash == 0 else 50

        # remove supernatant
        for s in mag_samples1:
            m10.transfer(sup_vol, s, liquid_waste)

        magdeck.disengage()

        # transfer TWB
        for s in mag_samples1:
            offset = (s, s.from_center(r=0.9, theta=0, h=-0.9))
            m300.transfer(50, twb, offset, blow_out=True)

        magdeck.engage(height=18)
        m300.delay(minutes=2)

    # full supernatant removal
    for s in mag_samples1:
        m300.transfer(300, s, liquid_waste)
        m10.transfer(10, s, liquid_waste)

    # second reagent addition
    small_vol_transfer(10, mq, touch=True)

    robot.pause('Replace 10ul tipracks in slots 7-9 where necessary.')
    m10.reset()

    for s in mag_samples1:
        m10.pick_up_tip()
        offset = (epm, epm.from_center(r=1, theta=0, h=0.9))
        m10.aspirate(4, epm)
        m10.move_to(offset)
        m10.dispense(4, s)
        m10.mix(5, 9, s)
        m10.blow_out(s.bottom(5))
        m10.drop_tip()

    for ind, s in zip(indexes, mag_samples1):
        m10.pick_up_tip()
        m10.transfer(4, ind.bottom(), s, blow_out=True, new_tip='never')
        m10.mix(5, 9, s)
        m10.blow_out(s.bottom(5))
        offset = (s, s.from_center(r=0.9, theta=0, h=-0.9))
        m10.drop_tip()

    robot.pause('Perform manual steps. Resume when finished.')

    # add CleanNGS beads
    small_vol_transfer(18, cleanngs_beads, mix_before=True)
    small_vol_transfer(16, mq)

    # incubate off and then on magnet
    m10.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m10.delay(minutes=5)

    # transfer supernatant to new locations on mag plate
    for source, dest in zip(mag_samples1, mag_samples2):
        m300.transfer(
            50,
            source,
            dest,
            blow_out=True
        )

    magdeck.disengage()

    # transfer more CleanNGS beads
    small_vol_transfer(
        6,
        cleanngs_beads,
        samples=mag_samples2,
        mix_before=True,
        mix_after=True
    )

    # incubate off and then on magnet
    m10.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m10.delay(minutes=5)

    robot.pause('Replace 300ul tipracks in slots 10-11 where necessary.')
    m300.reset()

    # remove supernatant
    for s in mag_samples2:
        m300.transfer(50, s, liquid_waste)

    # 2 ethanol washes (slow to not disturb beads)
    for wash in range(2):
        m300.set_flow_rate(dispense=60)
        m300.distribute(
            100,
            etoh[wash],
            [s.top() for s in mag_samples2],
            disposal_vol=0
        )

        m300.delay(minutes=2)

        # remove supernatant
        m300.set_flow_rate(dispense=300)
        for s in mag_samples2:
            m300.transfer(50, s, liquid_waste)

    # remove excess supernatant and airdry 2x following washes
    for _ in range(2):
        for s in mag_samples2:
            m10.transfer(50, s, liquid_waste)
            m10.delay(minutes=5)

    robot.pause('Replace 300ul tipracks in slots 10-11 where necessary.')
    m300.reset()

    # resuspension buffer
    magdeck.disengage()
    for s in mag_samples2:
        m300.pick_up_tip()
        m300.transfer(
            55,
            resus_buffer,
            s,
            new_tip='never'
        )
        m300.mix(10, 50, s)
        m300.blow_out(s.top())
        m300.drop_tip()

    # final incubation
    magdeck.engage(height=18)
    robot.home('Incubate on magnet for 2 minutes.')
