from opentrons import robot, containers, instruments

p10rack = containers.load(
    'tiprack-10ul',  # container type
    'E1',             # slot
    'p10-rack'         # user-defined name, optional for now
)
p200rack = containers.load(
	'tiprack-200ul',
	'A1',
	'p200-rack'
)
tuberack = containers.load(
    'tube-rack-2ml',
    'C1',
    'tube rack'
)
output = containers.load(
    '96-PCR-flat',
    'B2',
    'output'
)
trash = containers.load(
    'point',
    'D2',
    'trash'
)

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[p10rack],
    min_volume=1, # actual minimum volume of the pipette
    max_volume=10,
    axis="a",
    channels=1 # 1 o
)
p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20, # actual minimum volume of the pipette
    max_volume=200,
    axis="b",
    channels=1 # 1 o
)


# establish locations and volumes

samples = 6
total_volume = 25

DNA_local = tuberack['A1']
DNA_volume = 3

enzyme_local = tuberack['B1']
enzyme_volume = 3
enzyme_total = enzyme_volume*total_volume

buffer_local = tuberack['C1']
buffer_volume = 2.5

dNTP_local = tuberack['D1']
dNTP_volume = 2.5

fprimer_local = tuberack['A2']
fprimer_volume = 2

rprimer_local = tuberack['B2']
rprimer_volume = 2

water_local = tuberack['C2']
water_volume = 10 # total_volume - DNA_volume - enzyme_volume - buffer_volume - dNTP_volume - fprimer_volume - rprimer_volume

# Master Mix Location
MM_local = tuberack['D2']
MM_volume = total_volume - DNA_volume

# create master mix
p200.pick_up_tip().aspirate((enzyme_total), enzyme_local).dispense(MM_local).drop_tip()
p200.pick_up_tip().aspirate((buffer_volume*samples), buffer_local).dispense(MM_local).drop_tip()
p200.pick_up_tip().aspirate((dNTP_volume*samples), dNTP_local).dispense(MM_local).drop_tip()
p200.pick_up_tip().aspirate((fprimer_volume*samples), fprimer_local).dispense(MM_local).drop_tip()
p200.pick_up_tip().aspirate((rprimer_volume*samples), rprimer_local).dispense(MM_local).drop_tip()
p200.pick_up_tip().aspirate((water_volume*samples), water_local).dispense(MM_local).drop_tip()

# distribute master mix
p200.pick_up_tip()
for i in range(samples):
    p200.aspirate(MM_volume, MM_local).dispense(output[i])
p200.drop_tip()


# add DNA
for i in range(samples):
	p10.pick_up_tip().aspirate(DNA_volume, DNA_local).dispense(output[i]).drop_tip()