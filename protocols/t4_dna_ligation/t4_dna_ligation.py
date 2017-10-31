from opentrons import containers, instruments

# add a 2ml tube rack
tuberack = containers.load('tube-rack-2ml', 'C1')

# add a p10 pipette, with tiprack and trash
p10rack = containers.load('tiprack-200ul', 'A1')
trash = containers.load('trash-box', 'B2')
p10 = instruments.Pipette(
    axis='b',
    max_volume=10,
    trash_container=trash,
    tip_racks=[p10rack]
)

# single sample volumes
buffer_vol = 1
vector_vol = 1.5
insert_vol = 2
ligase_vol = 1.6
water_vol = 20 - (buffer_vol + vector_vol + insert_vol + ligase_vol)

if water_vol < 0:
    raise RuntimeWarning('Volumes add up to more than 20uL')

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
