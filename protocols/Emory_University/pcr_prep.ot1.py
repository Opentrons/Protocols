from opentrons import containers, instruments

trough_1 = containers.load('trough-12row', 'A2')
trough_2 = containers.load('trough-12row', 'B2')
trough_3 = containers.load('trough-12row', 'C2')
trough_4 = containers.load('trough-12row', 'D2')
sample = containers.load('96-PCR-flat', 'E1')

target = containers.load('96-PCR-flat', 'C1')

tiprack_1 = containers.load('tiprack-10ul', 'A3')
tiprack_2 = containers.load('tiprack-10ul', 'B3')
tiprack_3 = containers.load('tiprack-10ul', 'C3')
tiprack_4 = containers.load('tiprack-10ul', 'D3')


tiprack = [tiprack_1, tiprack_2, tiprack_3, tiprack_4]

trash = containers.load('trash-box', 'E3')

p10 = instruments.Pipette(
    name='p10',
    channels=1,
    axis='b',
    max_volume=12,
    tip_racks=tiprack,
    trash_container=trash)

m10 = instruments.Pipette(
    name='m10',
    channels=8,
    axis='a',
    max_volume=10,
    tip_racks=tiprack,
    trash_container=trash)

m10.transfer(12.5, trough_1['A1'], target.rows())

m10.transfer(0.25, trough_2.rows(), target.rows(), new_tip='always')

m10.transfer(0.25, trough_3.rows(), target.rows(), new_tip='always')

p10.distribute(0.15, trough_4.rows(0, length=8), target.cols('A', length=8),
               new_tip='always')

for col_num in range(len(target.cols())):
    p10.transfer(11.5, sample.wells(col_num), target.cols(col_num),
                 mix_after=(5, 11.5), new_tip='always')
