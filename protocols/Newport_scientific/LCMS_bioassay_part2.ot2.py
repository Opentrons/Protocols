from opentrons import labware, instruments
"""
PART II: After incubation
"""

# customization
sample_num = 96
reagent_row_1 = 6

# labware setup
incubation_plate = labware.load('96-PCR-tall', '1')
incubation_plate2 = labware.load('96-PCR-tall', '2')
pp_plate = labware.load('96-PCR-tall', '3')
pp_plate2 = labware.load('96-PCR-tall', '5')
b_gone_plate = labware.load('96-PCR-tall', '6')
b_gone_plate2 = labware.load('96-PCR-tall', '9')

reagent_rack = labware.load('96-PCR-tall', '4')
tiprack = labware.load('tiprack-200ul', '7')
tiprack2 = labware.load('tiprack-200ul', '8')
tiprack3 = labware.load('tiprack-200ul', '10')

meoh_loc = reagent_rack.wells('A5')

# Copy incubation plate to the PP plates and B-Gone plates. Locations to copy
# from and destination locations are determined by the number of samples. 
pp_dest = []
b_gone_dest = []
incub_source = []
if sample_num <= 72:
    incub_source = [well for well in incubation_plate.rows(0)] + [
                    well for well in incubation_plate.rows(1)[0:4]]
    pp_dest = [well for well in pp_plate.rows(0)] + [
                    well for well in pp_plate.rows(1)[0:4]]
    b_gone_dest = [well for well in b_gone_plate.rows(0)] + [
                    well for well in b_gone_plate.rows(1)[0:4]]
else:
    incub_source = [well for well in incubation_plate.rows(reagent_row_1)] + \
            [well for well in incubation_plate.rows(reagent_row_1 + 1)[0:4]]
    pp_dest = [well for well in pp_plate.rows(reagent_row_1)] + [
                    well for well in pp_plate.rows(reagent_row_1 + 1)[0:4]]
    b_gone_dest = [well for well in b_gone_plate.rows(0)] + [
                    well for well in b_gone_plate.rows(1)[0:4]]

well_count = 0
if sample_num <= 72:
    pp_dest_plate = pp_plate.rows[2:]
    b_gone_dest_plate = b_gone_plate.rows[2:]
    incub_source_plate = incubation_plate.rows[2:]
else:
    pp_dest_plate = pp_plate2.rows()
    b_gone_dest_plate = b_gone_plate2.rows()
    incub_source_plate = incubation_plate2.rows()

for source_row, pp_row, b_gone_row in zip(incub_source_plate, pp_dest_plate,
                                          b_gone_dest_plate):
    for source_well, pp_well, b_gone_well in zip(source_row, pp_row,
                                                 b_gone_row):
        if well_count < sample_num:
            incub_source.append(source_well)
            pp_dest.append(pp_well)
            b_gone_dest.append(b_gone_well)
            well_count += 1


# Pipette setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack, tiprack2, tiprack3])


# Transfer MeOH to PP plates
p300.pick_up_tip()
p300.transfer(300, meoh_loc, pp_dest, new_tip='never')
p300.transfer(150, meoh_loc, pp_dest, new_tip='never')
p300.drop_tip()

# Transfer incubation plate to PP plates
p300.transfer(150, incub_source, pp_dest, new_tip='always')

# Transfer MeOH to B-Gone plates
p300.pick_up_tip()
p300.transfer(133, meoh_loc, b_gone_dest, new_tip='never')
p300.drop_tip()

# Transfer incubation plate to B-Gone plates
p300.transfer(200, incub_source, b_gone_dest, new_tip='always')
