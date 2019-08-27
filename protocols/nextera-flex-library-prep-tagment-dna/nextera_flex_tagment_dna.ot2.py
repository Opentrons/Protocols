from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nextera DNA Flex NGS Library Prep: Tagment DNA',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware and modules
rxn_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'tagmentation reaction plate')
tuberack = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '2',
    'reagent tuberack'
)

# reagents
mm = tuberack.wells('A1')
blt = tuberack.wells('B1')
tb1 = tuberack.wells('C1')


def run_custom_protocol(
        p50_single_mount: StringSelection('left', 'right') = 'left',
        using_p50_multi: StringSelection('no', 'yes') = 'no',
        p50_multi_mount_if_applicable: StringSelection(
            'right', 'left') = 'right',
        number_of_samples_to_process: int = 24
):
    # check:
    if (
        using_p50_multi == 'yes'
        and p50_single_mount == p50_multi_mount_if_applicable
    ):
        raise Exception('Input different mounts for P50 and P300 multi-channel \
pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
1 and 96).')

    samples = rxn_plate.wells()[:number_of_samples_to_process]

    # pipettes
    slots = ['4', '5'] if number_of_samples_to_process > 94 else ['4']
    tips50s = [
        labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots]
    p50 = instruments.P50_Single(mount=p50_single_mount, tip_racks=tips50s)

    # create mastermix
    vol_blt = 11*number_of_samples_to_process
    vol_tb1 = 11*number_of_samples_to_process
    for i, (vol, reagent) in enumerate(zip([vol_blt, vol_tb1], [blt, tb1])):
        p50.pick_up_tip()
        p50.transfer(vol, reagent, mm, new_tip='never')
        p50.blow_out()
        if i == 0:
            p50.drop_tip()
    p50.mix(10, 40, mm)
    p50.blow_out(mm.top())

    if using_p50_multi == 'no':
        for s in samples:
            if not p50.tip_attached:
                p50.pick_up_tip()
            p50.transfer(20, mm, s, new_tip='never')
            p50.mix(10, 20, s)
            p50.blow_out(s.top())
            p50.drop_tip()

    else:
        strips = labware.load(
            'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
            '3',
            'mastermix strip rack'
        )
        tips50m = labware.load('opentrons_96_tiprack_300ul', '6')
        m50 = instruments.P50_Multi(
            mount=p50_multi_mount_if_applicable, tip_racks=[tips50m])
        num_cols = math.ceil(number_of_samples_to_process/8)
        samples_multi = rxn_plate.rows('A')[:num_cols]

        # transfer mm to strip
        t_vol = (vol_blt+vol_tb1)/8
        for s in strips.columns('1'):
            p50.transfer(t_vol, mm, s, new_tip='never')
            p50.blow_out(s)
        p50.drop_tip()

        # distribute mm to sample columns
        mm_source = strips.columns('1')[0]
        for s in samples_multi:
            m50.pick_up_tip()
            m50.transfer(20, mm_source, s, new_tip='never')
            m50.mix(10, 20, s)
            m50.blow_out(s.top())
            m50.drop_tip()

    robot.comment('Seal the plate and thermocycle running the TAG program.')
