from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'eppendorf_96_wellplate_150_pcr'
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
mag_plate = labware.load(plate_name, '1', share=True)
elution_plate = labware.load(plate_name, '2')
res12 = labware.load('usascientific_12_reservoir_22ml', '4')
tipracks50 = [
    labware.load('opentrons_96_tiprack_300ul', slot)
    for slot in ['3', '5', '6', '7', '8', '9', '10']
]

# reagents
beads = res12.wells()[0]
etoh = res12.wells()[1:3]
elution_buffer = res12.wells()[3]
liquid_waste = [chan.top() for chan in res12.wells()[10:]]


def run_custom_protocol(
        p50_multi_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 96
):
    # check
    if number_of_samples < 1 or number_of_samples > 96:
        raise Exception('Invalid sample number (must be from 1-96).')

    # pipettes
    m50 = instruments.P50_Multi(mount=p50_multi_mount, tip_racks=tipracks50)

    # samples
    num_cols = math.ceil(number_of_samples/8)
    mag_samples = mag_plate.rows('A')[:num_cols]
    elution_samples = elution_plate.rows('A')[:num_cols]

    tip_count = 0
    tip_max = len(tipracks50)*12

    def pick_up():
        nonlocal tip_count
        if tip_count == tip_max:
            robot.pause('Please replace tipracks before resuming.')
            m50.reset()
            tip_count = 0
        tip_count += 1
        m50.pick_up_tip()

    # mix, transfer, and mix beads
    pick_up()
    for _ in range(5):
        m50.aspirate(40, beads.bottom(3))
        m50.dispense(40, beads.bottom(15))
    m50.blow_out(beads.top(-5))
    for m in mag_samples:
        if not m50.tip_attached:
            pick_up()
        m50.transfer(15, beads, m, new_tip='never')
        m50.mix(3, 10, m)
        m50.blow_out(m.top(-2))
        m50.drop_tip()

    # incubation
    robot.comment('Incubating off magnet 2 minutes.')
    m50.delay(minutes=2)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    robot.comment('Incubating on magnet 2 minutes.')
    m50.delay(minutes=2)

    # discard supernatant
    for m in mag_samples:
        if not m50.tip_attached:
            pick_up()
        m50.transfer(
            45, m.bottom(0.5), liquid_waste[0], new_tip='never', air_gap=5)
        m50.blow_out()
        m50.drop_tip()

    # EtOH washes
    for wash in range(2):
        # transfer EtOH
        for m in mag_samples:
            tip_count += 3
            if tip_count >= tip_max:
                robot.pause('Please replace tipracks before resuming.')
                m50.reset()
                tip_count = 0
            m50.transfer(140, etoh[wash], m.bottom(5), new_tip='always')

        # incubate
        robot.comment('Incubating on magnet 2 minutes.')
        m50.delay(minutes=2)

        # discard supernatant
        for m in mag_samples:
            if not m50.tip_attached:
                pick_up()
            m50.transfer(
                150, m.bottom(0.5), liquid_waste[wash], new_tip='never')
            m50.blow_out()
            m50.drop_tip()

    # air dry
    magdeck.disengage()
    robot.comment('Airdrying on magnet 5 minutes.')
    m50.delay(minutes=5)

    # resuspend
    angles = [0 if i % 2 == 0 else math.pi for i in range(num_cols)]
    mix_locs = [
        (well, well.from_center(r=0.8, h=-0.9, theta=angle))
        for angle, well in zip(angles, mag_samples)
    ]
    for mix_loc, m in zip(mix_locs, mag_samples):
        pick_up()
        m50.aspirate(18, elution_buffer)
        m50.move_to(m)
        m50.dispense(18, mix_loc)
        m50.mix(3, 10, mix_loc)
        m50.blow_out(m.bottom(4))
        m50.drop_tip()

    # separate beads
    robot.comment('Incubating on magnet 2 minutes.')
    magdeck.engage(height=18)
    m50.delay(minutes=2)

    # transfer eluent
    for m, e in zip(mag_samples, elution_samples):
        pick_up()
        m50.transfer(14, m.bottom(0.5), e, new_tip='never')
        m50.blow_out()
        m50.drop_tip()

    magdeck.disengage()
