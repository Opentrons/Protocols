from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Synthesis of Hybrid Perovskite Nanocrystals',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
tiprack = labware.load('opentrons_96_tiprack_300ul', '1')
plate = labware.load('corning_96_wellplate_360ul_flat', '2', 'end plate')
tuberack = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '5',
    'reagent tuberack'
)

# reagents
cspbi3 = tuberack.wells('A1')
mapbbr3 = tuberack.wells('A2')
fapbi3 = tuberack.wells('A3')
chloroform = tuberack.rows('B')[:5]


def run_custom_protocol(
        p300_mount: StringSelection('right', 'left') = 'right',
        p50_mount: StringSelection('left', 'right') = 'left'
):
    # check
    if p300_mount == p50_mount:
        raise Exception('Input different mounts for P300 and P50 pipettes.')

    # pipettes
    p300 = instruments.P300_Single(mount=p300_mount)
    p50 = instruments.P50_Single(mount=p50_mount)
    tip_count = 0

    dest_sets = [
        [plate.wells(spot*7+i) for spot in range(i+1)] for i in range(5)] \
        + [[plate.wells(spot*7+i*8+12) for spot in range(4-i)]
            for i in range(4)]

    # transfer MAPBBR3
    p300.pick_up_tip(tiprack.wells(tip_count))
    tip_count += 1
    for i, set in enumerate(dest_sets):
        vol = 50 - 5*i
        p300.distribute(vol, mapbbr3, [d.top() for d in set], new_tip='never')
    p300.drop_tip()

    # transfer FAPB13
    p50.pick_up_tip(tiprack.wells(tip_count))
    tip_count += 1
    for i in range(1, 5):
        vol = 5*i
        p50.distribute(
            vol,
            fapbi3,
            [d.top() for d in plate.rows()[i][:5]],
            new_tip='never'
        )
    p50.drop_tip()

    # transfer cspbi3
    p50.pick_up_tip(tiprack.wells(tip_count))
    tip_count += 1
    for i in range(1, 5):
        vol = 5*i
        p50.distribute(
            vol,
            cspbi3,
            [d.top() for d in plate.columns()[i][:5]],
            new_tip='never'
        )
    p50.drop_tip()

    robot.pause('Take a photo of the plate before the robot adds chloroform')

    all_dests = [well for row in plate.rows()[:5] for well in row[:5]]
    p300.pick_up_tip(tiprack.wells(tip_count))
    for i in range(5):
        if i < 4:
            set = all_dests[i*6:i*6+6]
        else:
            set = all_dests[i*6:]
        p300.transfer(
            250, chloroform[i], [d.top() for d in set], new_tip='never')
    p300.drop_tip()
