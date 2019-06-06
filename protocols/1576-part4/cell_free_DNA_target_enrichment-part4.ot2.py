from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 4',
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
    tuberack = labware.load('opentrons-aluminum-block-2ml-screwcap', '8')
    tipracks = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['2', '3', '6', '9', '10', '11']]

    # instrument setup
    m50 = instruments.P50_Multi(
        mount='left',
        tip_racks=tipracks)
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=tipracks)

    # reagent setup
    pcr_mastermix = tuberack.wells('A1')
    primer_mix = tuberack.wells('B1')
    mastermix = trough.wells('A12')
    cleanup_beads = trough.wells('A1')
    ethanol = trough.wells('A3', length=2)
    nuclease_free_water = trough.wells('A4')

    temp_module.set_temperature(4)
    temp_module.wait_for_temp()

    # define sample locations
    col_num = int(number_of_samples / 8)
    sample_cols = temp_plate.cols('1', length=col_num)

    # determine master mix component volumes
    pcr_mastermix_vol = (25 * number_of_samples) * 1.05
    primer_mix_vol = (2.5 * number_of_samples) * 1.05
    volumes = [pcr_mastermix_vol, primer_mix_vol]
    components = [pcr_mastermix, primer_mix]

    # prepare master mix
    for vol, component in zip(volumes, components):
        p300.pick_up_tip()
        p300.transfer(vol, component, mastermix, new_tip='never')
        mix_vol = p300.max_volume if vol > p300.max_volume else vol
        p300.mix(10, mix_vol, mastermix)
        p300.blow_out(mastermix.top())
        p300.drop_tip()

    # distribute master mix
    m50.start_at_tip(tipracks[0].cols('2'))
    mastermix_dests = mag_plate.cols('1', length=col_num)
    m50.transfer(27.5, mastermix, mastermix_dests)

    # transfer sample library to master mix
    for sample, dest in zip(sample_cols, mastermix_dests):
        m50.transfer(22.5, sample, dest)

    robot.pause('Transfer the sample library to the pre-heated thermocycler \
(98°C) and skip to the next program. Place a clean plate on the Magnetic \
Module. Remove the plate on the Temperature Module and replace with the one \
in the Thermocycler after the program finishes. Replenish all of the tip \
racks before resuming the protocol.')

    m50.reset()
    p300.reset()

    # transfer beads to the clean plate on Magnetic Module
    mag_sample_cols = mag_plate.cols('1', length=col_num)
    m50.distribute(
        50, cleanup_beads, mag_sample_cols, blow_out=cleanup_beads.top())

    # transfer amplified library to the clean-up beads
    for sample, dest in zip(sample_cols, mag_sample_cols):
        m50.pick_up_tip()
        m50.transfer(50, sample, dest, new_tip='never')
        m50.mix(15, 50, dest)
        m50.blow_out(dest[0].top())
        m50.drop_tip()

    m50.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.engage()
    m50.delay(minutes=5)

    # remove supernatant
    for col in mag_sample_cols:
        m50.transfer(120, col, m50.trash_container.top())

    # wash plate with 80% ethanol twice
    m50.pick_up_tip()
    reuse_tip = m50.current_tip()
    for index in range(2):
        if not m50.tip_attached:
            m50.start_at_tip(reuse_tip)
            m50.pick_up_tip()
        m50.transfer(200, ethanol[index], mag_sample_cols, trash=False)
        m50.delay(seconds=30)
        for col in mag_sample_cols:
            m50.transfer(230, col, m50.trash_container.top(), trash=False)

    m50.delay(minutes=5)
    robot._driver.run_flag.wait()
    mag_module.disengage()

    # resuspend beads in nuclease-free water
    for col in mag_sample_cols:
        m50.pick_up_tip()
        m50.transfer(32.5, nuclease_free_water, col, new_tip='never')
        m50.mix(10, 25, col)
        m50.blow_out(col[0].top())
        m50.drop_tip()

    m50.delay(minutes=2)
    robot._driver.run_flag.wait()
    mag_module.engage()
    m50.delay(minutes=2)

    # transfer supernatant to new plate
    sample_dests = plate.cols('1', length=col_num)
    for sample, dest in zip(mag_sample_cols, sample_dests):
        m50.transfer(30, sample, dest)

    mag_module.disengage()
