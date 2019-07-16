from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
from opentrons.legacy_api.modules import tempdeck

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

"""Controlling two of the same module in the protocol:
1. SSH into robot
2. run $ls /dev/tty*
   you are looking for two values with the format /dev/ttyACM*
   you will use those values in line 27 and 28.
If you need to know which magdeck is hooked up to which port:
1. unplug one of the modules
2. run $ls /dev/tty* : the results correlates to the module that is plugged in
3. plug the other module in and run ls /dev/tty* again, you will be able to
   know the value of the second module
"""

# defining two Temperature Modules
tempdeck1 = tempdeck.TempDeck()
tempdeck2 = tempdeck.TempDeck()

tempdeck1._port = '/dev/ttyACM1'
tempdeck2._port = '/dev/ttyACM2'

if not robot.is_simulating():
    tempdeck1.connect()
    tempdeck2.connect()

tempdeck1.set_temperature(42)
tempdeck2.set_temperature(42)
tempdeck2.wait_for_temp()

# create custom plate
plate_name = 'Abgene-MIDI-96-800ul'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=27,
        volume=800
    )

# load modules and labware
magdeck = modules.load('magdeck', '1')
magplate = labware.load(plate_name, '1', share=True)
[modules.load('tempdeck', slot) for slot in ['4', '7']]
[plate_TM1, plate_TM2] = [
    labware.load('opentrons-aluminum-block-96-PCR-plate', slot, share=True)
    for slot in ['4', '7']
    ]
trough = labware.load('trough-12row', '2')
tuberack = labware.load('opentrons-tuberack-2ml-screwcap', '5')
tips10 = [labware.load('tiprack-10ul', slot) for slot in ['3', '6', '8']]
tips50 = [labware.load('opentrons-tiprack-300ul', str(slot))
          for slot in range(9, 12)]

# reagent setup
mm1 = [well for well in plate_TM2.columns('1')]
[fs1, rs, ss1, mm2, mm3] = [tuberack.wells(ind) for ind in range(5)]
[pb, eb, ps] = [trough.wells(ind) for ind in range(3)]
etoh = [chan for chan in trough.wells('A4', length=4)]
etoh_waste = [chan for chan in trough.wells('A8', length=4)]
liquid_waste = trough.wells('A12')


