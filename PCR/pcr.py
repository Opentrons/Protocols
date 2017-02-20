from opentrons import containers, instruments


p10rack = containers.load('tiprack-10ul', 'E1', 'p10-rack')
p200rack = containers.load('tiprack-200ul', 'A1', 'p200-rack')
source_tubes = containers.load('tube-rack-2ml', 'C1', 'tube rack')
dna_tubes = containers.load('tube-rack-2ml', 'C1', 'tube rack')

output = containers.load('96-PCR-flat', 'B2', 'output')
trash = containers.load('point', 'D2', 'trash')

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[p10rack],
    max_volume=10,
    axis="a"
)

p200 = instruments.Pipette(
    name="p200",
    trash_container=trash,
    tip_racks=[p200rack],
    max_volume=200,
    axis="b"
)

total_volume = 25
DNA_volumes = [1, 2, 3, 4, 5.5, 5]
num_pcr_samples = len(DNA_volumes)
DNA_sources = dna_tubes.wells(0, length=num_pcr_samples)

mix_location = source_tubes.wells('A1')
water_source = source_tubes.wells('C2')
sources = {
    'B1': 3,  # uL per PCR well
    'C1': 2.5,
    'D1': 2.5,
    'A2': 2,
    'B2': 2
}
sources_total_vol = sum(sources.values())

for name, vol in sources.items():
    p200.transfer(
        vol * (num_pcr_samples + 1),
        source_tubes.wells(name),
        mix_location)

p10.distribute(
    sources_total_vol,
    mix_location,
    output.wells('A1', length=num_pcr_samples))

p10.transfer(
    DNA_volumes,
    DNA_sources,
    output.wells('A1', length=num_pcr_samples),
    new_tip='always')

water_volumes = [total_volume - v - sources_total_vol for v in DNA_volumes]
p10.distribute(
    water_volumes,
    water_source,
    output.wells('A1', length=num_pcr_samples),
    new_tip='always')
