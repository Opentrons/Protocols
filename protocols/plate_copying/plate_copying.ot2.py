from opentrons import labware, instruments
from otcustomizers import StringSelection
# Copy contents of one plate into another

metadata = {
    'protocolName': 'Plate Copying',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

source_slot = '6'

dest_slots = ['1', '2', '3', '4', '5', '7', '8', '9']


# TODO: optimize so that you only use 1 tiprack and can use an extra container,
# when you have 96 well source + dest (384 needs 2x tipracks, 96 needs just 1x)
tip_slots = ['10', '11']

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

# TODO: customizable pipette vol
p50multi = instruments.P50_Multi(
    mount='right',
    tip_racks=tip_racks)

container_choices = [
    '96-flat', '96-PCR-tall', '96-deep-well', '384-plate']


def alternating_wells(plate, row_num):
    """
    Returns list of 2 WellSeries for the 2 possible positions of an
    8-channel pipette for a row in a 384 well plate.
    """
    return [
        plate.cols(row_num).wells(start_well, length=8, step=2)
        for start_well in ['A', 'B']
    ]


def run_custom_protocol(
        transfer_volume: float=20,
        robot_model: StringSelection('hood', 'not hood')='not hood',
        source_container: StringSelection(*container_choices)='96-flat',
        destination_container: StringSelection(*container_choices)='96-flat',
        number_of_destination_plates: int=4):

    # Load labware
    all_dest_plates = [labware.load(destination_container, slotName)
                       for slotName in dest_slots]

    source_plate = labware.load(source_container, source_slot)

    if ('384-plate' in [source_container, destination_container] and
            source_container != destination_container):
        raise Exception(
            'This protocol currently only allows 96:96 or 384:384 transfers.' +
            ' You entered "{}" and "{}"'.format(
                source_container, destination_container))

    col_count = len(all_dest_plates[0].cols())
    dest_plates = all_dest_plates[:number_of_destination_plates]

    for col_index in range(col_count):
        if destination_container == '384-plate':
            dest_wells = [[plate.cols(col_index).wells(well_index)
                          for plate in dest_plates] for well_index in range(2)]
            source_wells = [source_plate.cols(col_index).wells(well_index)
                            for well_index in range(2)]

            for source, dest in zip(source_wells, dest_wells):
                p50multi.distribute(
                    transfer_volume, source, dest, disposal_vol=0)
        else:
            dest_wells = [plate.cols(col_index) for plate in dest_plates]
            source_well = source_plate.cols(col_index)

            p50multi.distribute(
                transfer_volume, source_well, dest_wells, disposal_vol=0)
