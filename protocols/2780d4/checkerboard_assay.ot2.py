from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Checkerboard Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}


def run_custom_protocol(
        p50_mount: StringSelection('right', 'left') = 'right',
        p300_mount: StringSelection('left', 'right') = 'left',
        number_of_checkerboard_plates: int = 6
):

    # check
    if p50_mount == p300_mount:
        raise Exception('Pipette mounts cannot match.')
    if number_of_checkerboard_plates < 1 or number_of_checkerboard_plates > 8:
        raise Exception('Invalid number of checkerboard plates.')

    # pipettes
    p50 = instruments.P50_Single(mount=p50_mount)
    p300 = instruments.P300_Single(mount=p300_mount)

    # load labware
    cb_plates = [
        labware.load(
            'corning_96_wellplate_360ul_flat',
            str(slot+1),
            'checkerboard plate ' + str(slot+1)
        )
        for slot in range(number_of_checkerboard_plates)
    ]
    stock_plate = labware.load(
        'usascientific_96_wellplate_2.4ml_deep', '9', 'stock plate')
    tipracks = [
        labware.load('opentrons_96_tiprack_300ul', '10')]
    tuberack = labware.load(
        'opentrons_6_tuberack_falcon_50ml_conical', '11', 'reagent tuberack')

    # reagent setup
    tubes = {
        'water': [tuberack.wells('A1'), 70],
        'growth medium': [tuberack.wells('B1'), 70]
    }

    # share tips function
    all_tips = [tip for rack in tipracks for tip in rack.wells()]
    tip_counter = 0

    def pick_up(pip):
        nonlocal tip_counter
        if tip_counter == len(tipracks)*96:
            robot.pause('Replace tipracks before resuming.')
            tip_counter = 0
        pip.pick_up_tip(all_tips[tip_counter])
        tip_counter += 1
        return(tip_counter)

    # tube height tracking
    min_depth = 5
    r = tuberack.wells(0).properties['diameter']/2

    def h_asp(pip, vol, source):
        dh = vol/(math.pi*(r**2))*1.1
        if tubes[source][1] - dh < min_depth:
            tubes[source][1] = min_depth
        else:
            tubes[source][1] -= dh
        pip.aspirate(vol, tubes[source][0].bottom(tubes[source][1]))

    # transfer drug A from stock plate to checkerboard plates
    sources_A = [well for well in stock_plate.columns('1')[6::-1]]
    dests_A = [
        [well for plate in cb_plates for well in plate.rows(row)[:8]]
        for row in 'GFEDCBA'
    ]
    pick_up(p50)
    for s, d in zip(sources_A, dests_A):
        p50.distribute(
            20,
            s,
            [well.bottom(0.5) for well in d],
            new_tip='never',
            blow_out=True
        )
    p50.drop_tip()

    # transfer water to drug B alone control wells
    water_dests_A = [
        well for plate in cb_plates for well in plate.rows('H')[:8]]
    water_sets_A = [water_dests_A[i:i+2] for i in range(len(water_dests_A)//2)]
    pick_up(p50)
    for set in water_sets_A:
        h_asp(p50, 45, 'water')
        for well in set:
            p50.dispense(20, well.bottom(0.5))
        p50.blow_out(tubes['water'][0].top())
    p50.drop_tip()

    # transfer drug B from stock plate to checkerboard plates
    sources_B = [well for well in stock_plate.columns('2')[6::-1]]
    dests_B = [
        [well for plate in cb_plates for well in plate.columns()[col]]
        for col in range(6, -1, -1)
    ]
    pick_up(p50)
    for s, d in zip(sources_B, dests_B):
        sets = [d[i:i+2] for i in range(len(d)//2)]
        for set in sets:
            p50.aspirate(45, s)
            for well in set:
                p50.dispense(20, well.bottom(4))
                p50.touch_tip(well)
            p50.blow_out(s.top())
    p50.drop_tip()

    # transfer water to negative control wells
    water_dests_ct = [
        well for plate in cb_plates for well in plate.columns('9')]
    num_asp_water = math.ceil(len(water_dests_ct)/7)
    pick_up(p300)
    for _ in range(num_asp_water):
        if len(water_dests_ct) >= 7:
            h_asp(p300, 300, 'water')
            length = 7
        else:
            h_asp(p300, len(water_dests_ct)*40+30, 'water')
            length = len(water_dests_ct)
        for _ in range(length):
            p300.dispense(40, water_dests_ct.pop(0).bottom(0.5))
        p300.blow_out(tubes['water'][0].top())
    p300.drop_tip()

    # transfer growth medium to all wells
    all_dests = [
        well
        for plate in cb_plates
        for row in plate.rows()
        for well in row[:9]
    ]
    num_asp_gm = math.ceil(len(all_dests)/5)
    pick_up(p300)
    for _ in range(num_asp_gm):
        if len(all_dests) >= 5:
            h_asp(p300, 280, 'growth medium')
            length = 5
        else:
            h_asp(p300, len(all_dests)*50+30, 'growth medium')
            length = len(all_dests)
        for _ in range(length):
            dest = all_dests.pop(0)
            p300.dispense(50, dest.bottom(7))
            p300.touch_tip(dest)
        p300.blow_out(tubes['growth medium'][0].top())
    p300.drop_tip()
