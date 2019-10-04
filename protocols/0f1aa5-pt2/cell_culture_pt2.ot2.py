from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Cell Culture Assay: Part 2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
vial_rack_name = 'fisherbrand_24_vilerack'
if vial_rack_name not in labware.list():
    labware.create(
        vial_rack_name,
        grid=(6, 4),
        spacing=(18, 18),
        diameter=8,
        depth=40,
        volume=5000
    )

tiprack300_name = 'fisherbrand_96_tiprack_300ul'
if tiprack300_name not in labware.list():
    labware.create(
        tiprack300_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3,
        depth=60
    )

tiprack10_name = 'fisherbrand_96_tiprack_10ul'
if tiprack10_name not in labware.list():
    labware.create(
        tiprack10_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3,
        depth=60
    )

# load labware
plate_A = labware.load(
    'usascientific_96_wellplate_2.4ml_deep', '1', 'deepwell plate A')
plate_B = labware.load(
    'corning_96_wellplate_360ul_flat', '2', 'plate B')
falcon_tuberack = labware.load(
    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical',
    '3',
    'Falcon tuberack'
)
micro_tuberack = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '4',
    'microfuge tubes'
)
res12 = labware.load('usascientific_12_reservoir_22ml', '6')
tips300m = [
    labware.load(tiprack300_name, slot) for slot in ['7', '8', '10']]
tips300s = [
    labware.load(tiprack300_name, slot) for slot in ['11']]

# reagents
pbs = res12.wells('A2', length=2)
liquid_trash = res12.wells('A10', length=3)


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        p300_single_mount: StringSelection('left', 'right') = 'left',
        number_of_compounds: int = 24
):
    # check
    if p300_single_mount == p300_multi_mount:
        raise Exception('Input different mounts for P10 and P300 pipettes.')
    if number_of_compounds > 24 or number_of_compounds < 1:
        raise Exception('Invalid number of cultures (must be 1-24).')

    # pipettes
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300m)
    p300 = instruments.P300_Single(mount=p300_single_mount, tip_racks=tips300s)

    r15 = 14.9/2
    r50 = 27.81/2
    max_d15 = -117.5 + 5
    max_d50 = -113 + 5
    tubes = {
        'media': [falcon_tuberack.wells('A3'), '50', -25]}

    def h_trans(vol, tube, dest):
        nonlocal tubes

        if tubes[tube][1] == '15':
            dh = vol/((r15**2)*math.pi)
            if tubes[tube][2] - dh > max_d15:
                tubes[tube][2] -= dh
            else:
                tubes[tube][2] = max_d15
            h = tubes[tube][2]
        else:
            dh = vol/((r50**2)*math.pi)
            if tubes[tube][2] - dh > max_d50:
                tubes[tube][2] -= dh
            else:
                tubes[tube][2] = max_d50
            h = tubes[tube][2]

        p300.transfer(
            vol, tubes[tube][0].top(h), dest.top(), new_tip='never')
        p300.blow_out()

    # remove media from plate B
    for well in plate_B.rows('A'):
        m300.transfer(100, well.bottom(), liquid_trash[0])

    # PBS washes
    for wash in range(2):
        m300.pick_up_tip()
        m300.distribute(
            100,
            pbs[wash],
            [well.top() for well in plate_B.rows('A')],
            new_tip='never'
        )
        for well in plate_B.rows('A'):
            if not m300.tip_attached:
                m300.pick_up_tip()
            m300.transfer(
                100,
                well.bottom(),
                liquid_trash[wash+1],
                new_tip='never'
            )
            m300.drop_tip()

    trip_sources = [well for well in plate_A.wells('A5', to='D8')]
    trip_dests = [
        [well for well in row[i*3:i*3+3]]
        for i in range(4)
        for row in plate_B.rows()
    ]

    for s, d in zip(trip_sources, trip_dests):
        p300.pick_up_tip()
        p300.mix(10, 100, s)
        p300.blow_out(s.top())
        p300.transfer(200, s, [well for well in d], new_tip='never')
        p300.drop_tip()
