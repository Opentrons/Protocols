from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NGS Library Prep: Bead Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
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
plate1 = labware.load(plate_name, '2')
plate2 = labware.load(plate_name, '3')
strips = labware.load('opentrons-aluminum-block-PCR-strips-200ul', '4')
fresh_plate = labware.load(plate_name, '5')
tubes_ep = labware.load('opentrons-aluminum-block-2ml-eppendorf', '6')
tubes_falcon = labware.load('opentrons-tuberack-15ml', '7')
tips200 = [labware.load('tiprack-200ul', slot) for slot in ['8', '9']]
tips10_multi = labware.load('tiprack-10ul', '10')
tips10_single = labware.load('tiprack-10ul', '11')

# modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(plate_name, '1', share=True)

# pipettes
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tips10_multi]
)
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tips200
)


def run_custom_protocol(beads_strip_column: StringSelection('1', '2', '3', '4',
                                                            '5', '6', '7', '8',
                                                            '9', '10', '11',
                                                            '12') = '4'):

    # reagent setup
    beads = strips.columns(beads_strip_column)
    TE = tubes_ep.wells('A1')
    ethanol = tubes_falcon.wells('A1', length=2)
    plates = [plate1, plate2]
    rowA1 = [well for well in plate1.rows('A')]
    rowA2 = [well for well in plate2.rows('A')]

    # initialize ethanol height trackers, assuming that reagents are filled to
    # 14ml line in standard 15ml tube
    h_track = -18
    pi = math.pi
    r_cyl = 7.52

    # tip setup for single transfers using P10 multi-channel
    tip_rows = [row for row in tips10_single.rows()]
    tip_rows.reverse()
    tip_order = [well for row in tip_rows for well in row]
    tip_counter = 0

    # transfer beads to all wells of plates
    for plate in [rowA1, rowA2]:
        for well in plate:
            m10.pick_up_tip()
            m10.transfer(18.4, beads[0], well, new_tip='never')
            m10.mix(8, 10, well)
            m10.drop_tip()
            m10.reset()
        robot.pause('Replace 10ul tiprack in slot 10 with a full rack before '
                    'resuming.')

    # consolidate each column into well A of that column
    for plate in plates:
        for col in plate.columns():
            p300.consolidate(41.4, col[1:8], col[0])

    # incubate for 5 minutes
    p300.delay(minutes=5)
    robot._driver.run_flag.wait()

    # remove supernatant for each plate
    for ind, (plate_num, et_tube) in enumerate(zip(range(1, 3), ethanol)):
        robot.pause('Place sample plate %d on the magnetic module before '
                    'resuming.' % plate_num)
        robot._driver.run_flag.wait()
        magdeck.engage(height=18)

        # incubate on magnet for 10 minutes
        p300.delay(minutes=10)

        # remove supernatant
        p300.transfer(331.2,
                      mag_plate.rows('A'),
                      p300.trash_container.top(),
                      new_tip='always')

        # 3 ethanol washes
        for _ in range(3):
            # transfer and calculate next ethanol height to aspirate from
            p300.pick_up_tip()
            for s in mag_plate.rows('A'):
                p300.transfer(200,
                              et_tube.top(h_track),
                              s.top(),
                              new_tip='never')
                h_track -= 200/(pi*(r_cyl**2))
            p300.drop_tip()

            # incubate for 30 seconds
            p300.delay(seconds=30)

            # transfer out ethanol
            p300.transfer(200,
                          mag_plate.rows('A'),
                          p300.trash_container.top(),
                          new_tip='always')

        # reset ethanol height
        h_track = -18

        # dry pellet for 8 minutes
        p300.delay(minutes=8)
        robot._driver.run_flag.wait()

        # resuspend in TE
        magdeck.disengage()
        mag_sources = [well for well in mag_plate.rows('A')]
        dests1 = [well for well in fresh_plate.wells('A1', to='D2')]
        dests2 = [well for well in fresh_plate.wells('E2', to='H3')]
        dests = [dests1, dests2]
        set = dests[ind]
        for source, dest in zip(mag_sources, set):
            m10.pick_up_tip(tip_order[tip_counter])
            tip_counter += 1
            m10.transfer(10.5, TE, source, new_tip='never')
            m10.mix(10, 10, source)
            m10.transfer(10, source, dest, new_tip='never')
            m10.drop_tip()

        if plate_num == 1:
            robot.pause('Place sample plate %d back on the robot deck before '
                        'resuming.' % plate_num)
            robot._driver.run_flag.wait()
