from opentrons import robot, containers, instruments


source_tubes = containers.load('tube-rack-2ml', 'D2', 'tube rack')
dna_tubes = containers.load('tube-rack-2ml', 'C3', 'dna rack')
output = containers.load('96-PCR-flat', 'C1', 'output')

p10rack = containers.load('tiprack-10ul', 'B2', 'p10-rack')
p50rack = containers.load('tiprack-200ul', 'A1', 'p50-rack')
trash = containers.load('trash-box', 'A3')

p10 = instruments.Pipette(
    trash_container=trash,
    tip_racks=[p10rack],
    min_volume=1,
    max_volume=10,
    axis="a"
)

p50 = instruments.Pipette(
    trash_container=trash,
    tip_racks=[p50rack],
    min_volume=5,
    max_volume=50,
    axis="b"
)

total_volume = 25
DNA_volumes = [1, 2, 3, 4, 5.5, 5]
num_pcr_samples = len(DNA_volumes)
DNA_sources = dna_tubes.wells(0, length=num_pcr_samples)

mix_location = source_tubes.wells('A1')
water_source = source_tubes.wells('C2')

sources = [       #uL per PCR well
    ('B1', 3),    #enzyme -- 4
    ('C1', 2.5),  #buffer -- 5
    ('D1', 2.5),  #dNTP -- 2
    ('A2', 2),    #fprimer -- 3
    ('B2', 2)     #rprimer -- 1
]

sources_total_vol = sum([vol for _, vol in sources])

#Create Master Mix
for name, vol in sources:
    p50.transfer(
        vol * (num_pcr_samples + 1),
        source_tubes.wells(name),
        mix_location)

#Distribute Master Mix
p10.distribute(
    sources_total_vol,
    mix_location,
    output.wells('A1', length=num_pcr_samples))

#Add DNA
p10.transfer(
    DNA_volumes,
    DNA_sources,
    output.wells('A1', length=num_pcr_samples),
    new_tip='always')

#Add water
water_volumes = []
for v in DNA_volumes:
    water_volumes.append(total_volume - v - sources_total_vol)

p10.distribute(
    water_volumes,
    water_source,
    output.wells('A1', length=num_pcr_samples),
    new_tip='always')
