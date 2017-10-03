from opentrons import containers, instruments

containers.create(
    '2x3_plate',                   # name of you container
    grid=(2, 3),                   # specify amount of (columns, rows)
    spacing=(39, 24.9),            # distances (mm) between each (column, row)
    diameter=35.58,                # diameter (mm) of each well on the plate
    depth=16.5                     # depth (mm) of each well on the plate
)

culture_plate = containers.load('2x3_plate', 'C1')
trash = containers.load('trash-box', 'A3')
p1000rack1 = containers.load('tiprack-1000ul', 'A1')
p1000rack2 = containers.load('tiprack-1000ul', 'A2')
trough = containers.load('trough-12row', 'C2')

p1000 = instruments.Pipette(
    name="p1000",
    axis="a",
    min_volume=100,
    max_volume=1000,
    trash_container=trash,
    tip_racks=[p1000rack1, p1000rack2]
)

PBS_wash = trough['A1']
wash_volume = 6000
culture_medium = trough['A2']
dest_wells = [
    w.bottom(1, radius=1) for w in culture_plate.wells('A1', to='B3')]

p1000.transfer(
    wash_volume,
    dest_wells,
    trash,
    new_tip="always"
)
p1000.transfer(
    wash_volume,
    PBS_wash,
    dest_wells,
    new_tip="always"
)
p1000.transfer(
    wash_volume,
    dest_wells,
    trash,
    new_tip="always"
)
p1000.transfer(
    wash_volume,
    culture_medium,
    dest_wells,
    new_tip="always"
)
