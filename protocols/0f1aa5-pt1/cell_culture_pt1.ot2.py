from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Cell Culture Assay: Part 1',
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
    'usascientific_96_wellplate_2.4ml_deep', '1', 'plate A')
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
vial_rack = labware.load(vial_rack_name, '5', 'compound vial rack')
tips10 = [
    labware.load(tiprack10_name, slot) for slot in ['7', '8']]
tips300 = [
    labware.load(tiprack300_name, slot) for slot in ['10', '11']]

# reagents
l_tube = micro_tuberack.wells('A1')
d = micro_tuberack.wells('B1')
dm = micro_tuberack.wells('C1')


def run_custom_protocol(
        p10_mount: StringSelection('right', 'left') = 'right',
        p300_mount: StringSelection('left', 'right') = 'left',
):
    # check
    if p10_mount == p300_mount:
        raise Exception('Input different mounts for P10 and P300 pipettes.')

    # pipettes
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=tips10)
    p300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)

    r15 = 14.9/2
    r50 = 27.81/2
    max_d15 = -117.5 + 5
    max_d50 = -113 + 5
    tubes = {
        'media': [falcon_tuberack.wells('A3'), '50', -25]}

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

    # transfer media
    media_wells1 = [
        well for well in plate_A.wells('E1', length=24)]
    p300.pick_up_tip()
    for m in media_wells1:
        for v in [300, 300, 300, 90]:
            h_trans(v, 'media', m)
    p300.drop_tip()

    # transfer compounds
    compound_vials = [well for well in vial_rack.wells()]
    for compound, m in zip(compound_vials, media_wells1):
        p10.pick_up_tip()
        p10.transfer(10, compound, m, new_tip='never')
        p10.blow_out(m)
        p10.drop_tip()

    # transfer media to next set of destinations
    media_wells2 = [
        well for well in plate_A.wells('E5', length=24)]
    p300.pick_up_tip()
    for m in media_wells2:
        for v in [300, 300, 192]:
            h_trans(v, 'media', m)
    p300.drop_tip()

    # corresponding well-to-well transfer
    for s, d in zip(media_wells1, media_wells2):
        p10.pick_up_tip()
        p10.transfer(8, s, d, new_tip='never')
        p10.blow_out(d)
        p10.drop_tip()

    p300.pick_up_tip()
    for v in [300, 300, 200]:
        h_trans(v, 'media', plate_A.wells('A5'))
    for v in [300, 300, 184]:
        h_trans(v, 'media', plate_A.wells('B5'))
    p300.drop_tip()

    p10.pick_up_tip()
    for v in [10, 6]:
        p10.transfer(v, l_tube, plate_A.wells('B5').top(), new_tip='never')
    p10.mix(10, 9, plate_A.wells('B5'))
    p10.blow_out()
    p10.drop_tip()

    p300.pick_up_tip()
    for v in [300, 300, 192]:
        h_trans(v, 'media', plate_A.wells('C5'))
    p300.drop_tip()

    p10.pick_up_tip()
    p10.transfer(8, d, plate_A.wells('C5'), new_tip='never')
    p10.mix(10, 9, plate_A.wells('C5'))
    p10.blow_out()
    p10.drop_tip()

    p300.pick_up_tip()
    for v in [300, 300, 192]:
        h_trans(v, 'media', plate_A.wells('D5'))
    p300.drop_tip()

    p10.pick_up_tip()
    p10.transfer(8, dm, plate_A.wells('D5'), new_tip='never')
    p10.mix(10, 9, plate_A.wells('D5'))
    p10.blow_out()
    p10.drop_tip()
