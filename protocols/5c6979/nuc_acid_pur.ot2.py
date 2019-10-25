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


def run_custom_protocol(
        p50_multi_mount: StringSelection('right', 'left') = 'right',
        p300_multi_mount: StringSelection('left', 'right') = 'left',
        input_CSV: FileInput = example_csv
):
    # check
    if p50_multi_mount == p300_multi_mount:
        raise Exception('Pipette mount selections must be distinct.')

    # pipettes
    m50 = instruments.P50_Multi(mount=p50_multi_mount)
    m300 = instruments.P300_Multi(mount=p300_multi_mount)

    # parse
    rep_sets = [
        [magplate.rows('A')[int(col)-1] for col in line.split(',')]
        for line in input_CSV.splitlines() if line
    ]
    # samples
    mag_samples_m = [col for set in rep_sets for col in set]
    mix_sets = []
    for line in input_CSV.splitlines()[1:]:
        if line:
            set = []
            for col in line.split(','):
                col_ind = int(col) - 1
                angle = 0 if col_ind % 2 == 0 else math.pi
                mix_well = magplate.rows('A')[col_ind]
                set.append(
                    (
                     mix_well,
                     mix_well.from_center(r=0.9, h=-0.7, theta=angle)
                    )
                )
            mix_sets.append(set)

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
        m50.distribute(
            vol,
            src,
            [well for col in cols for well in magplate.columns(col)],
            disposal_vol=0,
            new_tip='never',
            blow_out=True
        )

    def remove_supernatant(vol, waste_chan):
        for set in rep_sets:
            if not m300.tip_attached:
                pick_up(m300, 'multi')
            m300.consolidate(
                vol, [s.bottom(0.5) for s in set], waste_chan, new_tip='never')
            m300.drop_tip()

    # HB distributions
    pick_up(m50, 'single')
    m50.aspirate(0, temp_plate.wells(0).top(5))
    # HB
    hb_distribute(10, hb[0], ['2', '5'])
    hb_distribute(20, hb[0], ['8'])
    hb_distribute(15, hb[0], ['3', '6'])

    # HB1
    hb_distribute(20, hb[1], ['1'])
    hb_distribute(10, hb[1], ['2'])
    hb_distribute(5, hb[1], ['3'])
    m50.drop_tip()

    # HB2
    pick_up(m50, 'single')
    hb_distribute(20, hb[2], ['4'])
    hb_distribute(10, hb[2], ['5'])
    hb_distribute(5, hb[2], ['6'])
    m50.drop_tip()

    # HB3
    pick_up(m50, 'single')
    hb_distribute(20, hb[3], ['7'])
    m50.drop_tip()

    robot.comment('Delaying 1 minute.')
    m50.delay(minutes=1)

    # bead distribution
    for col in magplate.columns()[:8]:
        pick_up(m50, 'single')
        m50.distribute(
            5, beads, [well.top(-2) for well in col], new_tip='never')
        m50.drop_tip()

    robot.pause('Fill tiprack in slot 4.')
    tipracks_multi.insert(0, tiprack_single)
    tip_max_m = len(tipracks_multi)*12
    tip_locs_m = [tip for rack in tipracks_multi for tip in rack.rows('A')]

    # mix wells
    tip_locs = []
    for mix_set, mag_set in zip(mix_sets, rep_sets):
        if len(mix_sets) > tip_max_m - tip_count_m:
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
    for pause in range(4):
        for t, mix_set, mag_set in zip(tip_locs_s, mix_sets, rep_sets):
            m300.pick_up_tip(t)
            for mix_loc, mag_samp in zip(mix_set, mag_set):
                m300.mix(10, 100, mix_loc)
                m300.blow_out(mag_samp.top(-2))
            if pause == 2:
                m300.drop_tip()
            else:
                m300.return_tip()
        if pause < 3:
            robot.comment('Delaying 20 minutes (part ' + str(pause) + '/3 of \
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
        for mix_set, mag_set in zip(mix_sets, rep_sets):
            if not m300.tip_attached:
                pick_up(m300, 'multi')
            for mix_loc, mag_samp in zip(mix_set, mag_set):
                m300.mix(3, 100, mix_loc)
                m300.blow_out(mag_samp.top(-2))
            m300.drop_tip()

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

    # mix
    for mix_set, mag_set in zip(mix_sets, rep_sets):
        if not m300.tip_attached:
            pick_up(m300, 'multi')
        for mix_loc, mag_samp in zip(mix_set, mag_set):
            m300.mix(3, 100, mix_loc)
            m300.blow_out(mag_samp.top(-2))
        m300.drop_tip()
    tempdeck.wait_for_temp()
    robot._driver.run_flag.wait()
    robot.pause('Move the plate onto the temperature module. Incubate for 1 \
hour, and then replace on the magnetic module before resuming.')

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

        if len(mag_samples_m) > tip_max_m - tip_count_m:
            robot.pause('Refill tiprack in slots 4, 6, 8, 9, and 11 before \
resuming.')
            tip_count_m = 0

        tip_locs = []
        for rep in range(2):
            for t, (mix_set, mag_set) in enumerate(zip(mix_sets, rep_sets)):
                if rep == 0:
                    if not m300.tip_attached:
                        pick_up(m300, 'multi')
                    tip_locs.append(m300.current_tip())
                else:
                    if not m300.tip_attached:
                        m300.pick_up_tip(tip_locs[t])
                for mix_loc, mag_samp in zip(mix_set, mag_set):
                    m300.mix(3, 100, mix_loc)
                    m300.blow_out(mag_samp.top())
                if rep == 1:
                    m300.drop_tip()
                else:
                    m300.return_tip()
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

    for mix_set, mag_set in zip(mix_sets, rep_sets):
        if not m300.tip_attached:
            pick_up(m300, 'multi')
        for mix_loc, mag_samp in zip(mix_set, mag_set):
            m300.mix(3, 100, mix_loc)
            m300.blow_out(mag_samp.top(-2))
        m300.drop_tip()

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
    tip_locs = []
    for pause in range(2):
        for t, (mix_set, mag_set) in enumerate(zip(mix_sets, rep_sets)):
            if pause == 0:
                if len(mix_sets) > tip_max_m - tip_count_m:
                    robot.pause('Refill tiprack in slots 4, 6, 8, 9, and 11 \
before resuming.')
                    tip_count_m = 0
                if not m300.tip_attached:
                    pick_up(m300, 'multi')
                tip_locs.append(m300.current_tip())
            else:
                m300.pick_up_tip(tip_locs[t])
            for mix_loc, mag_samp in zip(mix_set, mag_set):
                m300.mix(10, 100, mix_loc)
                m300.blow_out(mag_samp.top(-2))
            if pause == 0:
                m300.return_tip()
            else:
                m300.drop_tip()

        m300.delay(minutes=5)

    robot._driver.run_flag.wait()
    robot.comment('Incubating on magnet 1 minute.')
    magdeck.engage(height=18)
    m300.delay(minutes=1)

    remove_supernatant(100, waste[7])
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
        for mix_set, mag_set in zip(mix_sets, rep_sets):
            if not m300.tip_attached:
                pick_up(m300, 'multi')
            for mix_loc, mag_samp in zip(mix_set, mag_set):
                m300.mix(3, 100, mix_loc)
                m300.blow_out(mag_samp.top(-2))
            m300.drop_tip()

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
