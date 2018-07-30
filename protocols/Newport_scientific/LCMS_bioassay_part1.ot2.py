from opentrons import labware, instruments
"""
PART I: Filling the Incubation Plates
"""

# customization
sample_num = 96
reagent_row_1 = 0

# labware setup
incubation_plate = labware.load('96-PCR-tall', '1')
incubation_plate2 = labware.load('96-PCR-tall', '2')
sample_plate = labware.load('96-PCR-tall', '5')
reagent_rack = labware.load('tube-rack-2ml', '4')
tiprack = labware.load('tiprack-200ul', '7')
tiprack2 = labware.load('tiprack-200ul', '8')

buffer_loc = reagent_rack.wells('A1')
enzyme_loc = reagent_rack.wells('A2')
is_loc = reagent_rack.wells('A3')
water_loc = reagent_rack.wells('A4')
meoh_loc = reagent_rack.wells('A5')
gluc_std_loc = reagent_rack.wells('A6')
std = reagent_rack.wells('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'C1', 'C2',
                         'C3', 'C4')
naive_loc = reagent_rack.wells('C5')
QC = reagent_rack.wells('C6', 'D1', 'D2')

# Determines location of the samples in the incubation plate(s) depending on 
# the number of samples. If the number is less than or equal to 72, samples go
# into the sample plate as the reagents, starting at C1. If the number is 
# greater than 72, samples start in A1 of a second incubation plate.
sample_dest = []
sample_source = []
well_count = 0
if sample_num <= 72:
    sample_dest_plate = incubation_plate.rows[2:]
else:
    sample_dest_plate = incubation_plate2.rows()

for source_row, dest_row in zip(sample_plate.rows(), sample_dest_plate):
    for source_well, dest_well in zip(source_row, dest_row):
        if well_count < sample_num:
            sample_dest.append(dest_well)
            sample_source.append(source_well)
            well_count += 1

reagent_dest_loc = []
if sample_num <= 72:
    reagent_dest_loc = [well for well in incubation_plate.rows(0)] + [
                    well for well in incubation_plate.rows(1)[0:4]]
else:
    reagent_dest_loc = [well for well in incubation_plate.rows(reagent_row_1)]\
            + [well for well in incubation_plate.rows(reagent_row_1 + 1)[0:4]]


# Pipette setup
p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack, tiprack2])

p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack, tiprack2])


# Trasnfer buffer
p50.transfer(50, buffer_loc, reagent_dest_loc+sample_dest)

# Trasnfer enzyme
p50.transfer(40, enzyme_loc, reagent_dest_loc[1:]+sample_dest)

# Transfer internal standard
p50.transfer(20, is_loc, reagent_dest_loc+sample_dest)

# Transfer water
p50.transfer(40, water_loc, reagent_dest_loc[0])

# Transfer MeOH
p50.transfer(20, meoh_loc,
             [reagent_dest_loc[2], reagent_dest_loc[13]]+sample_dest)

# Transfer Gluc std
p50.transfer(20, gluc_std_loc, reagent_dest_loc[0:2])

# Transfer standards
p50.transfer(20, std, reagent_dest_loc[3:13], new_tip='always')

# Transfer naive solution
p300.transfer(200, naive_loc, reagent_dest_loc[0:13])

# Transfer QCs
p300.transfer(200, QC, reagent_dest_loc[13:16], new_tip='always')

# Transfer samples
for source, dest in zip(sample_source, sample_dest):
    p300.transfer(200, source, [reagent_dest_loc[15], dest])
