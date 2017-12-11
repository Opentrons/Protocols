from opentrons import containers, instruments
import math


"""
Column A
"""
tiprack1 = containers.load('tiprack-10ul', 'A1')

inputPlate1 = containers.load('96-deep-well', 'A2')

"""
Column B
"""
inputPlate2 = containers.load('96-deep-well', 'B2')

tiprack2 = containers.load('tiprack-10ul', 'B1')
"""
Column C
"""
inputPlate3 = containers.load('96-deep-well', 'C2')

tiprack3 = containers.load('tiprack-10ul', 'C1')
"""
Column D
"""
outputPlate = containers.load('384-plate', 'D2')

tiprack4 = containers.load('tiprack-10ul', 'D1')

"""
Column E
"""
trough = containers.load('trough-12row', 'E2')

trash = containers.load('trash-box', 'E1')

"""
Instruments
"""

pipette = instruments.Pipette(
    axis='a',
    name='10ul Multichannel',
    max_volume=10,
    min_volume=1,
    channels=8,
    tip_racks=[tiprack1, tiprack2, tiprack3, tiprack4],
    trash_container=trash)

"""
Variable initialization
"""


def run_custom_protocol(number_of_samples: int=288):
    num_samples = number_of_samples
    plates = [inputPlate1, inputPlate2, inputPlate3]
    # Plates/Tube racks
    if (num_samples > 288):
        raise Exception(print("Error - too many samples"))

    num_output = math.ceil(num_samples/16)
    num_plates = math.ceil(num_samples/96)

    plates = plates[0:num_plates]
    master_mix = trough.wells('A1')

    alternating_wells = []

    for row in outputPlate.rows('1', to=num_output):
        alternating_wells.append(row.wells('A', length=8, step=2))
        alternating_wells.append(row.wells('B', length=8, step=2))

    # Distribute MasterMix to entire 384 plate

    pipette.transfer(3, master_mix, alternating_wells)

    for start, plate in enumerate(plates):
        end = start + 1

        pipette.transfer(
            2,
            plate.rows('1', length=6),
            list(outputPlate.cols(0)[start*6:end*6]))

        pipette.transfer(
            2,
            plate.rows('7', length=6),
            list(outputPlate.cols(1)[start*6:end*6]))
        # Can we incorporate num samples?
