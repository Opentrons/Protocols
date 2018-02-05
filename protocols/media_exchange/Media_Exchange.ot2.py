from opentrons import containers, instruments

"""
Workflow description: Step1: pick up tips from a 10 ul-tip rack
Step2: Move to the a 96 well plate (compound library, plate 1)
OR 48-deep well reservoir (compound library)
Step3: Mix solutions and pipette 5 ul of compound solutions from the first row.
Step4: Transfer 5 ul of compound solutions
to a 96 well plate (plate 2, first row, A1 position)
Step5: Move to trash and eject tips.
Step6: Repeat Steps1-5 for the remaining rows (second, third, fourth etc.)
"""

"""
A
"""
output = containers.load('96-flat', '1')


"""
B
"""
tiprack = containers.load('tiprack-10ul', '2')


"""
C
"""
plate_48 = containers.load('48-well-plate', '3', share=True)
plate_96 = containers.load('96-flat', '3', share=True)


p10single = instruments.Pipette(
    mount='right',
    name='p10single',
    max_volume=10,
    min_volume=1,
    channels=1,
    tip_racks=[tiprack])

p10multi = instruments.Pipette(
    mount='left',
    name='p10multi',
    max_volume=10,
    min_volume=1,
    channels=8,
    tip_racks=[tiprack])


def run_custom_protocol(plate_size: int=96):
    if plate_size == 96:
        plate = plate_96
        pipette = p10multi
    else:
        plate = plate_48
        pipette = p10single

    pipette.transfer(
        5, plate.columns(), output.columns(), mix_before=(3, 5), new_tip='always')


run_custom_protocol(**{'plate_size': 96})
