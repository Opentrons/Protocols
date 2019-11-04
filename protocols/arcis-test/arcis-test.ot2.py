from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Arcis Blood Extraction and PCR Setup',
    'author': 'Chaz <chaz@opentrons.com',
    'source': 'Custom Protocol Request'
}

# create labware
tips = labware.load('opentrons_96_tiprack_300ul', '1', 'Opentrons Tips')
cp = labware.load('corning_96_wellplate_360ul_flat', '2', 'Corning Plate')
tube10 = labware.load(
    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '6', '10 Tube Rack'
)
tube24 = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '5', '1.5mL Tube Rack'
)
bp_name = 'bioplastics_96_wellplate_100ul'
if bp_name not in labware.list():
    labware.create(
        bp_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.07,
        depth=14,
        volume=100
    )
bp1 = labware.load(bp_name, '3', 'Bioplastics Plate')
bp2 = labware.load(bp_name, '4', 'Bioplastics Plate')

# create reagents
reagent1 = tube10.wells('A3')
reagent2 = tube10.wells('A1')
mastermix = tube24.wells('A2')
sample = tube24.wells('A1')

y = 'ABC'
well_list = []
for i in range(1, 7):
    for j in y:
        well_list.append(j+str(i))
well_list += ['A12', 'H12']

cpwells = cp.wells(well_list)
bp1wells = bp1.wells(well_list)
bp2wells = bp2.wells(well_list)


def run_custom_protocol(
    p50_mount: StringSelection('left', 'right') = 'left',
    p300_mount: StringSelection('right', 'left') = 'right'
):
    # create pipette
    p50 = instruments.P50_Single(mount=p50_mount)
    p300 = instruments.P300_Single(mount=p300_mount)

    # create tip sharing
    tipcount = 0

    def pick_up(pip):
        nonlocal tipcount
        if pip == p50:
            p50.pick_up_tip(tips.wells(tipcount))
        else:
            p300.pick_up_tip(tips.wells(tipcount))
        tipcount += 1

    # transfer 1
    pick_up(p300)
    for dest in cpwells:
        p300.transfer(150, reagent1, dest, new_tip='never')
    p300.drop_tip()

    # transfer 2
    pick_up(p50)
    for dest in bp1wells:
        p50.transfer(20, reagent2, dest, new_tip='never')
    p50.drop_tip()

    # transfer 3
    for dest in cpwells:
        pick_up(p50)
        p50.transfer(30, sample, dest, new_tip='never')
        p50.drop_tip()

    # transfer 4
    for src, dest in zip(cpwells, bp1wells):
        pick_up(p50)
        p50.transfer(5, src, dest, new_tip='never')
        p50.drop_tip()

    # transfer 5
    pick_up(p50)
    for dest in bp2wells:
        p50.transfer(20, mastermix, dest, new_tip='never')
    p50.drop_tip()

    # transfer 6
    for src, dest in zip(bp1wells, bp2wells):
        pick_up(p50)
        p50.transfer(5, src, dest, new_tip='never')
        p50.drop_tip()

    robot.comment('Protocol complete.')
