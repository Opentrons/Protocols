from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NGS Library Prep Part 4/4: M6 PCR Cleanup',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

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
trough = labware.load('usascientific_12_reservoir_22ml', '2')
tempdeck = modules.load('tempdeck', '4')
plate_TM = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul', '4', share=True)
tempdeck.set_temperature(25)
tempdeck.wait_for_temp()
reagent_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul', '5', 'reagent plate')
plate_2 = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul', '7')
tips10 = [labware.load('tiprack-10ul', slot)
          for slot in ['3', '6', '8']]
tips300 = [labware.load('opentrons-tiprack-300ul', str(slot))
           for slot in range(9, 12)]


def run_custom_protocol(
        number_of_samples: int = 96,
        p10_multi_mount: StringSelection('right', 'left') = 'right',
        p300_multi_mount: StringSelection('left', 'right') = 'left',
        dual_index: StringSelection('yes', 'no') = 'yes',
        reagent_starting_column: int = 1
):
    # checks
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples')
    if p10_multi_mount == p300_multi_mount:
        raise Exception('Invalid pipette mount combination')
    if reagent_starting_column > 7:
        raise Exception('Invlaid reagent starting column')

    # pipettes
    m10 = instruments.P10_Multi(mount=p10_multi_mount, tip_racks=tips10)
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)

    # reagent setup
    [fs2e1, fs1, rs, ss1, ss2e2, pcre3] = [
        reagent_plate.rows('A')[ind]
        for ind in range(reagent_starting_column-1, reagent_starting_column+5)
    ]
    [pb, eb, ps] = [trough.wells(ind) for ind in range(3)]
    etoh = [chan for chan in trough.wells('A4', length=4)]
    etoh_waste = [chan for chan in trough.wells('A8', length=4)]
    liquid_waste = trough.wells('A12')

    # sample setup
    num_cols = math.ceil(number_of_samples/8)
    samples_TM = plate_TM.rows('A')[:num_cols]
    samples_2 = plate_2.rows('A')[:num_cols]
    samples_mag = magplate.rows('A')[:num_cols]

    # tip check function
    tip10_max = len(tips10)*12
    tip300_max = len(tips300)*12
    tip10_count = 0
    tip300_count = 0

    def tip_check(pipette):
        nonlocal tip10_count
        nonlocal tip300_count
        if pipette == 'p300':
            tip300_count += 1
            if tip300_count > tip300_max:
                m300.reset()
                tip300_count = 1
                robot.pause('Please replace 300ul tipracks before resuming.')
        else:
            tip10_count += 1
            if tip10_count > tip10_max:
                m10.reset()
                tip10_count = 1
                robot.pause('Please replace 10ul tipracks before resuming.')

    def etoh_wash(inds):
        for wash in inds:
            tip_check('p300')
            m300.pick_up_tip()
            m300.transfer(
                120,
                etoh[wash],
                [s.top() for s in samples_mag],
                new_tip='never'
            )
            for s in samples_mag:
                if not m300.tip_attached:
                    tip_check('p300')
                    m300.pick_up_tip()
                m300.transfer(120, s, etoh_waste[wash], new_tip='never')
                m300.drop_tip()

    """M6 PCR Cleanup"""
    vol = 35 if dual_index == 'yes' else 30
    for source, dest in zip(samples_2, samples_mag):
        tip_check('p300')
        m300.pick_up_tip()
        m300.transfer(vol, source, dest, new_tip='never')
        m300.mix(15, 45, dest)
        m300.blow_out(dest.top())
        m300.drop_tip()

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)

    sup_vol = 70 if dual_index == 'yes' else 60
    for s in samples_mag:
        tip_check('p300')
        m300.transfer(sup_vol, s, liquid_waste)

    magdeck.disengage()

    for reagent, mix_vol in zip([eb, ps], [25, 45]):
        for s in samples_mag:
            tip_check('p300')
            m300.pick_up_tip()
            m300.transfer(30, reagent, s, new_tip='never')
            m300.mix(15, mix_vol, s)
            m300.drop_tip()

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)

    for s in samples_mag:
        tip_check('p300')
        m300.transfer(60, s, liquid_waste)

    etoh_wash([2, 3])

    m300.delay(minutes=5)
    magdeck.disengage()

    for s in samples_mag:
        tip_check('p300')
        m300.pick_up_tip()
        m300.transfer(20, eb, s, new_tip='never')
        m300.mix(15, 15, s)
        m300.drop_tip()

    m300.delay(minutes=2)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=3)

    for source, dest in zip(samples_mag, samples_TM):
        tip_check('p300')
        m300.transfer(17, source, dest, blow_out=True)

    magdeck.disengage()
