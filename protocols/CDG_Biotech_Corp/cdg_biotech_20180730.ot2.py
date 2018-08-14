from opentrons import labware, instruments

# Labware setup
P1 = labware.load('96-flat', '1')
P2 = labware.load('96-flat', '2')
P3 = labware.load('96-flat', '3')
P4 = labware.load('96-flat', '4')
P5 = labware.load('96-flat', '5')
P6 = labware.load('96-flat', '6')
P7 = labware.load('96-flat', '7')

reagent_1 = labware.load('trough-12row', '8').wells('A1')
reagent_2 = labware.load('trough-1row-25ml', '9')

tiprack1 = labware.load('tiprack-200ul', '10')
tiprack2 = labware.load('tiprack-200ul', '11')

# Pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack1])

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack2])

# All locations of all the plates
all_plates = P1.cols() + P2.cols() + P3.cols() + P4.cols() +\
       P5.cols() + P6.cols() + P7.cols()

# Transfer 130 uL of reagent_1
m300.transfer(130, reagent_1, all_plates)

# Transfer 140 uL of reagent_1
m300.transfer(140, reagent_1, all_plates)

# Row D of all plates
reagent_2_dest = P1.rows('D') + P2.rows('D') + P3.rows('D') + P4.rows('D') +\
       P5.rows('D') + P6.rows('D') + P7.rows('D')

# Transfer reagent_2
p300.transfer(110, reagent_2, reagent_2_dest)
