from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NGS Library Cleanup with Ampure XP Beads',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = "twintec_PCR_plate"
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        depth=14.6,
        diameter=6.46,
        volume=150
    )


# load labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(plate_name, '1', 'magnetic plate', share=True)
elution_plate = labware.load(
    plate_name, '2', 'elution plate')
tips300 = [
    labware.load('opentrons_96_filtertiprack_200ul', slot)
    for slot in ['5', '6', '8', '9']
]
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '7', 'reagent reservoir')
tips10 = labware.load('opentrons_96_filtertiprack_10ul', '3')

# reagents
beads = res12.wells('A1')
etoh = res12.wells('A2')
eb_buff = res12.wells('A3')
waste = [chan.top(-10) for chan in res12.wells('A11', length=2)]


def run_custom_protocol(
        p10_multi_mount: StringSelection('right', 'left') = 'right',
        p300_multi_mount: StringSelection('left', 'right') = 'left',
        number_of_samples: int = 48,
        bead_incubation_time_in_minutes: int = 10,
        bead_settling_time_on_magnet_in_minutes: int = 10,
        drying_time_in_minutes: int = 5,
        volume_EB_in_ul: float = 37.5,
        volume_final_elution_in_ul: float = 35
):
    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples.')
    if p10_multi_mount == p300_multi_mount:
        raise Exception('Pipette mounts cannot match.')

    # location for safe tip drop

    def drop(pip):
        pip.move_to(res12.wells()[7].top(10))
        pip.drop_tip()

    # pipettes
    m10 = instruments.P10_Multi(mount=p10_multi_mount, tip_racks=[tips10])
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)

    # sample setup
    num_cols = math.ceil(number_of_samples/8)
    mag_samples = mag_plate.rows('A')[:num_cols]
    elution_samples = elution_plate.rows('A')[:num_cols]

    # mix beads
    robot.head_speed(z=50, a=50)
    # transfer beads and mix samples
    for m in mag_samples:
        m300.pick_up_tip()
        m300.mix(5, 200, beads)
        m300.blow_out(beads.top())
        m300.transfer(110, beads, m, new_tip='never')
        m300.blow_out()
        m300.mix(10, 130, m)
        m300.blow_out(m.top())
        drop(m300)
    robot.head_speed(z=125, a=125)

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
    for m in mag_samples:
        m300.pick_up_tip()
        m300.transfer(
            160, m.bottom(0.5), waste[1], new_tip='never')
        m300.blow_out(waste[1])
        drop(m300)

    # 2x EtOH washes
    for _ in range(2):
        # transfer EtOH
        for m in mag_samples:
            m300.pick_up_tip()
            m300.transfer(180, etoh, m, new_tip='never', air_gap=20)
            m300.blow_out(m)
            drop(m300)

        robot.comment('Incubating for 1 minute.')
        m300.delay(minutes=1)

        # remove supernatant
        for m in mag_samples:
            m300.pick_up_tip()
            m300.transfer(
                180, m.bottom(0.5), waste[0], new_tip='never')
            m300.blow_out(waste[0])
            drop(m300)

    # remove residual supernatant
    for m in mag_samples:
        m10.pick_up_tip()
        m10.transfer(
            10, m.bottom(0.5), waste[1], new_tip='never')
        m10.blow_out()
        drop(m10)

    robot.comment('Drying for ' + str(drying_time_in_minutes) + ' minutes.')
    m300.delay(minutes=drying_time_in_minutes)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    # transfer EB buffer
    for m in mag_samples:
        m300.pick_up_tip()
        m300.aspirate(30, eb_buff.top(5))
        m300.aspirate(volume_EB_in_ul, eb_buff)
        m300.dispense(30+volume_EB_in_ul, m)
        m300.blow_out()
        drop(m300)

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
        m300.aspirate(30, m.top(5))
        m300.aspirate(volume_final_elution_in_ul, m)
        m300.dispense(volume_final_elution_in_ul, e)
        m300.dispense(30, e.bottom(7))
        m300.blow_out(e.top(-2))
        drop(m300)

    magdeck.disengage()
