from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Zymo Research Direct-zol-96 RNA MagPrep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_name = 'axygen_96_wellplate_2ml_deep'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.2,
        depth=41.5,
        volume=2000
    )

# load labware and modules
elution_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'elution plate')
etoh = labware.load('agilent_1_reservoir_290ml', '2', 'EtOH').wells(0)
waste_list = [
    res.wells(0).top()
    for res in [
        labware.load('agilent_1_reservoir_290ml', slot, 'waste')
        for slot in ['3', '6']
    ]
]
magdeck = modules.load('magdeck', '4')
mag_plate = labware.load(deep_name, '4', 'deepwell block', share=True)
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '5', 'reagent reservoir')
tips300 = [
    labware.load(
        'opentrons_96_tiprack_300ul', str(slot)) for slot in range(7, 12)
]

# reagents
beads = res12.wells()[0]
dnase = res12.wells()[1]
rna_buff = res12.wells()[2:5]
wash1 = res12.wells()[5:8]
wash2 = res12.wells()[8:11]
water = res12.wells(11)


def run_custom_protocol(
        number_of_samples_to_process: int = 96,
        p300_multi_mount: StringSelection('left', 'right') = 'left',
        volume_of_beads_in_ul: float = 30,
        bead_separation_time_in_minutes: int = 3
):
    # check
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples (must be 1-96).')

    # pipettes
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)

    # setup
    num_cols = math.ceil(number_of_samples_to_process/8)
    mag_samples = mag_plate.rows('A')[:num_cols]
    disp_locs = []
    for i, m in enumerate(mag_samples):
        angle = 0 if i % 2 == 0 else math.pi
        disp_loc = (m, m.from_center(r=0.9, h=-0.95, theta=angle))
        disp_locs.append(disp_loc)
    elution_samples = elution_plate.rows('A')[:num_cols]

    waste_ind = 0
    waste = waste_list[waste_ind]
    waste_vol = 0

    def waste_check(vol):
        nonlocal waste_vol
        nonlocal waste_ind
        nonlocal waste
        waste_vol += vol
        if waste_vol > 270000:
            waste_vol = 0
            if waste_ind < len(waste_list-1):
                waste_ind += 1
                waste = waste_list[waste_ind]
            else:
                robot.pause('Empty waste reservoirs in slots 3 and 6 and \
replace before resuming.')
                waste_ind = 0
                waste = waste_list[waste_ind]
        return waste

    etoh_vol = 0

    def etoh_check(vol):
        nonlocal etoh_vol
        etoh_vol -= vol
        if etoh_vol > 270000:
            robot.pause('Refill EtOH reservoir in slot 2 before resuming.')
            etoh_vol = 0

    tip_count = 0
    tip_max = len(tips300)*12

    def pick_up(loc=None):
        nonlocal tip_count
        if tip_count == tip_max:
            robot.pause('Replace 300ul tipracks before resuming.')
            m300.reset()
            tip_count = 0
        if loc:
            m300.pick_up_tip(loc)
        else:
            m300.pick_up_tip()
            tip_count += 1

    def etoh_wash_3x():
        tip_locs = []
        for wash in range(3):
            magdeck.disengage()
            for t, (s, d) in enumerate(zip(mag_samples, disp_locs)):
                if wash == 0:
                    pick_up()
                    tip_locs.append(m300.current_tip())
                else:
                    pick_up(tip_locs[t])
                etoh_check(500)
                m300.transfer(500, etoh, s.top(), new_tip='never')
                m300.mix(10, 250, d)
                m300.blow_out(s.top())
                m300.return_tip()
            magdeck.engage(height=14.93)
            m300.delay(minutes=bead_separation_time_in_minutes)
            for t, s in zip(tip_locs, mag_samples):
                pick_up(t)
                w = waste_check(500)
                m300.transfer(500, s, w, new_tip='never')
                if wash < 2:
                    m300.return_tip()
                else:
                    m300.drop_tip()

    def magbead_wash(w):
        magdeck.disengage()
        tip_locs = []
        for i, (s, d) in enumerate(zip(mag_samples, disp_locs)):
            r_ind = i//5
            pick_up()
            tip_locs.append(m300.current_tip())
            m300.transfer(500, w[r_ind], s.top(), new_tip='never')
            m300.mix(10, 250, d)
            m300.blow_out(s.top())
            m300.return_tip()
        magdeck.engage(height=14.93)
        m300.delay(minutes=bead_separation_time_in_minutes)
        for t, s in zip(tip_locs, mag_samples):
            pick_up(t)
            w = waste_check(500)
            m300.transfer(550, s, w, new_tip='never')
            m300.drop_tip()

    # add beads
    pick_up()
    m300.distribute(
        volume_of_beads_in_ul,
        beads,
        [s.top() for s in mag_samples],
        new_tip='never'
    )
    m300.drop_tip()

    # add first EtOH
    tip_locs = []
    for s in mag_samples:
        pick_up()
        tip_locs.append(m300.current_tip())
        etoh_check(450)
        m300.transfer(450, etoh, s, new_tip='never')
        m300.mix(10, 250, s)
        m300.blow_out(s.top())
        m300.drop_tip()

    # iterative mixing
    for mix in range(3):
        for t, m in zip(tip_locs, mag_samples):
            robot.comment('Incuating with iterative mixing...')
            m300.delay(minutes=2)
            pick_up(t)
            m300.mix(5, 200, m)
            m300.blow_out(m.top(-2))
            if mix < 2:
                m300.return_tip()
            else:
                m300.drop_tip()

    magdeck.engage(height=14.93)
    robot.comment('Beads separating for supernatant removal')
    m300.delay(minutes=bead_separation_time_in_minutes)

    # remove supernatant
    for m in mag_samples:
        pick_up()
        w = waste_check(1000)
        m300.transfer(1000, m, waste_list[0], new_tip='never')
        m300.drop_tip()

    # first set of 3x EtOH washes
    etoh_wash_3x()
    robot.comment('Airdrying beads for 5 minutes.')
    m300.delay(minutes=5)

    # transfer DNAse 1
    magdeck.disengage()
    for d, s in zip(disp_locs, mag_samples):
        pick_up()
        m300.transfer(50, dnase, d, new_tip='never')
        m300.mix(10, 40, d)
        m300.blow_out(s.top())
        m300.drop_tip()

    robot.comment('Incubating for 10 minutes.')
    m300.delay(minutes=10)

    # transfer RNA buffer
    tip_locs = []
    for i, s in enumerate(mag_samples):
        r_ind = i//5
        pick_up()
        tip_locs.append(m300.current_tip())
        m300.transfer(500, rna_buff[r_ind], s.top(), new_tip='never')
        m300.mix(10, 250, s)
        m300.blow_out(s.top())
        m300.return_tip()

    robot.comment('Incubating off magnet for 5 minutes')
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=14.93)
    robot.comment('Beads separating.')
    m300.delay(minutes=bead_separation_time_in_minutes)

    # remove supernatant
    for t, s in zip(tip_locs, mag_samples):
        pick_up(t)
        w = waste_check(550)
        m300.transfer(550, s, w, new_tip='never')
        m300.drop_tip()

    # wash 1
    magbead_wash(wash1)

    # wash 2
    magbead_wash(wash2)

    # second set of 3x EtOH washes
    etoh_wash_3x()
    robot.pause('Let the beads dry, ideally at 55C or let the plate seat for \
20min. Replace plate on magnetic module when finished if necessary before \
resuming.')

    # add DNAse/RNAse-free water and mix during 8 minute incubation
    magdeck.disengage()
    pick_up()
    m300.distribute(50, water, [s.top() for s in mag_samples], new_tip='never')
    tip_locs = []
    for mix_rep in range(3):
        for t, (s, d) in enumerate(zip(mag_samples, disp_locs)):
            if mix_rep == 0:
                if not m300.tip_attached:
                    m300.pick_up_tip()
                tip_locs.append(m300.current_tip())
            else:
                pick_up(tip_locs[t])
            m300.mix(10, 250, d)
            m300.blow_out(s.bottom(10))
            m300.return_tip()
        robot.comment('Incubating before next mix...')
        m300.delay(minutes=2)

    robot._driver.run_flag.wait()
    magdeck.engage(height=14.93)
    robot.comment('Incubating on magnet for bead separation')
    m300.delay(minutes=bead_separation_time_in_minutes)

    # transfer eluate to a new PCR plate
    for t, s, e in zip(tip_locs, mag_samples, elution_samples):
        pick_up(t)
        m300.transfer(50, s, e, new_tip='never')
        m300.blow_out()
        m300.drop_tip()

    magdeck.disengage()
