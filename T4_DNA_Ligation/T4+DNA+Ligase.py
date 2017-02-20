from opentrons import robot, containers, instruments

p10rack = containers.load('tiprack-200ul', 'A1', 'p10rack')
tuberack = containers.load('tube-rack-2ml', 'C1', 'tuberack')
trash = containers.load('point', 'B2', 'trash')

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[p10rack],
    max_volume=10,
    axis="b"
)

reaction_vol = 20

# single sample volumes
buffer_vol = 1
vector_vol = 1.5
insert_vol = 2
ligase_vol = 1.6
water_vol = reaction_vol - (buffer_vol + vector_vol + insert_vol + ligase_vol)

if water_vol < 0:
    raise RuntimeWarning(
        'Volumes add up to more than {} uL'.format(reaction_vol))

p10.transfer(water_vol, tuberack.wells('D1'), tuberack.wells('B2'))
p10.transfer(buffer_vol, tuberack.wells('A1'), tuberack.wells('B2'))
p10.transfer(vector_vol, tuberack.wells('B1'), tuberack.wells('B2'))
p10.transfer(insert_vol, tuberack.wells('C1'), tuberack.wells('B2'))

# resuspend and add ligase
p10.transfer(
    ligase_vol,
    tuberack.wells('A2'),
    tuberack.wells('B2'),
    mix_before=(3, 10),
    mix_after=(3, 10),
    touch_tip=True
)

for c in robot.commands():
    print(c)
