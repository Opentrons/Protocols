
from opentrons import containers, instruments

"""
Step1: pick up tips from a 200 ul-tip rack
Step2: Move to the Sterile Multichannel Disposable Solutions Basin
Step3: Mix cells (in Solutions Basin) up and down with multichannel pipette
Step4: Transfer 100 ul of cells in medium to a 96 well plate
(first row, A1 position)
Step5: Repeat Steps 2-4, but pipette cells in second row,
and so on untill all wells are filled with cells
Step6: Move to trash and eject tips.
"""

"""
A
"""

tiprack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('trash-box', 'A2')

"""
B
"""
solution_basin = containers.load('point', 'B1', 'solution basin')

"""
C
"""
plate_384 = containers.load('384-plate', 'C1')
plate_96 = containers.load('96-flat', 'C1')

"""
D
"""
plate_384_2 = containers.load('384-plate', 'D1')
plate_96_2 = containers.load('96-flat', 'D1')

plate_384_5 = containers.load('384-plate', 'D2')
plate_96_5 = containers.load('96-flat', 'D2')

"""
E
"""
plate_384_3 = containers.load('384-plate', 'E1')
plate_96_3 = containers.load('96-flat', 'E1')

plate_384_4 = containers.load('384-plate', 'E2')
plate_96_4 = containers.load('96-flat', 'E2')

plates_96 = [plate_96, plate_96_2,  plate_96_3, plate_96_4, plate_96_5]
plates_384 = [plate_384, plate_384_2, plate_384_3, plate_384_4, plate_384_5]


def run_custom_protocol(plate_size: int=96, number_of_plates: int=4):

    if plate_size == 96:
        plates = plates_96[0:number_of_plates]
    else:
        plates = plates_384[0:number_of_plates]

    p200 = instruments.Pipette(
        axis='a',
        name='p200multi',
        max_volume=200,
        min_volume=20,
        channels=8,
        tip_racks=[tiprack],
        trash_container=trash)

    if plate_size == 96:
        for plate in plates:
            p200.transfer(
                100,
                solution_basin,
                plate.rows(),
                mix_before=(3, 100))
    else:
        for plate in plates:
            alternating_rows = []
            for row in plate.rows():
                alternating_rows.append(row.wells('A', length=8, step=2))
                alternating_rows.append(row.wells('B', length=8, step=2))

            p200.transfer(
                50,
                solution_basin,
                alternating_rows,
                mix_before=(3, 100))
