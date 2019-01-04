from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
 'protocolName': 'Fluorescence Assay Specific Antibody Setup',
 'author': 'Laura <protocols@opentrons.com>',
 'source': 'Custom Protocol Request'
}


def run_custom_protocol(pipette_type: StringSelection(
        'p10-single', 'p50-multi')='p10-single',
        mm_volume: int=10,
        titrator_volume: int=10,
        dilution_volume: int=10):

    experiment_plate = labware.load('384-plate', '3')

    well_type = False  # Variable showing Well object not list of wells
    if pipette_type == 'p10-single':
        # Use tuberack if p10 single pipette
        tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
        master_mix = tuberack.wells('A1')
        ab_titrator = tuberack.wells('B1')
        well_type = True
        tiprack = labware.load('tiprack-10ul', '2')
        pipette = instruments.P10_Single(mount='right', tip_racks=[tiprack])
    elif pipette_type == 'p50-multi':
        # Use 96 flat if multichannel
        reagent_plate = labware.load('96-flat', '1')
        master_mix = reagent_plate.columns('1')
        ab_titrator = reagent_plate.columns('2')
        tiprack = labware.load('opentrons-tiprack-300ul', '2')
        pipette = instruments.P50_Multi(mount='left', tip_racks=[tiprack])

    if well_type:
        # If single channel, distribute in triplicate to 384 well plate
        destination = [well for col in experiment_plate.columns()
                       for well in col[0:3]]
        pipette.transfer(mm_volume, master_mix, destination, new_tip='once')
        pipette.transfer(
            titrator_volume,
            ab_titrator,
            destination[0:3],
            mix_after=(3, titrator_volume),
            new_tip='always')
        pipette.transfer(dilution_volume, destination[0:3], destination[3::])
    else:
        destination = [well for col in experiment_plate.columns()
                       for well in col[0:2]]
        pipette.transfer(mm_volume, master_mix, destination, new_tip='once')
        pipette.transfer(
            titrator_volume,
            ab_titrator,
            destination[0:2],
            mix_after=(3, titrator_volume),
            new_tip='always')
        pipette.transfer(dilution_volume, destination[0:2], destination[2::])

    robot.home()
