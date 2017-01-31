from opentrons import containers, instruments

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

# initial concentrations
buffer_initial = 10  # 10X
vector_initial = .005  # ug/uL
insert_initial = .0375

# final concentrations
buffer_final = 1  # 1X
vector_final = .01  # .05 ug/uL
insert_final = .0375  # .375 ug/uL

reaction_vol = 20

# single sample volumes
buffer_vol = (buffer_final * reaction_vol) / (buffer_initial)
vector_vol = (vector_final * 1) / (vector_initial)
insert_vol = (insert_final * 1) / (insert_initial)
ligase_vol = 1
water_vol = reaction_vol - (buffer_vol + vector_vol + insert_vol + ligase_vol)

if water_vol < 0:
    raise RuntimeWarning(
        'Volumes add up to more than {} uL'.format(reaction_vol))

p10.transfer(water_vol, tuberack['D1'], tuberack['B2'])
p10.transfer(buffer_vol, tuberack['A1'], tuberack['B2'])
p10.transfer(vector_vol, tuberack['B1'], tuberack['B2'])
p10.transfer(insert_vol, tuberack['C1'], tuberack['B2'])

# resuspend and add ligase
p10.transfer(
    ligase_vol,
    tuberack['A2'],
    tuberack['B2'],
    mix_before=(3, 10),
    mix_after=(3, 10),
    touch_tip=True
)
