from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
reagent_res = labware.load(
    'usascientific_12_reservoir_22ml', '1', 'reagent reservoir')
pbs_t = labware.load('agilent_1_reservoir_290ml', '2', 'PBS-T').wells(0)
wash_buff = labware.load(
    'agilent_1_reservoir_290ml', '3', 'wash buffer').wells(0)
tiprack_single = labware.load('opentrons_96_tiprack_300ul', '4')
tuberack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap',
    '5',
    'reagent tube block'
)
tipracks_multi = [
    labware.load('opentrons_96_tiprack_300ul', slot)
    for slot in ['6', '8', '9', '11']
]
magdeck = modules.load('magdeck', '7')
magplate = labware.load('biorad_96_wellplate_200ul_pcr', '7', share=True)
tempdeck = modules.load('tempdeck', '10')
temp_plate = labware.load('biorad_96_wellplate_200ul_pcr', '10', share=True)
tempdeck.set_temperature(41)

# reagents
hb = [tube for tube in tuberack.columns('1')]
beads = tuberack.wells('A2')

rxn_mm = reagent_res.wells(0)
hrp = reagent_res.wells(1)
substrate = reagent_res.wells(2)
waste = [chan.top() for chan in reagent_res.wells()][4:]

example_csv = """
1,2, 4
3, 5
6
7, 8
10,11
"""

example_hb_csv = """,column 1,column 2,column 3,column 4,column 5,column 6,\
column 7,column 8,column 9,column 10,column 11,column 12
hb0,,10,15,,10,15,,20,,,,
hb1,20,10,5,,,,,,,,,
hb2,,,,20,10,5,,,,,,
hb3,,,,,,,20,,,,,
"""