def run_custom_protocol(
        number_of_samples: int = 96,
        p10_mount: StringSelection('right', 'left') = 'right',
        p50_mount: StringSelection('right', 'left') = 'left',
        dual_index: StringSelection('yes', 'no') = 'yes'
):
    # checks
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples')
    if p10_mount == p50_mount:
        raise Exception('Invalid pipette mount combination')

    # pipettes
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=tips10)
    p50 = instruments.P50_Single(mount=p50_mount, tip_racks=tips50)

    # sample setup
    tm1_samples = plate_TM1.wells()[:number_of_samples]
    tm2_samples = plate_TM2.wells()[:number_of_samples]
    mag_samples = magplate.wells()[:number_of_samples]

    # tip check function
    tip10_max = len(tips10)*96
    tip50_max = len(tips50)*96
    tip10_count = 0
    tip50_count = 0

    def tip_check(pipette):
        nonlocal tip10_count
        nonlocal tip50_count
        if pipette == 'p50':
            tip50_count += 1
            if tip50_count > tip50_max:
                p50.reset()
                tip50_count = 1
                robot.pause('Please replace 50ul tipracks before resuming.')
        else:
            tip10_count += 1
            if tip10_count > tip10_max:
                p10.reset()
                tip10_count = 1
                robot.pause('Please replace 10ul tipracks before resuming.')

    """M1 First Strand cDNA Synthesis - High RNA Input"""

    def etoh_wash(inds):
        for wash in inds:
            tip_check('p50')
            p50.pick_up_tip()
            p50.transfer(
                120,
                etoh[wash],
                [s.top() for s in mag_samples],
                new_tip='never'
            )
            for s in mag_samples:
                if not p50.tip_attached:
                    tip_check('p50')
                    p50.pick_up_tip()
                p50.transfer(120, s, etoh_waste[wash], new_tip='never')
                p50.drop_tip()

    for s in tm1_samples:
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(5, fs1, s, new_tip='never')
        p10.mix(5, 5, s)
        p10.blow_out(s.bottom(5))
        p10.drop_tip()

    robot.pause('Seal the plate and put on a thermocycler for 3 min at 90°C, \
and hold at 42°C. Remove the plate from the thermocycler and put back on TM1 \
before resuming')

    for i, s in enumerate(tm1_samples):
        mm1_loc = mm1[i//12]
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(10, mm1_loc, s, new_tip='never')
        p10.mix(10, 10, s)
        p10.blow_out(s.bottom(5))
        p10.drop_tip()

    robot.pause('Seal the plate and place back in TM1 before resuming. The \
plate will then incubate for 15 minutes')
    robot._driver.run_flag.wait()
    p10.delay(minutes=15)
    robot._driver.run_flag.wait()
    robot.pause('Remove the seal. The reagent plate in TM2 can now be trashed')

    """M2 RNA Removal"""

    for s in tm1_samples:
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(5, rs, s, new_tip='never')
        p10.mix(10, 10, s)
        p10.blow_out(s.bottom(5))
        p10.drop_tip()

    tempdeck2.set_temperature(25)
    tempdeck2.wait_for_temp()
    robot._driver.run_flag.wait()
    robot.pause('Seal the plate, put it on a thermocycler for 10 min at 95°C, \
and replace on TM2 (now set at 25˚C).')

    """M3 Second Strand Synthesis"""

    for s in tm1_samples:
        tip_check('p50')
        p50.pick_up_tip()
        p50.transfer(10, ss1, s, new_tip='never')
        p50.mix(10, 25, s)
        p50.blow_out(s.top())
        p50.drop_tip()

    tempdeck1.deactivate()

    robot.pause('Seal the plate and put it on a thermocycler for 98°C/1min; \
ramp down to 25°C; 25°C/30min. Then unseal and replace it on TM2. Place a new \
MIDI plate on the magdeck. Place a new PCR plate on TM1.')

    for s in tm2_samples:
        tip_check('p50')
        p50.pick_up_tip()
        p50.transfer(5, mm2, s, new_tip='never')
        p50.mix(10, 30, s)
        p50.blow_out(s.top())
        p50.drop_tip()

    p50.delay(minutes=15)

    """M4 DNA Cleanup"""

    tip_check('p50')
    p50.pick_up_tip()
    p50.mix(10, 40, pb)
    p50.blow_out(pb.top())
    p50.distribute(
        16,
        pb,
        [s for s in mag_samples],
        disposal_vol=0,
        new_tip='never'
    )

    for source, dest in zip(tm2_samples, mag_samples):
        if not p50.tip_attached:
            tip_check('p50')
            p50.pick_up_tip()
        p50.transfer(35, source, dest, new_tip='never')
        p50.mix(15, 40, s)
        p50.blow_out(s.top())
        p50.drop_tip()

    p50.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p50.delay(minutes=3)

    for s in mag_samples:
        tip_check('p10')
        p10.transfer(51, s, liquid_waste)

    magdeck.disengage()

    for s in mag_samples:
        tip_check('p50')
        p50.pick_up_tip()
        p50.transfer(40, eb, s, new_tip='never')
        p50.mix(15, 30, s)
        p50.blow_out(s.top())
        p50.drop_tip()

    p50.delay(minutes=2)

    for s in mag_samples:
        tip_check('p50')
        p50.pick_up_tip()
        p50.transfer(48, ps, s, new_tip='never')
        p50.mix(15, 45, s)
        p50.blow_out(s.top())
        p50.drop_tip()

    p50.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p50.delay(minutes=3)

    for s in mag_samples:
        tip_check('p50')
        p50.transfer(96, s, liquid_waste)

    etoh_wash(range(2))

    p50.delay(minutes=5)

    magdeck.disengage()

    for s in mag_samples:
        tip_check('p50')
        p50.pick_up_tip()
        p50.transfer(20, eb, s, new_tip='never')
        p50.mix(15, 15, s)
        p50.blow_out(s.top())
        p50.drop_tip()

    p50.delay(minutes=2)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p50.delay(minutes=3)

    for source, dest in zip(mag_samples, tm1_samples):
        tip_check('p50')
        p50.transfer(17, source, dest, blow_out=True)

    """M5 PCR Amplification"""

    robot.pause("Place the i7 index plate on TM2")

    for s, index in zip(tm1_samples, tm2_samples):
        tip_check('p10')
        p10.pick_up_tip()
        p10.transfer(8, mm3, s, new_tip='never')
        p10.transfer(5, index, s, new_tip='never')
        p10.mix(10, 9, s)
        p10.blow_out(s.bottom(5))
        p10.drop_tip()

    if dual_index == 'yes':
        robot.pause("Replace i7 index plate with i5 index plate on TM2")
        for s, index in zip(tm1_samples, tm2_samples):
            tip_check('p10')
            p10.pick_up_tip()
            p10.transfer(5, s, index, new_tip='never')
            p10.mix(10, 9, s)
            p10.blow_out(s.bottom(5))
            p10.drop_tip()

    magdeck.disengage()

    robot.pause('Seal the plate on TM1, thermocycle, and replace on TM1. \
Replace the MIDI plate on the magdeck with a fresh plate. Replace the index \
plate on TM2 with a fresh PCR plate.')

    """M6 PCR Cleanup"""
    vol = 35 if dual_index == 'yes' else 30
    for source, dest in zip(tm1_samples, mag_samples):
        tip_check('p50')
        p50.pick_up_tip()
        p50.transfer(vol, source, dest, new_tip='never')
        p50.mix(15, 45, dest)
        p50.blow_out(dest.top())
        p50.drop_tip()

    p50.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p50.delay(minutes=3)

    sup_vol = 70 if dual_index == 'yes' else 60
    for s in mag_samples:
        tip_check('p50')
        p50.transfer(sup_vol, s, liquid_waste)

    magdeck.disengage()

    for reagent, mix_vol in zip([eb, ps], [25, 45]):
        for s in mag_samples:
            tip_check('p50')
            p50.pick_up_tip()
            p50.transfer(30, reagent, s, new_tip='never')
            p50.mix(15, mix_vol, s)
            p50.drop_tip()

    p50.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p50.delay(minutes=3)

    for s in mag_samples:
        tip_check('p50')
        p50.transfer(60, s, liquid_waste)

    etoh_wash([2, 3])

    p50.delay(minutes=5)
    magdeck.disengage()

    for s in mag_samples:
        tip_check('p50')
        p50.pick_up_tip()
        p50.transfer(20, eb, s, new_tip='never')
        p50.mix(15, 15, s)
        p50.drop_tip()

    p50.delay(minutes=2)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    p50.delay(minutes=3)

    for source, dest in zip(mag_samples, tm2_samples):
        tip_check('p50')
        p50.transfer(17, source, dest, blow_out=True)
