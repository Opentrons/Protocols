from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Haptoglobin Assay',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create labware
tr_custom = 'opentrons_15_tuberack_customtubes'
if tr_custom not in labware.list():
    labware.create(
        tr_custom,
        grid=(5, 3),
        spacing=(25, 25),
        diameter=14.9,
        depth=100,
        volume=1300
    )

tr1 = labware.load(tr_custom, '1', 'Tube Rack 1 (13x100)')
tr2 = labware.load(tr_custom, '2', 'Tube Rack 2 (13x100)')
tr3 = labware.load(tr_custom, '3', 'Tube Rack 3 (13x100)')

tr1550 = labware.load(
    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical',
    '6', '15mL & 50mL Tube Rack')

ep1 = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '4', 'Eppendorf Tube Rack 1')

ep2 = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '5', 'Eppendorf Tube Rack 2')

fp = labware.load('corning_96_wellplate_360ul_flat', '7', '96 Well Plate')

tips50 = [labware.load(
    'opentrons_96_tiprack_300ul', str(slot)) for slot in range(8, 10)
    ]

tips1k = [labware.load('opentrons_96_tiprack_1000ul', '11')]

pbs = tr1550.wells('A3')
methemo = tr1550.wells('B3')
h2o2 = tr1550.wells('A4')


def run_custom_protocol(
        p50_mount: StringSelection('left', 'right') = 'left',
        p1000_mount: StringSelection('right', 'left') = 'right'):

    # create pipettes
    pip50 = instruments.P50_Single(mount=p50_mount, tip_racks=tips50)
    pip1k = instruments.P1000_Single(mount=p1000_mount, tip_racks=tips1k)

    dcurve = ep1.rows('A')+ep1.wells('B1', 'B2')

    pip50.transfer(8, pbs, dcurve, new_tip='always')

    for i in range(7):
        pip50.pick_up_tip()
        pip50.transfer(8, dcurve[i], dcurve[i+1], new_tip='never')
        pip50.mix(3, 20, dcurve[i+1])
        pip50.drop_tip()

    robot.pause('Standard Curve complete. When ready, click RESUME.')

    tbs = tr1.wells()+tr2.wells()+tr3.wells()+tr1550.wells('A1', 'B1', 'C1')

    eps = ep1.wells()+ep2.wells()

    pip50.pick_up_tip()

    for well in tbs:
        pip50.transfer(25, methemo, well.top(-10), new_tip='never')

    pip50.drop_tip()

    for src, dest in zip(eps, tbs):
        pip50.transfer(5, src, dest.top(-10), new_tip='always')

    robot.pause("Remove tubes from OT-2 and incubate at 37C in water bath for \
    45 minutes. After incubation, return tubes to robot and click RESUME.")

    pip1k.pick_up_tip()

    for well in tbs:
        pip1k.transfer(100, h2o2, well.top(-10), new_tip='never')

    robot.pause('Vortex tubes and then let sample incubate for 1 hour. When \
    ready to resume, click RESUME.')

    dest_sets = [row[i*2:i*2+2] for i in range(6) for row in fp.rows()]

    for src, dest in zip(tbs, dest_sets):
        pip1k.transfer(200, src, [well.top(-60) for well in dest])

    robot.comment('Congratulations, the protocol is now complete!')
