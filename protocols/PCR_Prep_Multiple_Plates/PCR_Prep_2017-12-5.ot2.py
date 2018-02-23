from opentrons import containers, instruments
import math


"""
Column A
"""
tiprack1 = containers.load('tiprack-10ul', '1')

inputPlate1 = containers.load('96-deep-well', '4')

"""
Column B
"""
inputPlate2 = containers.load('96-deep-well', '2')

tiprack2 = containers.load('tiprack-10ul', '5')
"""
Column C
"""
inputPlate3 = containers.load('96-deep-well', '3')

tiprack3 = containers.load('tiprack-10ul', '6')
"""
Column D
"""
outputPlate = containers.load('384-plate', '7')

tiprack4 = containers.load('tiprack-10ul', '10')

"""
Column E
"""
trough = containers.load('trough-12row', '8')

"""
Instruments
"""

p10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack1, tiprack2, tiprack3, tiprack4]
)

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

    for col in outputPlate.cols('1', to=num_output):
        alternating_wells.append(col.wells('A', length=8, step=2))
        alternating_wells.append(col.wells('B', length=8, step=2))

    # Distribute MasterMix to entire 384 plate

    p10.transfer(3, master_mix, alternating_wells)

    for start, plate in enumerate(plates):
        end = start + 1

        p10.transfer(
            2,
            plate.cols('1', length=6),
            list(outputPlate.rows(0)[start*6:end*6]))

        p10.transfer(
            2,
            plate.cols('7', length=6),
            list(outputPlate.rows(1)[start*6:end*6]))
        # Can we incorporate num samples?
