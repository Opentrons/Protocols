from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 3',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        number_of_samples: StringSelection('16', '48', '96')='96'):

    number_of_samples = int(number_of_samples)

    # labware setup
    plate = labware.load('biorad-hardshell-96-PCR', '1')
    mag_module = modules.load('magdeck', '4')
    mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
    trough = labware.load('trough-12row', '5')
    temp_module = modules.load('tempdeck', '7')
    temp_plate = labware.load(
        'opentrons-aluminum-block-96-PCR-plate', '7', share=True)
    tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['8', '9', '10', '11']]
    tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
                   for slot in ['3', '6']]

    # instrument setup
    m50 = instruments.P50_Multi(
        mount='left',
        tip_racks=tipracks_50)
    m300 = instruments.P300_Multi(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    cleanup_beads = trough.wells('A1')
    elution_buffer = trough.wells('A2')
    ethanol = trough.wells('A3', length=2)

    temp_module.set_temperature(4)
    temp_module.wait_for_temp()

    # define sample locations
    col_num = int(number_of_samples / 8)
    sample_cols = temp_plate.cols('1', length=col_num)

    # transfer beads to the clean plate on Magnetic Module
    mag_sample_cols = mag_plate.cols('1', length=col_num)
    m300.distribute(
        90, cleanup_beads, mag_sample_cols, blow_out=cleanup_beads.top())

    # transfer ligation reaction to beads
    for sample, dest in zip(sample_cols, mag_sample_cols):
        m300.pick_up_tip()
        m300.transfer(100, sample, dest, new_tip='never')
        m300.mix(15, 100, dest)
        m300.blow_out(dest[0].top())
        m300.drop_tip()

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.engage()
    m300.delay(minutes=5)

    # remove supernatant
    for col in mag_sample_cols:
        m300.transfer(230, col, m300.trash_container.top())

    # wash beads with 80% ethanol twice
    m300.pick_up_tip()
    reuse_tip = m300.current_tip()
    for index in range(2):
        if not m300.tip_attached:
            m300.start_at_tip(reuse_tip)
            m300.pick_up_tip()
        m300.transfer(200, ethanol[index], mag_sample_cols, trash=False)
        m300.delay(seconds=30)
        for col in mag_sample_cols:
            m300.transfer(230, col, m300.trash_container.top(), trash=False)

    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.disengage()

    # resuspend beads in Buffer EB
    for col in mag_sample_cols:
        m50.pick_up_tip()
        m50.transfer(27, elution_buffer, col, new_tip='never')
        m50.mix(10, 20, col)
        m50.blow_out(col[0].top())
        m50.drop_tip()

    m50.delay(minutes=2)
    robot._driver.run_flag.wait()
    mag_module.engage()
    m50.delay(minutes=2)

    # transfer supernatant to new plate
    sample_dests = plate.cols('1', length=col_num)
    for sample, dest in zip(mag_sample_cols, sample_dests):
        m50.transfer(24, sample, dest)

    mag_module.disengage()
