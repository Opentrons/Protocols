from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Cell Culture Assay: Part 3',
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
plate_B = labware.load(
    'corning_96_wellplate_360ul_flat', '2', 'plate B')
falcon_tuberack = labware.load(
    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical',
    '3',
    'Falcon tuberack'
)
tips10 = labware.load(tiprack10_name, '7')


def run_custom_protocol(
        p10_mount: StringSelection('right', 'left') = 'right',
        p300_mount: StringSelection('left', 'right') = 'left'
):
    # check
    if p10_mount == p300_mount:
        raise Exception('Input different mounts for P10 and P300 pipettes.')

    # pipettes
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=[tips10])
    p300 = instruments.P300_Single(mount=p300_mount)

    r15 = 14.9/2
    r50 = 27.81/2
    max_d15 = -117.5 + 5
    max_d50 = -113 + 5
    tubes = {
        'media': [falcon_tuberack.wells('A3'), '50', -25],
        'LP': [falcon_tuberack.wells('A1'), '15', -25]
    }

    def h_trans(vol, tube, dest):
        nonlocal tubes

        pip = p10 if vol < 30 else p300

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

        pip.transfer(
            vol, tubes[tube][0].top(h), dest.top(), new_tip='never')
        pip.blow_out()

    p10.pick_up_tip()
    for dest in plate_B.wells():
        h_trans(10, 'LP', dest)
    p10.drop_tip()
