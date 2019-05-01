from opentrons import labware, instruments, modules, robot
import math

metadata = {
    'protocolName': 'NGS Library Prep: Library Purification',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

pcr_plate_name = 'eppendorf-twin.tec-skirted-96-PCR'
if pcr_plate_name not in labware.list():
    labware.create(
        pcr_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.46,
        depth=14.6,
        volume=150)

tiprack_100ul_name = 'neptune-filter-tiprack-100ul'
if tiprack_100ul_name not in labware.list():
    labware.create(
        tiprack_100ul_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=40)

tiprack_10ul_name = 'neptune-filter-tiprack-10ul'
if tiprack_10ul_name not in labware.list():
    labware.create(
        tiprack_10ul_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=40)


def run_custom_protocol(
        sample_num: int=24):

    # labware setup
    new_plate = labware.load(pcr_plate_name, '1')
    trough = labware.load('trough-12row', '2')
    mag_module = modules.load('magdeck', '4')
    mag_plate = labware.load(pcr_plate_name, '4', share=True)

    tipracks_300 = [labware.load('tiprack-200ul', slot)
                    for slot in ['5', '6', '8']]

    # instruments setup
    m300 = instruments.P300_Multi(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    ampure_xp_beads = trough.wells('A1')
    ethanol = trough.wells('A2')
    elution_buffer = trough.wells('A3')

    sample_col = math.ceil(sample_num / 8)

    if mag_module._engaged:
        mag_module.disengage()

    # transfer AMPure XP Beads to samples
    for col in mag_plate.cols('1', length=sample_col):
        m300.pick_up_tip()
        m300.mix(5, 300, ampure_xp_beads)
        m300.blow_out(ampure_xp_beads)
        m300.transfer(45, ampure_xp_beads, col, new_tip='never')
        m300.mix(5, 30, col)
        m300.blow_out(col)
        m300.drop_tip()

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.engage(height=18)
    m300.delay(minutes=2)

    # remove supernatant
    for col in mag_plate.cols('1', length=sample_col):
        m300.transfer(90, col, m300.trash_container.top())

    # wash plate with ethanol
    m300.transfer(
        150,
        ethanol,
        [col[0].top() for col in mag_plate.cols('1', length=sample_col)],
        air_gap=True)
    for _ in range(5):
        mag_module.disengage()
        m300.delay(seconds=5)
        robot._driver.run_flag.wait()
        mag_module.engage(height=18)
        m300.delay(seconds=5)
        robot._driver.run_flag.wait()
    m300.delay(minutes=2)
    # remove supernatant
    for col in mag_plate.cols('1', length=sample_col):
        m300.transfer(200, col, m300.trash_container.top(), air_gap=True)

    robot.comment("Drying beads for 5 minutes. Protocol will resume \
    automatically.")
    m300.delay(minutes=5)

    robot._driver.run_flag.wait()
    mag_module.disengage()

    # transfer elution buffer
    for col in mag_plate.cols('1', length=sample_col):
        m300.pick_up_tip()
        m300.transfer(40, elution_buffer, col, new_tip='never')
        m300.mix(5, 30, col)
        m300.blow_out(col)
        m300.drop_tip()

    mag_module.engage(height=18)
    m300.delay(minutes=2)

    # transfer supernatant to new_plate
    for source, dest in zip(
            mag_plate.cols('1', length=sample_col),
            new_plate.cols('1', length=sample_col)):
        m300.transfer(40, source, dest)
