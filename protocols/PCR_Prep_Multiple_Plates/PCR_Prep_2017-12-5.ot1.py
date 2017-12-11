from opentrons import containers, instruments
import math

tipracks = [
    containers.load('tiprack-10ul', slot)
    for slot in ['A1', 'B1', 'C1', 'D1']]

inputPlates = [
    containers.load('96-deep-well', slot)
    for slot in ['A2', 'B2', 'C2']]

outputPlate = containers.load('384-plate', 'D2')

trough = containers.load('trough-12row', 'E2')

trash = containers.load('trash-box', 'E1')

pipette = instruments.Pipette(
    axis='a',
    max_volume=10,
    min_volume=1,
    channels=8,
    tip_racks=tipracks,
    trash_container=trash)


def run_custom_protocol(number_of_samples: int=288):
    num_samples = number_of_samples

    # Plates/Tube racks
    if (num_samples > 288):
        raise Exception(
            "Error - too many samples. " +
            "The maximum number of samples is 288")

    num_output = math.ceil(num_samples/16)
    num_plates = math.ceil(num_samples/96)

    plates = inputPlates[0:num_plates]
    master_mix = trough.wells('A1')

    alternating_wells = []

    for row in outputPlate.rows('1', to=num_output):
        alternating_wells.append(row.wells('A').bottom())
        alternating_wells.append(row.wells('B').bottom())

    # Distribute MasterMix to entire 384 plate
    pipette.transfer(3, master_mix, alternating_wells)

    for start, plate in enumerate(plates):
        end = start + 1

        for num, well in enumerate(outputPlate.cols(0)[start*6:end*6]):
            pipette.transfer(
                2,
                plate.rows(num),
                well.bottom())

        for num, well in enumerate(outputPlate.cols(1)[start*6:end*6]):
            pipette.transfer(
                2,
                plate.rows(num + 6),
                well.bottom())
    # Can we incorporate num samples?
