from opentrons import labware, instruments

# number of samples
num_samples = 8  # change here

# tube rack holding reagents
reagents = labware.load('tube-rack-2ml', '3')

# reagent locations
water = reagents['A1']  # can change location here
mastermix = reagents['A2']  # change here

# 96 well plate
primer_plate = labware.load('96-deep-well', '4')

# tip racks for p10 and p50 pipette
tip10_rack = labware.load('tiprack-10ul', '1')
tip200_rack = labware.load('tiprack-200ul', '2')

# PCR strips
pcr_strips = labware.load('PCR-strip-tall', '5')

# p10 (1 - 10 uL) (single)
p10single = instruments.P10_Single(
    mount='right',
    tip_racks=[tip10_rack])

# p50 (5 - 50 uL) (multi)
p50multi = instruments.Pipette(
    mount='left',
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tip200_rack])

tuberange = [tube for tube in range(0, num_samples)]

templates = [tube for row in reagents.rows('B', to='D') for tube in row]

# list of primers
primers = []

for primer in range(0, num_samples*2, 2):
    primers.append(primer_plate.wells(primer, length=2))

# pcr tubes in strips
pcr_tubes = [tube for tube in pcr_strips.wells(length=num_samples)]

# Transfer 7 uL of H2O from tube A1 into each PCR tube (PCR strip).
p10single.transfer(7, water, pcr_tubes, new_tip='once')

# Transfer 1 uL of each Primer1 and Primer2 from the first two wells of plate
# to the first PCR tube (PCR strip),
# Primer3 and Primer 4 into the second PCR tube and so on
for tube in tuberange:
    p10single.transfer(1, primers[tube], pcr_tubes[tube], new_tip='always')

# Transfer 1 uL Template from the tube B1 to PCR tube 1,
# template from tube B2 into PCR tube 2 and so on
for tube in tuberange:
    p10single.transfer(1, templates[tube], pcr_tubes[tube], new_tip='always')

# Transfer 10 uL of PCR MasterMix from tube A2 into each PCR tube.
p10single.transfer(10, mastermix, pcr_tubes, new_tip='always')
