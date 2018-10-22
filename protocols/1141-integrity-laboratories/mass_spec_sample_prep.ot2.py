from opentrons import labware, instruments
from otcustomizers import StringSelection

tipracks = {'p10': 'tiprack-10ul', 'p50': 'opentrons-tiprack-300ul',
            'p300': 'opentrons-tiprack-300ul', 'p1000': 'tiprack-1000ul'}


def run_custom_protocol(
        sample_container: StringSelection(
            'opentrons-tuberack-15ml', 'opentrons-tuberack-2ml-eppendorf',
            'opentrons-tuberack-2ml-screwcap', 'PCR-strip-tall', '96-flat',
            '96-deep-square')='opentrons-tuberack-15ml',
        sample_number: int=24,
        destination_container: StringSelection(
            'opentrons-tuberack-15ml', 'opentrons-tuberack-2ml-eppendorf',
            'opentrons-tuberack-2ml-screwcap', 'PCR-strip-tall', '96-flat',
            '96-deep-square')='opentrons-tuberack-15ml',
        destination_number: int=3,
        transfer_volume: float=300,
        destination_start_well: str='B1',
        strategy: StringSelection('row', 'column')='row',
        pipette_type: StringSelection('p10', 'p50', 'p300', 'p1000')='p300'
        ):

    output_plates = [
        labware.load(destination_container, slot)
        for slot in ['2', '3', '4', '5', '6', '7', '8', '9', '10']][
        :destination_number]

    sample_plate = labware.load(sample_container, '1')

    tiprack = labware.load(tipracks[pipette_type], '11')

    if pipette_type == 'p10':
        pipette = instruments.P10_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p50':
        pipette = instruments.P50_Single(
            mount='left',
            tip_racks=[tiprack])
    elif pipette_type == 'p300':
        pipette = instruments.P300_Single(
            mount='left',
            tip_racks=[tiprack])
    else:
        pipette_type.instruments.P1000_Single(
            mount='left',
            tip_racks=[tiprack])

    if strategy == 'column':
        samples = sample_plate.wells('A1', length=sample_number)
        loc_names = [well.get_name() for well in output_plates[0].wells()]
        index = loc_names.index(destination_start_well)
        dests = [[plate.wells(i) for plate in output_plates] for i in range(
            index, index+destination_number)]
    else:
        samples = [well for row in sample_plate.rows() for well in row][
            :sample_number]
        loc_names = [well.get_name()
                     for row in output_plates[0].rows() for well in row]
        index = loc_names.index(destination_start_well)
        dests = [[plate.wells(i) for plate in output_plates]
                 for i in loc_names[index:index+destination_number]]

    for sample, dest in zip(samples, dests):
        pipette.transfer(transfer_volume, sample, dest)
