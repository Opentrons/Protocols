from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nextera DNA Flex NGS Library Prep: Cleanup Libraries \
Part 1/2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_name = 'thermofisherscientific_96_deepwellplate_800ul'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=27,
        volume=800
    )

# load labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'PCR rxn plate', share=True)
deep_plate = labware.load(deep_name, '2', 'new midi plate')
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '3', 'reagent reservoir')
slots50 = [str(slot) for slot in range(4, 8)]
tips50 = [labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots50]
slots300 = [str(slot) for slot in range(8, 12)]
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots300]

# reagents
spb = res12.wells(0)
nuc_free_water = res12.wells(1)


def run_custom_protocol(
        p50_type: StringSelection('single', 'multi') = 'single',
        p300_type: StringSelection('single', 'multi') = 'single',
        p50_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('right', 'left') = 'right',
        DNA_type: StringSelection(
            'standard DNA', 'small PCR amplicon') = 'standard DNA',
        number_of_samples_to_process: int = 96
):
    # check:
    if p50_mount == p300_mount:
        raise Exception('Input different mounts for P50 and P300 multi-channel \
pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
1 and 96).')

    # pipettes
    num_cols = math.ceil(number_of_samples_to_process/8)

    if p50_type == 'multi':
        pip50 = instruments.P50_Multi(mount=p50_mount, tip_racks=tips50)
        [mag_samples50, deep_samples50] = [
            plate.rows('A')[:num_cols] for plate in [mag_plate, deep_plate]]
    else:
        pip50 = instruments.P50_Single(mount=p50_mount, tip_racks=tips50)
        [mag_samples50, deep_samples50] = [
            plate.wells()[:number_of_samples_to_process]
            for plate in [mag_plate, deep_plate]
        ]
    if p300_type == 'multi':
        pip300 = instruments.P300_Multi(mount=p300_mount, tip_racks=tips300)
        [mag_samples300, deep_samples300] = [
            plate.rows('A')[:num_cols] for plate in [mag_plate, deep_plate]]

    else:
        pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)
        [mag_samples300, deep_samples300] = [
            plate.wells()[:number_of_samples_to_process]
            for plate in [mag_plate, deep_plate]
        ]

    def slot_parse(slots):
        slot_str = ''
        for i, s in enumerate(slots):
            if i < len(slots)-1:
                slot_str += s + ', '
            else:
                slot_str += s
        return slot_str

    slot_str50 = slot_parse(slots50)
    slot_str300 = slot_parse(slots300)

    tip50_max = len(tips50)*12 if p50_type == 'multi' else len(tips50)*96
    tip300_max = len(tips300)*12 if p300_type == 'multi' else len(tips300)*96
    tip50_count = 0
    tip300_count = 0

    def pick_up(pip):
        nonlocal tip50_count
        nonlocal tip300_count

        if pip == 'pip50':
            if tip50_count == tip50_max:
                robot.pause('Replace 300ul tipracks in slots \
' + slot_str50 + ' before resuming.')
                pip50.reset()
                tip50_count = 0
            pip50.pick_up_tip()
            tip50_count += 1
        else:
            if tip300_count == tip300_max:
                robot.pause('Replace 300ul tipracks in slots \
' + slot_str300 + ' before resuming.')
                pip300.reset()
                tip300_count = 0
            pip300.pick_up_tip()
            tip300_count += 1

    if magdeck.status == 'disengaged':
        magdeck.engage(height=18)
    pip50.delay(minutes=5)

    # transfer supernatant from PCR plate to new deepwell plate
    for source, dest in zip(mag_samples50, deep_samples50):
        pick_up('pip50')
        pip50.transfer(45, source, dest, new_tip='never')
        pip50.blow_out()
        pip50.drop_tip()

    # mix and distribute SPB
    pick_up('pip300')
    pip300.mix(10, 250, spb)
    pip300.blow_out(spb.top())

    if DNA_type == 'standard DNA':
        for s in deep_samples300:
            if not pip300.tip_attached:
                pick_up('pip300')
            pip300.transfer(40, nuc_free_water, s.top(), new_tip='never')
            pip300.blow_out(s.top())
            pip300.transfer(45, spb, s, new_tip='never')
            pip300.mix(10, 100, s)
            pip300.blow_out(s.top())
            pip300.drop_tip()
        robot.comment('Seal deepwell plate in slot 2 and incubate at room \
temperature for 5 minutes. Then place on the magnetic deck and proceed with \
Cleanup Libraries: Part 2')
    else:
        for s in deep_samples300:
            if not pip300.tip_attached:
                pick_up('pip300')
            pip300.transfer(81, spb, s, new_tip='never')
            pip300.mix(10, 100, s)
            pip300.blow_out(s.top())
            pip300.drop_tip()
        robot.comment('Place on the magnetic deck and proceed with Cleanup \
Libraries: Part 2')
