from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell Culture Assay: Part 4',
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
    'corning_96_wellplate_360ul_flat', '1', 'plate B')
plate_C = labware.load(
    'corning_96_wellplate_360ul_flat', '2', 'plate C')
plate_D = labware.load(
    'corning_96_wellplate_360ul_flat', '3', 'plate D')
plate_E = labware.load(
    'corning_96_wellplate_360ul_flat', '4', 'plate E')

res12 = labware.load('usascientific_12_reservoir_22ml', '5')
tips300m = [
    labware.load(tiprack300_name, slot) for slot in ['6', '7', '8', '9']]
tips300s = [
    labware.load(tiprack300_name, slot) for slot in ['10', '11']]

# reagents
ctg = res12.wells('A1')
pbs = res12.wells('A2', length=2)
waste = res12.wells('A12').top()


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        p300_single_mount: StringSelection('left', 'right') = 'left',
):

    # pipettes
    p300 = instruments.P300_Single(mount=p300_single_mount, tip_racks=tips300s)
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300m)

    tip300s_count = 0
    tip300m_count = 0
    tip300s_max = len(tips300s)*96
    tip300m_max = len(tips300m)*12

    def pick_up(pip):
        nonlocal tip300s_count
        nonlocal tip300m_count

        if pip == p300:
            if tip300s_count == tip300s_max:
                robot.pause('Refill P300 single tip racks before resuming.')
                tip300m_count = 0
                p300.reset()
            tip300s_count += 1
        else:
            if tip300m_count == tip300m_max:
                robot.pause('Refill P300 multi tip racks before resuming.')
                tip300m_count = 0
                m300.reset()
            tip300m_count += 1
        pip.pick_up_tip()

    # transfer supernatant from plate B to corresponding columns of plates C, D
    sources = [well.bottom(0.5) for well in plate_B.rows('A')]
    dests = plate_C.rows('A')[3:] + plate_D.rows('A')[3:] + \
        plate_E.rows('A')[3:]
    for s, d in zip(sources, dests[:12]):
        pick_up(m300)
        m300.transfer(50, s, d, new_tip='never')
        m300.blow_out()
        m300.drop_tip()

    # transfer again
    for s, d in zip(dests[:12], dests[12:24]):
        pick_up(m300)
        m300.transfer(100, s, d, new_tip='never')
        m300.blow_out()
        m300.drop_tip()

    # remove supernatant from plate B
    for well in plate_B.rows('A'):
        pick_up(m300)
        m300.transfer(300, well.bottom(0.5), waste, new_tip='never')
        m300.drop_tip()

    # PBS wash
    pick_up(m300)
    m300.distribute(
        100, pbs, [well.top() for well in plate_B.rows('A')], new_tip='never')
    for well in plate_B.rows('A'):
        if not m300.tip_attached:
            pick_up(m300)
        m300.transfer(120, well.bottom(0.5), waste, new_tip='never')
        m300.drop_tip()

    # distribute CTG
    pick_up(m300)
    m300.distribute(
        200, ctg, [well.top() for well in plate_B.rows('A')], new_tip='never')
    m300.drop_tip()
