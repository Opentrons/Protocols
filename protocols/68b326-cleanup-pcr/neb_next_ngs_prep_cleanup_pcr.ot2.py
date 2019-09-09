from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NEB Next Ultra II FS Library Prep: Cleanup of PCR \
Reaction',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
pcr_name = 'biorad_96_wellplate_350ul_pcr'
if pcr_name not in labware.list():
    labware.create(
        pcr_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=19.85,
        volume=350
    )

res_name = 'axygen_12_reservoir_22ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=8.3,
        depth=42,
        volume=22000
    )

# load labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(pcr_name, '1', 'PCR plate', share=True)
elution_plate = labware.load(pcr_name, '2', 'elution plate')
res12 = labware.load(res_name, '4', 'reagent reservoir')
tips50 = [
    labware.load('opentrons_96_tiprack_300ul', slot)
    for slot in ['3', '5', '6', '7']
]
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', str(slot))
    for slot in range(8, 12)
]

# reagents
etoh = res12.wells('A1', length=2)
te = res12.wells('A3')
spri_beads = res12.wells('A5')
liquid_waste = [well.top() for well in res12.wells('A10', length=3)]


def run_custom_protocol(
        p50_multi_mount: StringSelection('right', 'left') = 'right',
        p300_multi_mount: StringSelection('left', 'right') = 'left',
        number_of_sample_to_process: int = 96
):
    # check
    if p50_multi_mount == p300_multi_mount:
        raise Exception('Input different mounts for P10 and P300 pipettes.')
    if number_of_sample_to_process > 96 or number_of_sample_to_process < 1:
        raise Exception('Invalid number of samples to process (should be \
between 1 and 96)')

    # pipettes
    m50 = instruments.P50_Multi(mount=p50_multi_mount, tip_racks=tips50)
    m300 = instruments.P300_Single(
        mount=p300_multi_mount, tip_racks=tips300)

    # setup
    num_cols = math.ceil(number_of_sample_to_process/8)
    mag_samples_multi = mag_plate.rows('A')[:num_cols]
    elution_samples_multi = elution_plate.rows('A')[:num_cols]

    tip50_count = 0
    tip300_count = 0
    tip50_max = len(tips50)*12
    tip300_max = len(tips300)*12

    def pick_up(pip):
        nonlocal tip50_count
        nonlocal tip300_count

        if pip == m300:
            if tip300_count == tip300_max:
                robot.pause('Refill 300ul tip racks before resuming.')
                tip300_count = 0
                m300.reset()
            tip300_count += 1
        else:
            if tip50_count == tip50_max:
                robot.pause('Refill 10ul tip racks before resuming.')
                tip50_count = 0
                m50.reset()
            tip50_count += 1
        pip.pick_up_tip()

    def mix(reps, vol, loc, pip, disp_perc=0.5):
        if pip == m50:
            a, d = 12.5, 50*disp_perc
        else:
            a, d = 75, 300*disp_perc
        pip.set_flow_rate(aspirate=a, dispense=d)
        for _ in range(reps):
            pip.aspirate(vol, loc)
            pip.delay(seconds=3)
            pip.dispense(vol, loc)
            pip.delay(seconds=3)
        pip.set_flow_rate(aspirate=2*a, dispense=d/disp_perc)

    # mix and distribute beads to intitial PCR plate
    pick_up(m300)
    mix(5, 100, spri_beads, m300)
    m300.distribute(
        45, spri_beads, [m.top() for m in mag_samples_multi], new_tip='never')
    for m in mag_samples_multi:
        if not m300.tip_attached:
            pick_up(m300)
        mix(5, 50, m, m300)
        m300.drop_tip()

    robot.comment('Room temperature incubation for 5 minutes')
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    robot.comment('Magnetic separation for 5 minutes')
    m300.delay(minutes=5)

    # discard supernatant
    for m in mag_samples_multi:
        pick_up(m300)
        m300.aspirate(100, m.bottom(0.5))
        m300.delay(seconds=3)
        m300.dispense(100, liquid_waste[2])
        m300.drop_tip()

    # ethanol washes
    for wash in range(2):
        pick_up(m300)
        for m in mag_samples_multi:
            m300.transfer(200, etoh[wash], m.top(), new_tip='never')
        m300.delay(seconds=30)
        for m in mag_samples_multi:
            if not m300.tip_attached:
                pick_up(m300)
            m300.aspirate(210, m.bottom(0.5))
            m300.delay(seconds=3)
            m300.dispense(210, liquid_waste[wash])
            m300.drop_tip()

    robot.comment('Delaying 5 minutes')
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    # distribute TE and resuspend
    pick_up(m50)
    m50.distribute(
        33, te, [m.top() for m in mag_samples_multi], new_tip='never')
    for i, m in enumerate(mag_samples_multi):
        if not m50.tip_attached:
            pick_up(m50)
        angle = 0 if i % 2 == 0 else math.pi
        disp_loc = (m, m.from_center(r=0.95, h=-0.6, theta=angle))
        mix(10, 20, disp_loc, m50, disp_perc=1.0)
        m50.drop_tip()

    robot.comment('Room temperature incubation for 5 minutes')
    m50.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    robot.comment('Magnetic incubation for 5 minutes')
    m50.delay(minutes=5)

    # transfer supernatant
    for m, e in zip(mag_samples_multi, elution_samples_multi):
        pick_up(m50)
        m50.aspirate(15, m.bottom(0.5))
        m50.delay(seconds=3)
        m50.dispense(15, e)
        m50.blow_out()
        m50.drop_tip()
