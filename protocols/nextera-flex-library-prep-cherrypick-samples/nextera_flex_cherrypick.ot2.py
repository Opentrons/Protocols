from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Nextera DNA Flex NGS Library Prep: Cherrypick Samples',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create source plate
plate_name = 'olympus_96_wellplate_200ul_pcr'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.6,
        depth=14.5,
        volume=200
    )

# load labware
source_plates = {}
for i in range(9):
    slot = str(i+1)
    source_plates[slot] = labware.load(
        plate_name, slot, 'source plate ' + slot)
destination_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '10', 'destination_plate')
tiprack = labware.load('opentrons_96_tiprack_300ul', '11')

example_csv = """source plate, source well, destination well
1, A1, A1
1, H2, B1
5, A3, C1
"""


def run_custom_protocol(
        pipette_type: StringSelection(
            'P50 Single-channel',
            'P300 Single-channel') = 'P50 Single-channel',
        pipette_mount: StringSelection('left', 'right') = 'left',
        cherrypicking_CSV: FileInput = example_csv,
        volume_to_cherrypick_in_ul: float = 30,
        starting_tip_position: str = 'A1'
):
    # pipette
    if pipette_type.split()[0] == 'P50':
        pip = instruments.P50_Single(mount=pipette_mount, tip_racks=[tiprack])
        if volume_to_cherrypick_in_ul < 5:
            raise Exception('Cannot accommodate volumes < 5ul with P50')
    else:
        pip = instruments.P300_single(mount=pipette_mount, tip_racks=[tiprack])
        if volume_to_cherrypick_in_ul < 30:
            raise Exception('Cannot accommodate volumes < 30ul with P300')

    pip.start_at_tip(tiprack.wells(starting_tip_position))
    all_wells = [child.get_name() for child in tiprack.get_all_children()]
    if starting_tip_position not in all_wells:
        raise Exception('Invalid starting tip (must be in A1-H12)')
    tip_count = all_wells.index(starting_tip_position)

    def pick_up():
        nonlocal tip_count

        if tip_count == 96:
            robot.pause('Refill 300ul tiprack in slot 11 before resuming.')
            pip.reset()
            tip_count = 0
            pip.start_at_tip(tiprack.wells('A1'))
        tip_count += 1
        pip.pick_up_tip()

    # parse CSV
    data = [
        [val.strip() for val in line.split(',')]
        for line in example_csv.splitlines() if line][1:]

    for trans in data:
        [s_plate, s_well, d_well] = [val for val in trans]
        if s_plate not in [key for key in source_plates]:
            raise Exception('Invalid source plate: ' + s_plate)
        if s_well not in all_wells:
            raise Exception('Invalid source well: ' + s_well)
        if d_well not in all_wells:
            raise Exception('Invlaid destination well: ' + d_well)

        pick_up()
        dest = destination_plate.wells(d_well)
        pip.transfer(
            volume_to_cherrypick_in_ul,
            source_plates[s_plate].wells(s_well),
            dest,
            new_tip='never'
        )
        pip.blow_out(dest.top(-2))
        pip.drop_tip()
