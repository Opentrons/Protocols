from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Zymobiomics Magbead Nucleic Acid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_name = 'vwr_96_wellplate_2ml_deep'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=40,
        volume=2000
    )

# load labware
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(
    deep_name, '1', 'deepwell plate (on magdeck)', share=True)
output_rack = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '2',
    'output 1.5ml snapcap tubes'
)
mbb = labware.load('opentrons_6_tuberack_falcon_50ml_conical', '3').wells()[0]
orig_tuberack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap',
    '4',
    'original 2ml screwcap tubes in aluminum block'
)
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '5', 'reagent reservoir')
tipracks_m = [
    labware.load('opentrons_96_tiprack_300ul', slot, '300ul tiprack')
    for slot in ['6', '9']
]
tipracks_s = labware.load('opentrons_96_tiprack_300ul', '8', '300ul tiprack')
waste = labware.load(
    'agilent_1_reservoir_290ml', '11', 'liquid waste').wells(0).top()


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        p300_single_mount: StringSelection('left', 'right') = 'left',
        number_of_samples: int = 24,
        volume_of_beads_in_ul: float = 30,
        bead_separation_time_in_minutes: int = 2,
        dry_on_temperature_module: StringSelection('yes', 'no') = 'yes'
):
    # check
    if number_of_samples > 24:
        raise Exception('Can only process up to 24 samples.')
    if volume_of_beads_in_ul < 30:
        raise Exception('WARNING: bead volume \
' + str(volume_of_beads_in_ul) + ' is lower than P300 range.')

    # pipette
    if p300_multi_mount == p300_single_mount:
        raise Exception('Pipette mounts cannot match.')
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tipracks_m)
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=[tipracks_s])

    # reagent setup
    beads = res12.wells()[0]
    magwash1 = res12.wells()[1]
    magwash2 = res12.wells()[2:4]

    # sample setup
    source_tubes = orig_tuberack.wells()[:number_of_samples]
    mag_samples = mag_plate.wells()[:number_of_samples]
    num_cols = math.ceil(number_of_samples/8)
    mag_cols = mag_plate.rows('A')[:num_cols]
    output_tubes = output_rack.wells()[:number_of_samples]

    if dry_on_temperature_module == 'yes':
        tempdeck = modules.load('tempdeck', '7')
        temp_plate = labware.load(
            deep_name, '7', 'spot for drying mid-protocol', share=True)
        p300.pick_up_tip()
        p300.aspirate(30, temp_plate.wells()[0].top(10))
        p300.dispense(30, temp_plate.wells()[0].top(10))

    # transfer samples to magnetic plate
    for s, d in zip(source_tubes, mag_samples):
        if not p300.tip_attached:
            p300.pick_up_tip()
        p300.transfer(200, s.bottom(5), d.bottom(10), new_tip='never')
        p300.blow_out()
        p300.drop_tip()

    mbb_h = 70
    r = 27.81/2

    # transfer mag binding buffer
    m300.pick_up_tip()
    dh = 600/(math.pi*(r**2))*1.1  # adjust height from which to aspirate MBB
    for m in mag_cols:
        if mbb_h - dh > 10:
            mbb_h -= dh
        else:
            mbb_h = 10
        m300.transfer(600, mbb.bottom(mbb_h), m.top(), new_tip='never')
        m300.blow_out()
    m300.drop_tip()

    # mix and transfer beads
    m300.pick_up_tip()
    for _ in range(10):
        m300.aspirate(100, beads.bottom(5))
        m300.dispense(100, beads.bottom(20))
    m300.blow_out(beads.top(-5))
    for m in mag_cols:
        if not m300.tip_attached:
            m300.pick_up_tip()
        m300.transfer(volume_of_beads_in_ul, beads, m, new_tip='never')
        m300.mix(5, 200, m.bottom(5))
        m300.blow_out(m.top(-5))
        m300.drop_tip()

    # remove supernatant
    magdeck.engage(height=14.94)
    m300.delay(minutes=bead_separation_time_in_minutes)
    for m in mag_cols:
        m300.transfer(900, m, waste)

    # 3x magwashes
    angles_s = [
        0 if i//8 % 2 == 0 else math.pi
        for i, col in enumerate(mag_cols)
    ]
    angles_m = [0 if i % 2 == 0 else math.pi for i, col in enumerate(mag_cols)]
    mix_locs_s, mix_locs_m = [
        [(col, col.from_center(theta=angle, r=0.85, h=-0.9))
         for col, angle in zip(mag_cols, angles)]
        for angles in [angles_s, angles_m]
    ]
    for wash in [magwash1] + [w for w in magwash2]:
        magdeck.disengage()
        for m, mix_loc in zip(mag_cols, mix_locs_m):
            # resuspend beads in wash
            m300.pick_up_tip()
            m300.transfer(900, wash, m.top(), new_tip='never')
            m300.move_to(m.bottom(0.5))
            m300.mix(10, 250, mix_loc)
            m300.blow_out(m.top())
            # separate out beads and remove supernatant
            magdeck.engage(height=14.94)
            m300.delay(minutes=bead_separation_time_in_minutes)
            m300.transfer(950, m, waste, new_tip='never')
            m300.drop_tip()

    # dry beads
    if dry_on_temperature_module == 'yes':
        robot.comment('Temperature module reaching temp...')
        tempdeck.wait_for_temp()
        robot._driver.run_flag.wait()
        robot.pause('Replace tubes A1-C1 in original sample rack (slot 2) with \
molecular grade water. Move plate from magnetic module to temperature module \
to dry. Replace the plate on the magnetic module and resume when ready.')
    else:
        robot.pause('Replace tubes A1-C1 in original sample rack (slot 2) with \
molecular grade water. Resume once the beads are sufficiently dry.')

    # transfer water and mix iteratively
    magdeck.disengage()
    water_tubes = orig_tuberack.wells()[:3]
    for i, (m, mix_loc) in enumerate(zip(mag_samples, mix_locs_s)):
        water_tube = water_tubes[i//8]
        p300.pick_up_tip()
        p300.transfer(200, water_tube, m, new_tip='never')
        p300.move_to(m.bottom(5))
        p300.mix(10, 100, mix_loc)
        p300.blow_out(m.top(-5))
        p300.drop_tip()

    tip_locs = []
    for mix in range(4):
        m300.delay(minutes=1)
        for i, (m, mix_loc) in enumerate(zip(mag_cols, mix_locs_m)):
            if mix == 0:
                m300.pick_up_tip()
                tip_locs.append(m300.current_tip())
            else:
                m300.pick_up_tip(tip_locs[i])
            m300.move_to(m.bottom(5))
            m300.mix(10, 100, mix_loc)
            m300.blow_out(m.top(-5))
            if mix == 3:
                m300.drop_tip()
            else:
                m300.return_tip()

    # separate beads and transfer eluent to new tubes
    magdeck.engage(height=14.94)
    m300.delay(minutes=bead_separation_time_in_minutes)
    for s, d in zip(source_tubes, output_tubes):
        p300.transfer(200, s, d.top(-5))

    magdeck.disengage()
