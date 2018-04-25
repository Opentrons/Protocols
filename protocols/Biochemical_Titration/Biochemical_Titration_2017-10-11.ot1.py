from opentrons import containers, instruments


"""
Step1. Transferring 20ul of DMSO into column 2-12 of 96
well plate (master plate)
Step 2. Transferring 10ul from column 1 into column 2 (1->3)
Mixing x3 continuing across the plate. Missing out column 6.
And finishing at column 11. So that c6 and 12 only have dmso in them.
Step3. Change tips . Trash, then refill tips
Step4. Transfer 5ul from master 96 to the intermediate 96 plate.
Order column 6, then 12. Then 11,10,9,8,7,5,4,3,2,1.
Dispense at the bottom of the wells Blow out
Step5. Change tips. Then add 95ul of buffer( column 2 of trough)
to add the well. In the same order (at bottom of well.

"""


"""
 Column A
"""
# trough with solutions
trough = containers.load('trough-12row', 'A1')

tiprack = containers.load('tiprack-200ul', 'A2')

tiprack2 = containers.load('tiprack-200ul', 'A3')

"""
 Column B
"""
source_plate_1 = containers.load('96-deep-well', 'B1')
source_plate_2 = containers.load('96-deep-well', 'B2')
source_plate_3 = containers.load('96-deep-well', 'B3')

"""
 Column C
"""
output_plate_4 = containers.load('96-deep-well', 'C1')
source_plate_4 = containers.load('96-deep-well', 'C3')

"""
 Column D
"""
output_plate_1 = containers.load('96-deep-well', 'D1')
output_plate_2 = containers.load('96-deep-well', 'D2')
output_plate_3 = containers.load('96-deep-well', 'D3')

"""
 Column E
"""
trash = containers.load('trash-box', 'E1')

tiprack3 = containers.load('tiprack-200ul', 'E2')

tiprack4 = containers.load('tiprack-200ul', 'E3')


p50multi = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tiprack, tiprack2, tiprack3, tiprack4],
    trash_container=trash)

DMSO = trough.wells('A1')
buffer = trough.wells('A2')

all_source_plates = [
    source_plate_1,
    source_plate_2,
    source_plate_3,
    source_plate_4]
all_output_plates = [
    output_plate_1,
    output_plate_2,
    output_plate_3,
    output_plate_4]


def run_custom_protocol(number_of_plates: int=1):

    source_plates = all_source_plates[0:number_of_plates]
    output_plates = all_output_plates[0:number_of_plates]

    for source, output in zip(source_plates, output_plates):

        DMSO_source_rows = source.wells('A6', 'A12')
        DMSO_output_rows = output.wells('A6', 'A12')

        plate_rows = list(
            source.rows('1', '2', '3', '4', '5', '7', '8', '9', '10'))
        source_rows = list(
            source.rows('2', '3', '4', '5', '7', '8', '9', '10', '11'))

        # Step 1
        p50multi.transfer(20, DMSO, source.rows('2', length=11))

        # Step 2
        p50multi.transfer(10, source_rows, plate_rows, air_gap=10)

        source_plate_rows = []
        output_plate_rows = []
        for num in range(10, -1, -1):
            if num != 5:
                source_plate_rows.append(source.rows(num)(0).bottom())
                output_plate_rows.append(output.rows(num)(0).bottom())

        # Step 3/4
        p50multi.transfer(5, DMSO_source_rows, DMSO_output_rows)
        p50multi.transfer(5, source_plate_rows, output_plate_rows)

        DMSO_source_bot = [well.bottom() for well in DMSO_source_rows]
        DMSO_output_bot = [well.bottom() for well in DMSO_output_rows]

        p50multi.transfer(95, DMSO_source_bot, DMSO_output_bot)

        p50multi.transfer(95, source_plate_rows, output_plate_rows)
