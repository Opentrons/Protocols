from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Cell Culture Dilution',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
tips300_name = 'TipOne_96_tiprack_300ul'
if tips300_name not in labware.list():
    labware.create(
        tips300_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60
    )

# load labware
reagent_tuberack = labware.load(
    'opentrons_15_tuberack_falcon_15ml_conical', '2', 'reagent tuberack')
tips50 = labware.load(tips300_name, '4', 'P50 tiprack')
tips300 = labware.load(tips300_name, '5', 'P300 tiprack')

# reagents
gm = reagent_tuberack.wells('A1')
water = reagent_tuberack.wells('A2')


def run_custom_protocol(
        p50_single_mount: StringSelection('right', 'left') = 'right',
        p300_single_mount: StringSelection('left', 'right') = 'left',
        stock_plate_type: StringSelection(
            'deepwell', 'flat well') = 'deepwell',
        drug_rows_separated_by_commas: str = 'A, B, C, D, E, F, G, H',
        number_of_test_plates: int = 6,
        number_of_replicates_per_source: int = 1
):
    # check
    if p50_single_mount == p300_single_mount:
        raise Exception('Pipette mounts cannot be the same.')
    if number_of_test_plates > 7:
        raise Exception('Cannot accommodate more than 7 test plates.')

    drug_rows = [
        row.strip() for row in drug_rows_separated_by_commas.split(',')]
    for row in drug_rows:
        if row.upper() not in 'ABCDEFGH':
            raise Exception('Invalid drug row (' + row + ').')
    if len(drug_rows)*number_of_replicates_per_source > 8:
        raise Exception('Cannot accommodate this many replicates per source.')

    # plates
    if stock_plate_type == 'deepwell':
        stock_plate = labware.load(
            'usascientific_96_wellplate_2.4ml_deep', '1', 'stock plate')
    else:
        stock_plate = labware.load(
            'corning_96_wellplate_360ul_flat', '1', 'stock plate')
    test_plates = [
        labware.load(
            'corning_96_wellplate_360ul_flat',
            str(slot),
            'test plate ' + str(i)
        )
        for i, slot in enumerate(
            ['3', '6', '7', '8', '9', '10', '11'][:number_of_test_plates])
    ]

    # pipettes
    p50 = instruments.P50_Single(mount=p50_single_mount, tip_racks=[tips50])
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=[tips300])

    tubes = {
        'growth medium': [gm, 100, 14000],
        'water': [water, 100, 14000]
    }
    r15 = 14.90/2
    min_h = 10

    def h_track(vol, tube):
        nonlocal tubes
        # calculate aspiration height
        tubes[tube][2] -= vol
        if tubes[tube][2] < 1000:
            robot.pause(
                'Fill liquid in ' + tube + ' tube (rack well '
                + tubes[tube][0].get_name() + ') before resuming.'
            )
            tubes[tube][1] = 100
            tubes[tube][2] = 14000
        dh = vol/((r15**2)*math.pi)
        new_h = tubes[tube][1] - dh if tubes[tube][1] - dh > min_h else min_h
        tubes[tube][1] = new_h
        return new_h

    # distribute replicates
    for i, drug_row in enumerate(drug_rows):
        source_wells = stock_plate.rows(drug_row)[10::-1]
        dest_sets = [
            [well
             for plate in test_plates
             for well in plate.columns()[col][
                i*number_of_replicates_per_source:
                (i+1)*number_of_replicates_per_source]
             ]
            for col in [11] + [num for num in range(9, -1, -1)]
        ]
        p50.pick_up_tip()
        for s, d in zip(source_wells, dest_sets):
            p50.distribute(
                20,
                s,
                [well.bottom(1) for well in d],
                new_tip='never',
                disposal_vol=0
            )
        p50.drop_tip()

    # distribute water to control wells with height tracking
    water_dests = [
        well for plate in test_plates for well in plate.columns()[10]]
    num_aspirations_w = math.ceil(len(water_dests)/2)
    p50.pick_up_tip()
    for i in range(num_aspirations_w):
        dests = [well.bottom(1) for well in water_dests[i*2:i*2+2]]
        asp_h = h_track(40, 'water')
        p50.distribute(40, water.bottom(asp_h), dests, new_tip='never')
        p50.blow_out()
    p50.drop_tip()

    # distibute growth medium to all wells of all plates
    all_dests = [well for plate in test_plates for well in plate.wells()]
    num_aspirations_gm = math.ceil(len(all_dests)/6)
    p300.pick_up_tip()
    for i in range(num_aspirations_gm):
        if i*6+6 < len(all_dests):
            dests = all_dests[i*6:i*6+6]
            asp_vol = 300
        else:
            dests = all_dests[i*6:]
            asp_vol = len(all_dests[i*6:])*50

        asp_h = h_track(asp_vol, 'growth medium')
        p300.aspirate(asp_vol, gm.bottom(asp_h))
        for d in dests:
            p300.dispense(50, d.top(-1))
            p300.move_to((d, d.from_center(r=1, h=0.9, theta=0)))
            p300.move_to((d, d.from_center(r=1, h=0.9, theta=math.pi)))
        p300.blow_out(gm.top())
