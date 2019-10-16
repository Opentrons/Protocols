from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Cytotoxicity Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
tuberack50 = labware.load(
    'opentrons_6_tuberack_falcon_50ml_conical', '1', '50ml tuberack')
plate = labware.load('corning_96_wellplate_360ul_flat', '2', 'assay plate')
tips300 = labware.load('opentrons_96_tiprack_300ul', '4', '300ul tiprack')

# setup tube dictionary
tubes = {
    'A': [tuberack50.wells('A1'), 70],
    'B': [tuberack50.wells('B1'), 70],
    'C': [tuberack50.wells('A2'), 70],
    'D': [tuberack50.wells('B2'), 70]
}
waste = tuberack50.wells('A3').top()


def run_custom_protocol(
        p300_single_mount: StringSelection('right', 'left') = 'right'
):

    # pipette
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=[tips300])

    # height track
    r = 27.81/2

    def h_asp(vol, tube):
        dh = vol/(math.pi*(r**2))*1.05
        if tubes[tube][1] - dh < 5:
            tubes[tube][1] = 5
        else:
            tubes[tube][1] -= dh
        h = tubes[tube][1]
        p300.aspirate(vol, tubes[tube][0].bottom(h))

    def tube_trans(vol, source, dests, drop_tip=True):
        num_dist = math.ceil(len(dests)/3)
        if not p300.tip_attached:
            p300.pick_up_tip()
        for _ in range(num_dist):
            num_dests = len(dests) if len(dests) < 3 else 3
            asp_vol = 100 * num_dests
            h_asp(asp_vol, source)
            dest_set = dests[:num_dests]
            for d in dest_set:
                p300.dispense(100, d.top())
                dests.pop(0)
            p300.blow_out(tubes[source][0].top())
        if drop_tip:
            p300.drop_tip()

    # transfer media
    media_dests = [
        well for col in plate.columns()[:6] for well in col[1:]] + [
        well for well in plate.columns()[6][:3]
    ]
    tube_trans(100, 'A', media_dests)

    # transfer effector cells
    effector_dests1 = [well for well in plate.rows('A')[:6]] + [
        well for well in plate.columns('7')[:3]]
    tube_trans(100, 'B', effector_dests1, drop_tip=False)

    effector_dests2 = [well for well in plate.rows('A')[:6]]
    tube_trans(100, 'B', effector_dests2, drop_tip=False)

    # serially dilute 1:2
    for source_set, dest_set in zip(
            [col[0:6] for col in plate.columns()[:6]],
            [col[1:7] for col in plate.columns()[:6]]):

        for s, d in zip(source_set, dest_set):
            p300.transfer(100, s, d, new_tip='never')
            p300.mix(3, 50, d)
            p300.blow_out(d.top())
        p300.transfer(100, dest_set[-1], waste, new_tip='never')
        p300.blow_out()
    p300.drop_tip()

    # transfer control target cells
    control_dests = [well for col in plate.columns()[:3] for well in col]
    tube_trans(100, 'C', control_dests)

    # transfer target cells
    target_dests = [well for col in plate.columns()[3:6] for well in col]
    tube_trans(100, 'D', target_dests)
