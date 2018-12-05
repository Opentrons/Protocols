from opentrons import labware, instruments
from otcustomizers import StringSelection


def run_custom_protocol(
    tuberack_type: StringSelection(
        'opentrons-tuberack-2ml-eppendorf',
        'opentrons-tuberack-2ml-screwcap')='opentrons-tuberack-2ml-eppendorf',
    number_of_aliquots: int=5,
    aliquot_volume: float=10,
    pipette_type: StringSelection(
        'p10-Single', 'P50-Sinlge', 'p300-Single')='p10-Single',
    pipette_mount: StringSelection('left', 'right')='left',
    tip_use_strategy: StringSelection(
        'use one tip', 'new tip each time')='use one tip'
        ):

    if number_of_aliquots > 47:
        raise Exception("Number of aliquots exceeds limit. \
        Must be 47 or lower.")

    if number_of_aliquots > 23:
        tuberack = [labware.load(tuberack_type, slot)
                    for slot in ['1', '2']]
        rack_wells = [well for rack in tuberack for well in rack.wells()]
    else:
        tuberack = labware.load(tuberack_type, '1')
        rack_wells = tuberack.wells()

    sample = rack_wells[0]
    dests = rack_wells[1:1+number_of_aliquots]

    pipette_name = pipette_type.split('-')[0]
    if pipette_name == 'p10':
        tiprack = labware.load('tiprack-10ul', '4')
        pipette = instruments.P10_Single(
            mount=pipette_mount,
            tip_racks=[tiprack])
    else:
        tiprack = labware.load('opentrons-tiprack-300ul', '4')
        if pipette_name == 'p50':
            pipette = instruments.P50_Single(
                mount=pipette_mount,
                tip_racks=[tiprack])
        else:
            pipette = instruments.P300_Single(
                mount=pipette_mount,
                tip_racks=[tiprack])

    if tip_use_strategy == 'use one tip':
        pipette.pick_up_tip()
        for dest in dests:
            pipette.transfer(aliquot_volume, sample, dest, new_tip='never')
        pipette.drop_tip()
    else:
        for dest in dests:
            pipette.transfer(aliquot_volume, sample, dest)
