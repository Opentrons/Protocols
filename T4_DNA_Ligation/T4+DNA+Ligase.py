from opentrons import robot, containers, instruments

p10rack = containers.load(
    'tiprack-200ul', 
    'A1',
    'p10rack'
)
tuberack = containers.load(
    'tube-rack-2ml', 
    'C1',
    'tuberack'
)
trash = containers.load(
    'point', 
    'B2', 
    'trash')

p10 = instruments.Pipette(
    name="p10", # optional
    trash_container=trash,
    tip_racks=[p10rack],
    max_volume=10,
    min_volume=.5, # actual minimum volume of the pipette
    axis="b",
    channels=1 # 1 o
)
reaction_vol = 20 #uL
samples = 1

# locations
buffer_local = tuberack['A1']
vector_local = tuberack['B1']
insert_local = tuberack['C1']
water_local = tuberack['D1']
ligase_local = tuberack['A2']
sample_local = tuberack['B2']

# initial concentrations
buffer_initial = 10 # 10X
vector_initial = .005 # ug/uL
insert_initial = .0375

# final concentrations
buffer_final = 1 # 1X
vector_final = .01 # .05 ug/uL
insert_final = .0375 # .375 ug/uL

# single sample volumes
buffer_vol = (buffer_final*reaction_vol)/(buffer_initial) # uL
vector_vol = (vector_final*1)/(vector_initial) # uL
insert_vol = (insert_final*1)/(insert_initial) # uL
ligase_vol = 1 # per 20 uL
water_vol = reaction_vol - buffer_vol - vector_vol - insert_vol - ligase_vol # fill to 20 uL

if water_vol < 0:
    print("Volumes add up to more than 20 uL")


# add water

if water_vol <= 10:
    p10.pick_up_tip().aspirate(water_vol, water_local).dispense(sample_local).drop_tip()
else:
    water_vol = water_vol/2
    p10.pick_up_tip().aspirate(water_vol, water_local).dispense(sample_local).aspirate(water_vol, water_local).dispense(sample_local).drop_tip()

# add buffer
p10.pick_up_tip().aspirate(buffer_vol, buffer_local).dispense(sample_local).drop_tip()

# add vector
p10.pick_up_tip().aspirate(vector_vol, vector_local).dispense(sample_local).drop_tip()

# add insert
p10.pick_up_tip().aspirate(insert_vol, insert_local).dispense(sample_local).drop_tip()

# resuspend and add ligase
p10.pick_up_tip().mix(3, 10, ligase_local).aspirate(ligase_vol, ligase_local).dispense(sample_local).touch_tip()
p10.mix(3, 10, sample_local).drop_tip()




