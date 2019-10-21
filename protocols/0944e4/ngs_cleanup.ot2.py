from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NGS Library Cleanup with Ampure XP Beads',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = "twintec PCR plate"
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        depth=16.4,
        diameter=6.46,
        volume=150)


# load labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(plate_name, '1', 'magnetic plate', share=True)
elution_plate = labware.load(
    plate_name, '2', 'elution plate')
tips300 = [
    labware.load('opentrons_96_filtertiprack_200ul', slot)
    for slot in ['3', '5', '6', '9']
]
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '7', 'reagent reservoir')
tips10 = labware.load('opentrons_96_filtertiprack_10ul', '8')

# reagents
beads = res12.wells('A1')
etoh = res12.wells('A2')
eb_buff = res12.wells('A3')
waste = [chan.top() for chan in res12.wells('A11', length=2)]


def run_custom_protocol(
        p10_multi_mount: StringSelection('right', 'left') = 'right',
        p300_multi_mount: StringSelection('left', 'right') = 'left',
        number_of_samples: int = 48,
        bead_incubation_time_in_minutes: int = 10,
        bead_settling_time_on_magnet_in_minutes: int = 10,
        drying_time_in_minutes: int = 5
):
    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples.')
    if p10_multi_mount == p300_multi_mount:
        raise Exception('Pipette mounts cannot match.')

    # pipettes
    m10 = instruments.P10_Multi(mount=p10_multi_mount, tip_racks=[tips10])
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)

    # sample setup
    num_cols = math.ceil(number_of_samples/8)
    mag_samples = mag_plate.rows('A')[:num_cols]
    elution_samples = elution_plate.rows('A')[:num_cols]

    # mix beads
    m300.pick_up_tip()
    m300.mix(10, 200, beads)
    m300.blow_out(beads.top())

    # transfer beads and mix samples
    for m in mag_samples:
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.transfer(110, beads, m, new_tip='never')
        m300.mix(10, 130, m)
        m300.drop_tip()

    # incubation
    robot.comment('Incubating off magnet for \
' + str(bead_incubation_time_in_minutes) + ' minutes.')
    m300.delay(minutes=bead_incubation_time_in_minutes)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    robot.comment('Incubating on magnet for \
' + str(bead_settling_time_on_magnet_in_minutes) + ' minutes.')
    m300.delay(minutes=bead_settling_time_on_magnet_in_minutes)

    # remove supernatant
    m300.transfer(
        160, [m.bottom(0.5) for m in mag_samples], waste[1], new_tip='always')

    # 2x EtOH washes
    for _ in range(2):
        # transfer EtOH
        m300.transfer(180, etoh, mag_samples, new_tip='always', air_gap=20)

        robot.comment('Incubating for 1 minute.')
        m300.delay(minutes=1)

        # remove supernatant
        m300.transfer(
            200,
            [m.bottom(0.5) for m in mag_samples],
            waste[0],
            new_tip='always'
        )

    # remove residual supernatant
    m10.transfer(
        10,
        [m.bottom(0.3) for m in mag_samples],
        waste[1],
        new_tip='always'
    )

    robot.comment('Drying for ' + str(drying_time_in_minutes) + ' minutes.')
    m300.delay(minutes=drying_time_in_minutes)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    # transfer EB buffer
    m300.transfer(37.5, eb_buff, mag_samples, new_tip='always')

    robot.pause('Remove PCR plate, seal and shake at 1800 RPM for 2 minutes. \
Return PCR plate to magnetic module and incubate for 3 minutes before \
resuming.')

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    robot.comment('Incubating on magnet for 3 minutes.')
    m300.delay(minutes=3)

    # transfer supernatant to new PCR plate
    for m, e in zip(mag_samples, elution_samples):
        m300.pick_up_tip()
        m300.transfer(35, m, e, new_tip='never')
        m300.blow_out(e.top())
        m300.drop_tip()
