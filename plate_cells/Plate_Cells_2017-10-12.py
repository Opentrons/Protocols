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
solution_basin = containers.load('point', 'B1')

"""
C
"""
plate_384 = containers.load('384-plate', 'C1')
plate_96 = containers.load('96-flat', 'C1')

p200 = instruments.Pipette(
    axis='a',
    name='p200multi',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=trash)


def run_protocol(plate_size: int=96):

    if plate_size == 96:
        plate = plate_96
    else:
        plate = plate_384

    if plate_size == 96:
        p200.transfer(100, solution_basin, plate.rows(), mix_before=(3, 100))
    else:
        alternating_wells = []
        for row in plate.rows():
            alternating_wells.append(row.wells('A', length=8, step=2))
            alternating_wells.append(row.wells('B', length=8, step=2))

        p200.transfer(
            100, solution_basin, alternating_wells, mix_before=(3, 100))
