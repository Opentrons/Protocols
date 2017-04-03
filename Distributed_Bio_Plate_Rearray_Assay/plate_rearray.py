from opentrons import containers, instruments


p200rack = containers.load('tiprack-200ul','A1','p200rack')
output1 = containers.load('96-PCR-flat','C1','output1')
output2 = containers.load('96-PCR-flat','D1','output2')
input1 = containers.load('96-PCR-flat','C2','input1')
input2 = containers.load('96-PCR-flat','D2','input2')
input3 = containers.load('96-PCR-flat','C3','input3')
input4 = containers.load('96-PCR-flat','D3','input4')
trash = containers.load('point','B2','trash')

p200 = instruments.Pipette(
    name = "p200",
    axis = "b",
    min_volume = 20,
    max_volume = 200,
    trash_container=trash,
    tip_racks = [p200rack],
    channels = 1
)

source_wells = input1.wells('B11','C4','C6','D2')
output_wells = output1.wells('A1','A2','A3','A4')

p200.transfer(20, source_wells, output_wells, new_tip='always',trash=False,touch_tip=True,blow_out=True,)

source_wells1 = input2.wells('A3','D3','G5','A7','H2','F3','F2','F1','E12')
output_wells1 = output2.wells('A1','A2','A3','A4','A5','A6','A7','A8','A9')

p200.transfer(20, source_wells1, output_wells1, new_tip='never')
