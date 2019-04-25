from opentrons import labware, instruments, modules
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NGS Library Prep: BP Post Index 2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_name = 'Zymo-96-deep'
if deep_name not in labware.list():
    labware.create(
        grid=(12, 8),
        spacing=(8, 8),  # check
        diameter=7,  # check
        depth=31,  # check
        volume=1100)

plate_name = 'MicroAmp-96-PCR'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.49,
        depth=20.1,
        volume=200)

# labware
strips = labware.load('PCR-strip-tall', '2')
tubes_ep = labware.load('opentrons-tuberack-2ml-eppendorf', '3')
tubes_falcon = labware.load('opentrons-tuberack-15ml', '4')
tips_10 = labware.load('tiprack-10ul', '7')
sample_tips = labware.load('tiprack-200ul', '9')

# modules
magdeck = modules.load('magdeck', '1')
mag_strips = labware.load('opentrons-aluminum-block-PCR-strips-200ul',
                          '1',
                          share=True)

# pipettes
p10 = instruments.P10_Single(mount='right')
p300 = instruments.P300_Single(mount='left')


def run_custom_protocol(
        beads_strip_column: StringSelection('1', '2', '3', '4', '5', '6', '7',
                                            '8', '9', '10', '11', '12') = '4',
        elution_strip_column: StringSelection('1', '2', '3', '4', '5', '6',
                                              '7', '8', '9', '10', '11',
                                              '12') = '5'):
    # reagent setup
    beads = mag_strips.columns(beads_strip_column)
    empty_strips = [well for col in
                    mag_strips.columns(elution_strip_column)
                    for well in col]
    TE = tubes_ep.wells('A1')
    ethanol = tubes_falcon.wells('A1')

    # initialize ethanol height trackers, assuming that reagents are filled to
    # 14ml line in standard 15ml tube
    h_track = -18
    pi = math.pi
    r_cyl = 7.52

    # distribute beads and mix:
    sample_locs = mag_strips.wells(0, length=12)
    beads_tips = sample_tips.wells(0, length=12)
    for ind, (tip, dest) in enumerate(zip(beads_tips, sample_locs)):
        p300.pick_up_tip(tip)
        bead_source = ind // 2
        p300.transfer(40, beads[bead_source], dest, new_tip='never')
        p300.mix(8, 40, dest)
        p300.drop_tip()

    # first pooling
    tip_count = 12
    for set in range(2):
        for i in range(3):
            tip = sample_tips.wells(tip_count)
            p300.pick_up_tip(tip)
            tip_count += 1
            pool_ind = set*6+i
            p300.transfer(90,
                          mag_strips.wells(pool_ind+3),
                          mag_strips.wells(pool_ind),
                          new_tip='never')
            p300.return_tip()

    # move pools 79 directly after pools 1-3
    for tip, source, dest in zip(sample_tips.wells(3, length=3),
                                 mag_strips.wells(6, length=3),
                                 mag_strips.wells(3, length=3)):
        p300.pick_up_tip(tip)
        p300.transfer(180, source, dest, new_tip='never')
        p300.return_tip()

    p300.delay(minutes=5)
    magdeck.engage(height=18)
    p300.delay(minutes=10)

    new_pools = [well for well in mag_strips.wells(0, length=6)]
    # transfer out supernatant
    for tip, well in zip(sample_tips.wells(), new_pools):
        p300.pick_up_tip(tip)
        p300.transfer(180,
                      well,
                      p300.trash_container.top(),
                      blow_out=True,
                      new_tip='never')
        p300.return_tip()

    ethanol_tip = sample_tips.wells('H11')
    # 3 ethanol washes
    for _ in range(3):
        # calculate ethanol height to aspirate from and transfer
        p300.pick_up_tip(ethanol_tip)
        for n in new_pools:
            p300.transfer(200,
                          ethanol.top(h_track),
                          n.top(),
                          new_tip='never')
            h_track -= 200/(pi*(r_cyl**2))
        p300.return_tip()

        p300.delay(seconds=30)

        for tip, well in zip(sample_tips.wells(), new_pools):
            p300.pick_up_tip(tip)
            p300.transfer(200,
                          well,
                          p300.trash_container.top(),
                          blow_out=True,
                          new_tip='never')
            p300.return_tip()

    # dry pellet
    p300.delay(minutes=8)

    # resuspend in TE
    magdeck.disengage()
    TE_tip = sample_tips.wells('H12')
    p10.pick_up_tip(TE_tip)
    p10.transfer(10.5, TE, [p.top() for p in new_pools], new_tip='never')
    p10.drop_tip()
    p10.delay(minutes=2)
    magdeck.engage(height=18)
    p10.delay(minutes=5)

    # transfer to new strips
    for tip, source, dest in zip(sample_tips.wells(), new_pools, empty_strips):
        p10.pick_up_tip(tip)
        p10.transfer(10, source, dest, new_tip='never')
        p10.drop_tip()
