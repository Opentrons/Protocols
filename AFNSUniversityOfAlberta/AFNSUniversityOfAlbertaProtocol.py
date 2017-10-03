from opentrons import containers, instruments

# volume master mix1
vol1 = 8  # can change here

# volume master mix2
vol2 = 8  # can change here

# volume cDNA
cdna_vol = 2  # can change here

# number of PCR strips you are using
num_strips = 6  # can change here, will change the below too

# tube rack holding master mix
master_mixes = containers.load('tube-rack-2ml', 'A1')

# tubes with master mix in rack

# can change position of master mix tubes here
master_mix1 = master_mixes.wells('A1')
# can change position
master_mix2 = master_mixes.wells('A2')

# 96 well plate
destination_plate = containers.load('96-PCR-flat', 'C1')

# PCR strips with cDNA
pcr_strips = containers.load('PCR-strip-tall', 'E1')

# tip rack for p10 pipettes
tip10_rack = containers.load('tiprack-10ul', 'A2')
tip10_rack2 = containers.load('tiprack-10ul', 'A3')

# trash to dispose of tips
trash = containers.load('point', 'C2', 'trash')

# p10 (1 - 10 uL) (single)
p10single = instruments.Pipette(
    axis='b',
    name='p10single',
    max_volume=10,
    min_volume=1,
    channels=1,
    trash_container=trash,
    tip_racks=[tip10_rack])

# p10 (1 - 10 uL) (multi)
p10multi = instruments.Pipette(
    axis='a',
    name='p10multi',
    max_volume=10,
    min_volume=1,
    channels=8,
    trash_container=trash,
    tip_racks=[tip10_rack2])

# set rows of 96 well plate that get each mix
# 1 to 6 as written, will change based on num_strips
mix1_rows = [row for row in destination_plate.rows('1', length=num_strips)]
# 7 to 12 as written, will change based on num_strips
mix2_rows = [
    row
    for row
    in destination_plate.rows(12 - num_strips, length=num_strips)]

# pcr strips location
strips = pcr_strips.rows('1', length=num_strips)

# transfer master mix1 to 96 plate
for row in range(0, num_strips):
    p10single.transfer(vol1, master_mix1, mix1_rows[row], new_tip='once')

# transfer master mix2 to 96 plate
for row in range(0, num_strips):
    p10single.transfer(vol2, master_mix2, mix2_rows[row], new_tip='once')

# transfer cDNA from strips to both designated rows of 96 well plate
for row in range(0, num_strips):
    # cDNA to first designated row
    p10multi.transfer(cdna_vol, strips[row], destination_plate.rows(row))
    # cDNA to second designated row
    p10multi.transfer(
        cdna_vol, strips[row], destination_plate.rows(row + num_strips))
