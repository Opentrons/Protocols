from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nextera DNA Flex NGS Library Prep: Amplify Tagmented DNA',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'reaction plate', share=True)
tuberack = labware.load(
    'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
    '2',
    'reagent tuberack'
)
liquid_waste = labware.load(
    'agilent_1_reservoir_290ml', '4', 'liquid waste').wells(0).top()
tips50 = labware.load('opentrons_96_tiprack_300ul', '5')
tips300 = labware.load('opentrons_96_tiprack_300ul', '6')

# reagents
mm = tuberack.wells('A1')
epm = tuberack.wells('B1')
nuc_free_water = tuberack.wells('C1')


def run_custom_protocol(
        p300_type: StringSelection('single', 'multi') = 'single',
        p50_single_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples_to_process: int = 24
):
    # check:
    if p50_single_mount == p300_mount:
        raise Exception('Input different mounts for P50 and P300 multi-channel \
pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
1 and 96).')

    num_cols = math.ceil(number_of_samples_to_process/8)

    # pipettes
    p50 = instruments.P50_Single(mount=p50_single_mount, tip_racks=[tips50])
    samples50 = mag_plate.wells()[:number_of_samples_to_process]

    if p300_type == 'multi':
        pip300 = instruments.P300_Multi(mount=p300_mount, tip_racks=[tips300])
        samples300 = mag_plate.rows('A')[:num_cols]
    else:
        pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=[tips300])
        samples300 = mag_plate.wells()[:number_of_samples_to_process]

    magdeck.engage(height=18)

    # create mastermix
    pip = p50 if p300_type == 'multi' else pip300
    vol_epm = 22*number_of_samples_to_process
    vol_nuc_free_water = 22*number_of_samples_to_process
    pip.pick_up_tip()
    for i, (vol, reagent) in enumerate(
            zip([vol_nuc_free_water, vol_epm], [nuc_free_water, epm])):
        pip.transfer(vol, reagent, mm, new_tip='never')
        pip.blow_out()
    pip.mix(10, 40, mm)
    pip.blow_out(mm.top())

    # remove supernatant
    for s in samples300:
        if not pip300.tip_attached:
            pip300.pick_up_tip()
        pip300.transfer(300, s, liquid_waste, new_tip='never')
        pip300.blow_out()
        pip300.drop_tip()

    magdeck.disengage()

    # distribute mastermix
    for s in samples50:
        if not p50.tip_attached:
            p50.pick_up_tip()
        p50.transfer(40, mm, s, new_tip='never')
        p50.mix(10, 30, s)
        p50.blow_out()
        p50.drop_tip()

    robot.comment('Add the appropriate index adapters to each sample and mix. \
Seal the plate, centrifuge, and run the BLT PCR program.')
