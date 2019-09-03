from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell Culture Cherrypick',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
flat_name = 'corning_96_wellplate_360ul_flat'
if flat_name not in labware.list():
    labware.create(
        flat_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.85,
        depth=10.76,
        volume=360
    )

# load labware
tips300 = labware.load('opentrons_96_tiprack_300ul', '1', '300ul tiprack')
destination_plate = labware.load(flat_name, '2', 'destination plate')


def run_custom_protocol(
        p300_mount: StringSelection('right', 'left') = 'right',
        volume_to_cherrypick_in_ul: float = 30,
        cherrypick_wells_separated_by_comma: str = 'B6, C1, C4, D5, E7, F8',
        number_of_source_plates: int = 6,
        tiprack_start_well: str = 'A1'
):

    # parse input
    source_well_names = [
        s.strip() for s in cherrypick_wells_separated_by_comma.split(',')]

    # checks
    if volume_to_cherrypick_in_ul < 30:
        raise Exception('P300 pipette cannot accommodate volumes less than \
30ul.')
    if number_of_source_plates > 9:
        raise Exception('Maximum of 9 source plates.')
    possible_wells = [well.get_name() for well in tips300.get_children_list()]
    if tiprack_start_well not in possible_wells:
        raise Exception('Invalid tiprack start well.')
    if len(source_well_names)*number_of_source_plates > 96:
        raise Exception('Combination of cherrypick wells and number of source \
plates will exceed capacity of destination plate.')
    for s in source_well_names:
        if s not in possible_wells:
            raise Exception('Invalid cherrypick well: ' + s)

    # labware
    source_plates = [
        labware.load(flat_name, str(slot), 'source plate ' + str(i+1))
        for i, slot in enumerate(range(3, 3+number_of_source_plates))
    ]

    # pipette
    p300 = instruments.P300_Single(mount=p300_mount, tip_racks=[tips300])
    p300.start_at_tip(tiprack_start_well)

    # perform transfers
    d_count = 0
    for plate in source_plates:
        for s in source_well_names:
            dest = destination_plate.wells()[d_count]
            p300.pick_up_tip()
            p300.transfer(
                volume_to_cherrypick_in_ul,
                plate.wells(s),
                dest,
                new_tip='never'
            )
            p300.blow_out(dest)
            p300.drop_tip()
            d_count += 1
