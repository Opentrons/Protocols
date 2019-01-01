from opentrons import instruments, labware, robot
from otcustomizers import StringSelection

metadata = {
 'protocolName': 'Fluorescence Assay Specific Enzyme Concentration',
 'author': 'Laura <protocols@opentrons.com>',
 'source': 'Custom Protocol Request'
}


def run_custom_protocol(pipette_type: StringSelection(
        'p10-single', 'p50-multi')='p10-single',
        mm_volume: int=10,
        mm_location: str='1',
        titrator_location: str='A3',
        titrator_volume: int=10,
        dilution_volume: int=10,
        detection_reagent_volume: int=5,
        incubation_time: int=90):

    experiment_plate = labware.load('384-plate', '3')

    if pipette_type == 'p10-single':
        tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
        tiprack = labware.load('tiprack-10ul', '2')
        tiprack2 = labware.load('tiprack-10ul', '5')
        pipette = instruments.P10_Single(
            mount='right', tip_racks=[tiprack, tiprack2])

        mm_c = tuberack.wells('A' + mm_location)
        mm_d = tuberack.wells('B' + mm_location)
        mm_e = tuberack.wells('C' + mm_location)

        pipette.transfer(
            mm_volume,
            mm_c,
            experiment_plate.rows('I'),
            new_tip='once')
        pipette.transfer(
            mm_volume,
            mm_c,
            experiment_plate.rows('K'),
            new_tip='once'
        )
        pipette.transfer(
            mm_volume,
            mm_d,
            experiment_plate.rows('M'),
            new_tip='once'
        )
        pipette.transfer(
            mm_volume,
            mm_e,
            experiment_plate.rows('O'),
            new_tip='once'
        )
        # transfer titrator
        pipette.transfer(
            titrator_volume,
            tuberack.wells(titrator_location),
            experiment_plate.columns('1').rows('I', 'K', 'M', 'O'),
            new_tip='once'
        )

        # titrator dilution
        pipette.transfer(
            titrator_volume,
            experiment_plate.rows('I')[0],
            experiment_plate.rows('I')[1::],
            new_tip='once',
            mix_after=(3, titrator_volume))

        pipette.transfer(
            titrator_volume,
            experiment_plate.rows('K')[0],
            experiment_plate.rows('K')[1::],
            new_tip='once',
            mix_after=(3, titrator_volume))

        pipette.transfer(
            titrator_volume,
            experiment_plate.rows('M')[0],
            experiment_plate.rows('M')[1::],
            new_tip='once',
            mix_after=(3, titrator_volume))

        pipette.transfer(
            titrator_volume,
            experiment_plate.rows('O')[0],
            experiment_plate.rows('O')[1::],
            new_tip='once',
            mix_after=(3, titrator_volume))

    else:
        plate = labware.load('96-flat', '1')
        tiprack = labware.load('opentrons-tiprack-300ul', '2')
        tiprack2 = labware.load('opentrons-tiprack-300ul', '5')
        pipette = instruments.P50_Multi(
            mount='left', tip_racks=[tiprack, tiprack2])
        pipette.transfer(
            mm_volume,
            plate.columns(mm_location)[0],
            experiment_plate.rows('A'),
            new_tip='once')
        pipette.transfer(
            titrator_volume,
            plate.columns(titrator_location)[0],
            experiment_plate.rows('A')[0],
            new_tip='once',
            mix_after=(3, titrator_volume))
        pipette.transfer(
            dilution_volume,
            experiment_plate.rows('A')[0],
            experiment_plate.rows('A')[1::],
            new_tip='once',
            mix_after=(3, dilution_volume))

    robot.home()

    # workaround delay error if longer than 40 minutes
    if incubation_time > 40:
        for n in range(incubation_time):
            pipette.delay(minutes=n)
    else:
        pipette.delay(minutes=incubation_time)

    if pipette_type == 'p10-single':
        pipette.transfer(
            detection_reagent_volume,
            tuberack.wells('A4'),
            experiment_plate.columns().rows('I', 'K', 'M', 'O'),
            new_tip='always',
            mix_after=(3, detection_reagent_volume))
    else:
        pipette.transfer(
            detection_reagent_volume,
            plate.columns('5')[0],
            experiment_plate.rows('A'),
            new_tip='always',
            mix_after=(3, detection_reagent_volume))

    robot.home()
