
from opentrons import labware, instruments

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

tiprack = labware.load('tiprack-200ul', '1')

"""
B
"""
solution_basin = labware.load('point', '2', 'solution basin')

"""
C
"""
plate_384 = labware.load('384-plate', '3', share=True)
plate_96 = labware.load('96-flat', '3', share=True)

"""
D
"""
plate_384_2 = labware.load('384-plate', '4', share=True)
plate_96_2 = labware.load('96-flat', '4', share=True)

plate_384_5 = labware.load('384-plate', '5', share=True)
plate_96_5 = labware.load('96-flat', '5', share=True)

"""
E
"""
plate_384_3 = labware.load('384-plate', '6', share=True)
plate_96_3 = labware.load('96-flat', '6', share=True)

plate_384_4 = labware.load('384-plate', '7', share=True)
plate_96_4 = labware.load('96-flat', '7', share=True)

plates_96 = [plate_96, plate_96_2,  plate_96_3, plate_96_4, plate_96_5]
plates_384 = [plate_384, plate_384_2, plate_384_3, plate_384_4, plate_384_5]


def run_custom_protocol(plate_size: int=96, number_of_plates: int=4):

    if plate_size == 96:
        plates = plates_96[0:number_of_plates]
    else:
        plates = plates_384[0:number_of_plates]

    p200 = instruments.P300_Multi(
        mount='left',
        tip_racks=[tiprack]
    )

    if plate_size == 96:
        for plate in plates:
            p200.transfer(
                100,
                solution_basin,
                plate.cols(),
                mix_before=(3, 100))
    else:
        for plate in plates:
            alternating_cols = []
            for col in plate.cols():
                alternating_rows.append(col.wells('A', length=8, step=2))
                alternating_rows.append(col.wells('B', length=8, step=2))

            p200.transfer(
                50,
                solution_basin,
                alternating_cols,
                mix_before=(3, 100))
