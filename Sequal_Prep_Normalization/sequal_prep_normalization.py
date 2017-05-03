from opentrons import robot, instruments, containers


plate = containers.load('96-PCR-flat', 'C1', 'plate')
pcr_plate = containers.load('96-PCR-flat', 'C2', 'pcr_plate')
trough = containers.load('trough-12row', 'A3', 'trough')
tube_rack = containers.load('tube-rack-2ml', 'C3', 'tuberack')

p50rack1 = containers.load('tiprack-200ul', 'A1', 'p50rack')
p50rack2 = containers.load('tiprack-200ul', 'A2', 'p50rack2')
p50rack3 = containers.load('tiprack-200ul', 'A2', 'p50rack2')
p50rack4 = containers.load('tiprack-200ul', 'E1', 'p50rack3')
p50rack5 = containers.load('tiprack-200ul', 'E2', 'p50rack4')
p50rack6 = containers.load('tiprack-200ul', 'E3', 'p50rack2')
trash = containers.load('point', 'D3', 'trash')

p50 = instruments.Pipette(   
        axis="a",
        max_volume=50,
        tip_racks=[p50rack1, p50rack2, p50rack3],
        trash_container=trash,
        channels=8
)
p50S = instruments.Pipette(   
        axis="b",
        max_volume=50,
        tip_racks=[p50rack4, p50rack5, p50rack6],
        trash_container=trash
)

PCR_vol = 5

BINDING_BUFFER = trough.wells('A1')
WASH_BUFFER = trough.wells('A2')
ELUTION_BUFFER = trough.wells('A3')

p50S.distribute(PCR_vol, BINDING_BUFFER, plate.wells())

p50S.transfer(
    PCR_vol, pcr_plate.wells(), plate.wells(),
    mix_after=(2, PCR_vol), new_tip='always')

p50S.delay(minutes=60)

p50.transfer(50, plate.rows(), trash)
p50.transfer(50, WASH_BUFFER, plate.rows())
p50.transfer(50, plate.rows(), trash)

p50.pick_up_tip()
for i in range(11):
    p50.transfer(
        20, ELUTION_BUFFER, plate.rows(i), mix_after=(5, 20), new_tip='never')
    p50.transfer(
        20, plate.rows(i), plate.rows(i + 1), new_tip='never')
p50.drop_tip()

p50S.transfer(20, plate.rows('1', to='8'), tube_rack.wells('A1'))
