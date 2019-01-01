from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
 'protocolName': 'Fluorescence Assay Setup',
 'author': 'Laura <protocols@opentrons.com>',
 'source': 'Custom Protocol Request'
 }


def run_custom_protocol(pipette_type: StringSelection(
        'p10-single', 'p50-multi')='p10-single',
        mm_volume: int=10,
        donor_sub_volume: int=10,
        start: str='A',
        end: str='A',
        starting_well: int=0,
        ending_well: int=12,
        mm_loc: str='A1',
        donor_loc: str='B1'):

    experiment_plate = labware.load('384-plate', '3')

    if pipette_type == 'p10-single':
        tiprack = labware.load('tiprack-10ul', '2')
        tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
        source1 = tuberack.wells(mm_loc)
        source2 = tuberack.wells(donor_loc)
        destination = experiment_plate.rows(
            start, to=end)[starting_well:ending_well]
        pipette = instruments.P10_Single(mount='right', tip_racks=[tiprack])
    else:
        tiprack = labware.load('opentrons-tiprack-300ul', '2')
        plate = labware.load('96-flat', '1')
        source1 = plate.columns(mm_loc)
        source2 = plate.columns(donor_loc)
        destination = experiment_plate.columns(
            start, to=end)[starting_well:ending_well]
        pipette = instruments.P50_Multi(mount='left', tip_racks=[tiprack])

    pipette.pick_up_tip()
    pipette.distribute(
        mm_volume,
        source1,
        destination,
        new_tip='never')
    pipette.drop_tip()

    pipette.distribute(
        donor_sub_volume,
        source2,
        destination,
        new_tip='always',
        mix_after=(3, donor_sub_volume))

    robot.home()
