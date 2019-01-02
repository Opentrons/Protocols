from opentrons import instruments, labware, robot
from otcustomizers import StringSelection

metadata = {
 'protocolName': 'Fluorescence Assay Standard Curve',
 'author': 'Laura <protocols@opentrons.com>',
 'source': 'Custom Protocol Request'
}


def run_custom_protocol(pipette_type: StringSelection(
        'p10-single', 'p50-multi')='p10-single',
        standards: int=12,
        standard_volume: int=15,
        detection_reagent_volume: int=5):

    standard_plate = labware.load('384-plate', '3')

    if pipette_type == 'p10-single':
        tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
        source = tuberack.wells('A1')
        reagent = tuberack.wells('B1')
        destination = [well
                       for rows in standard_plate.rows('A', length=standards)
                       for well in rows[0:3]]
        tiprack = labware.load('tiprack-10ul', '2')
        pipette = instruments.P10_Single(mount='right', tip_racks=[tiprack])
    else:
        plate = labware.load('96-flat', '1')
        source = plate.columns('1')[0]
        reagent = plate.columns('2')[0]
        destination = [well for cols in standard_plate.columns('1', to='3')
                       for well in cols[0]]
        tiprack = labware.load('opentrons-tiprack-300ul', '2')
        pipette = instruments.P50_Multi(mount='left', tip_racks=[tiprack])

    pipette.distribute(standard_volume, source, destination, new_tip='always')
    pipette.transfer(
        detection_reagent_volume,
        reagent,
        destination,
        mix_after=(3, detection_reagent_volume),
        new_tip='always')

    robot.home()