def run_custom_protocol(
        p50_multi_mount: StringSelection('right', 'left') = 'right',
        p300_multi_mount: StringSelection('left', 'right') = 'left',
        HB_CSV: FileInput = example_hb_csv,
        replicate_CSV: FileInput = example_csv
):
    # check
    if p50_multi_mount == p300_multi_mount:
        raise Exception('Pipette mount selections must be distinct.')

    # pipettes
    m50 = instruments.P50_Multi(mount=p50_multi_mount)
    m300 = instruments.P300_Multi(mount=p300_multi_mount)

    # parse
    [rep_sets_m, rep_sets_t] = [
        [[plate.rows('A')[int(col)-1] for col in line.split(',')]
            for line in replicate_CSV.splitlines() if line]
        for plate in [magplate, temp_plate]
    ]
    # samples
    mag_samples_m = [col for set in rep_sets_m for col in set]
    mix_sets_m = []
    mix_sets_t = []
    for line in replicate_CSV.splitlines()[1:]:
        if line:
            set_m = []
            set_t = []
            for col in line.split(','):
                col_ind = int(col) - 1
                angle = 0 if col_ind % 2 == 0 else math.pi
                mix_well_m = magplate.rows('A')[col_ind]
                mix_well_t = temp_plate.rows('A')[col_ind]
                set_m.append(
                    (
                     mix_well_m,
                     mix_well_m.from_center(r=0.9, h=-0.7, theta=angle)
                    )
                )
                set_t.append(
                    (
                     mix_well_t,
                     mix_well_t.from_center(r=0.9, h=-0.7, theta=angle)
                    )
                )
            mix_sets_m.append(set_m)
            mix_sets_t.append(set_t)

    tip_count_s = 0
    tip_max_s = 96
    tip_locs_s = [
        tip for col in tiprack_single.columns() for tip in col[len(col)-1::-1]]
    tip_count_m = 0
    tip_max_m = len(tipracks_multi)*12
    tip_locs_m = [tip for rack in tipracks_multi for tip in rack.rows('A')]

    def pick_up(pipette, mode):
        nonlocal tip_count_s
        nonlocal tip_count_m
        if mode == 'single':
            if tip_count_s == tip_max_s:
                robot.pause('Refill tiprack in slot 4 before resuming.')
                tip_count_s = 0
            pipette.pick_up_tip(tip_locs_s[tip_count_s])
            tip_count_s += 1
        else:
            if tip_count_m == tip_max_m:
                robot.pause('Refill tiprack in slots 1, 4, 8, 9, and 11 before \
resuming.')
                tip_count_m = 0
            pipette.pick_up_tip(tip_locs_m[tip_count_m])
            tip_count_m += 1

    def hb_distribute(vol, src, cols):
        m50.transfer(
            vol,
            src,
            [well for col in cols for well in magplate.columns(col)],
            new_tip='never',
            blow_out=True
        )

    def remove_supernatant(vol, waste_chan):
        for set in rep_sets_m:
            if not m300.tip_attached:
                pick_up(m300, 'multi')
            m300.consolidate(
                vol, [s.bottom(0.5) for s in set], waste_chan, new_tip='never')
            m300.drop_tip()

    # parse HB file
    hb_all = {h: {} for h in hb}
    hb_input_data = [
        line.split(',')[1:13]
        for line in HB_CSV.splitlines()[1:5]
    ]
    for key, line in zip(hb_all, hb_input_data):
        for i, vol in enumerate(line):
            if vol and vol.strip() != '0':
                if vol not in hb_all[key]:
                    hb_all[key][vol] = []
                hb_all[key][vol].append(str(i+1))

    # HB distributions
    pick_up(m50, 'single')
    m50.aspirate(0, temp_plate.wells(0).top(5))
    for i, source in enumerate(hb_all):
        if not m50.tip_attached:
            pick_up(m50, 'single')
        for vol in hb_all[source]:
            hb_distribute(float(vol), source, hb_all[source][vol])
        if i != 0:
            m50.drop_tip()

    robot.comment('Delaying 1 minute.')
    m50.delay(minutes=1)

    # bead distribution
    for col in magplate.columns()[:8]:
        pick_up(m50, 'single')
        for well in col:
            m50.transfer(5, beads, well.top(-2), new_tip='never')
            m50.blow_out()
        m50.drop_tip()

    robot.pause('Fill tiprack in slot 4.')
    tipracks_multi.insert(0, tiprack_single)
    tip_max_m = len(tipracks_multi)*12
    tip_locs_m = [tip for rack in tipracks_multi for tip in rack.rows('A')]

    # mix wells
    tip_locs = []
    for mix_set, mag_set in zip(mix_sets_m, rep_sets_m):
        if len(mix_sets_m) > tip_max_m - tip_count_m:
            robot.pause('Refill tiprack in slots 4, 6, 8, 9, and 11 before \
resuming.')
            tip_count_m = 0
        pick_up(m300, 'multi')
        tip_locs.append(m300.current_tip())
        for mix_loc, mag_samp in zip(mix_set, mag_set):
            m300.mix(10, 100, mix_loc)
            m300.blow_out(mag_samp.top(-2))
        m300.return_tip()

    # 60 minute pause with 3x iterative mixing every 20 minutes
    for pause in range(3):
        if pause > 0:
            for t, mix_set, mag_set in zip(tip_locs_s, mix_sets_m, rep_sets_m):
                m300.pick_up_tip(t)
                for mix_loc, mag_samp in zip(mix_set, mag_set):
                    m300.mix(10, 100, mix_loc)
                    m300.blow_out(mag_samp.top(-2))
                if pause == 2:
                    m300.drop_tip()
                else:
                    m300.return_tip()
        robot.comment('Delaying 20 minutes (part ' + str(pause+1) + '/3 of \
60-minute pause).')
        m300.delay(minutes=20)

    magdeck.engage(height=18)
    robot.comment('Incubating on magnet for 1 minute.')
    m300.delay(minutes=1)

    remove_supernatant(40, waste[0])

    # 2x PBS-T washes
    for wash in range(1, 3):
        pick_up(m300, 'multi')
        m300.distribute(
            150,
            pbs_t,
            [m.top() for m in mag_samples_m],
            new_tip='never',
            disposal_vol=0
        )

        magdeck.disengage()
        for _ in range(3):
            m300.delay(seconds=10)
            robot._driver.run_flag.wait()
            magdeck.engage(height=18)
            m300.delay(seconds=10)
            robot._driver.run_flag.wait()
            magdeck.disengage()

        magdeck.engage(height=18)
        robot.comment('Incubating on magnet for 1 minute.')
        m300.delay(minutes=1)
        if wash == 2:
            robot._driver.run_flag.wait()
            robot.pause('Add the reducing agent to the master mix.')

        remove_supernatant(150, waste[wash])

    # distribute reaction buffer master mix
    pick_up(m300, 'multi')
    m300.distribute(
        50,
        rxn_mm,
        [m.top() for m in mag_samples_m],
        new_tip='never',
        disposal_vol=0
    )

    magdeck.disengage()

    # mix wells
    tip_locs = []
    for mix_set, mag_set in zip(mix_sets_m, rep_sets_m):
        if len(mix_sets_m) > tip_max_m - tip_count_m:
            robot.pause('Refill tiprack in slots 4, 6, 8, 9, and 11 before \
resuming.')
            tip_count_m = 0
        if not m300.tip_attached:
            pick_up(m300, 'multi')
        tip_locs.append(m300.current_tip())
        for mix_loc, mag_samp in zip(mix_set, mag_set):
            m300.mix(10, 100, mix_loc)
            m300.blow_out(mag_samp.top(-2))
        m300.return_tip()

    robot.pause('Move the plate onto the temperature module.')

    # 60 minute pause with 3x iterative mixing every 20 minutes
    for pause in range(3):
        if pause > 0:
            for t, mix_set, mag_set in zip(tip_locs_s, mix_sets_t, rep_sets_t):
                m300.pick_up_tip(t)
                for mix_loc, mag_samp in zip(mix_set, mag_set):
                    m300.mix(10, 100, mix_loc)
                    m300.blow_out(mag_samp.top(-2))
                if pause == 2:
                    m300.drop_tip()
                else:
                    m300.return_tip()
        robot.comment('Delaying 20 minutes (part ' + str(pause+1) + '/3 of \
60-minute pause).')
        m300.delay(minutes=20)

    m300.home()
    robot.pause('Move the plate onto the magnetic module.')

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    robot.comment('Incubating on magnet for 1 minute.')
    m300.delay(minutes=1)

    remove_supernatant(50, waste[3])

    # 2x wash buffer washes
    for wash in range(4, 6):
        pick_up(m300, 'multi')
        m300.distribute(
            150,
            wash_buff,
            [m.top() for m in mag_samples_m],
            disposal_vol=0,
            new_tip='never'
        )
        magdeck.disengage()
        for rep in range(2):
            for _ in range(3):
                m300.delay(seconds=10)
                robot._driver.run_flag.wait()
                magdeck.engage(height=18)
                m300.delay(seconds=10)
                robot._driver.run_flag.wait()
                magdeck.disengage()

            robot.comment('Incubating 5 minutes.')
            m300.delay(minutes=5)

        magdeck.engage(height=18)
        robot.comment('Incubating 1 minute.')
        m300.delay(minutes=1)

        remove_supernatant(150, waste[wash])

    # PBS-T
    pick_up(m300, 'multi')
    m300.distribute(
        150,
        pbs_t,
        [m.top() for m in mag_samples_m],
        disposal_vol=0,
        new_tip='never'
    )

    magdeck.disengage()
    for _ in range(3):
        m300.delay(seconds=10)
        robot._driver.run_flag.wait()
        magdeck.engage(height=18)
        m300.delay(seconds=10)
        robot._driver.run_flag.wait()
        magdeck.disengage()

    magdeck.engage(height=18)
    robot.comment('Incubating 1 minute.')
    m300.delay(minutes=1)

    remove_supernatant(150, waste[6])

    # HRP
    pick_up(m300, 'multi')
    m300.distribute(
        100,
        hrp,
        [m.top() for m in mag_samples_m],
        disposal_vol=0,
        new_tip='never'
    )
    magdeck.disengage()
    for rep in range(2):
        for _ in range(3):
            m300.delay(seconds=10)
            robot._driver.run_flag.wait()
            magdeck.engage(height=18)
            m300.delay(seconds=10)
            robot._driver.run_flag.wait()
            magdeck.disengage()

        robot.comment('Incubating 5 minutes.')
        m300.delay(minutes=5)

    magdeck.engage(height=18)
    robot.comment('Incubating 1 minute.')
    m300.delay(minutes=1)

    remove_supernatant(150, waste[wash])

    robot.pause('Empty liquid waste in reservoir channels 4-12 before \
resuming.')

    # 3x PBS-T washes
    for wash in range(3):
        pick_up(m300, 'multi')
        m300.distribute(
            150,
            pbs_t,
            [m.top() for m in mag_samples_m],
            new_tip='never',
            disposal_vol=0
        )

        magdeck.disengage()
        for _ in range(3):
            m300.delay(seconds=10)
            robot._driver.run_flag.wait()
            magdeck.engage(height=18)
            m300.delay(seconds=10)
            robot._driver.run_flag.wait()
            magdeck.disengage()

        magdeck.engage(height=18)
        robot.comment('Incubating on magnet for 1 minute.')
        m300.delay(minutes=1)

        if wash < 2:
            remove_supernatant(150, waste[wash])
        else:
            robot._driver.run_flag.wait()
            robot.pause('Prepare the substrate and load it into the 12-channel \
reservoir in channel 3.')
            for i, m in enumerate(mag_samples_m):
                if not m300.tip_attached:
                    pick_up(m300, 'multi')
                m300.transfer(160, m.bottom(0.5), waste[2], new_tip='never')
                m300.drop_tip()
                pick_up(m300, 'multi')
                m300.transfer(100, substrate, m, new_tip='never')
                m300.drop_tip()
                if i < len(mag_samples_m) - 1:
                    robot.pause('Waiting for measurement...')
                else:
                    robot.comment('Take final measurement. Protocol finished.')
