from opentrons import containers, instruments

# volume of each antibody
vol = 50  # change here (in ul)

# extra voume aspirate for accuracy in multidispense
extravol = 20  # can change here (in ul)

# 96 well deep plate with antibodies
antibodies = containers.load('96-deep-well', 'C2')

# 96 well flat ELISA plates
plate1 = containers.load('96-PCR-flat', 'A1')
plate2 = containers.load('96-PCR-flat', 'B1')
plate3 = containers.load('96-PCR-flat', 'C1')
plate4 = containers.load('96-PCR-flat', 'D1')
plate5 = containers.load('96-PCR-flat', 'E1')
plate6 = containers.load('96-PCR-flat', 'A2')
plate7 = containers.load('96-PCR-flat', 'E2')
plate8 = containers.load('96-PCR-flat', 'A3')
plate9 = containers.load('96-PCR-flat', 'B3')
plate10 = containers.load('96-PCR-flat', 'C3')
plate11 = containers.load('96-PCR-flat', 'D3')

# tip rack for p50 pipette
tip200_rack = containers.load('tiprack-200ul', 'B2')

# trash to dispose of tips
trash = containers.load('point', 'D2', 'trash')

# p300 (50 - 300 uL) (multi)
p300multi = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=300,
    min_volume=50,
    channels=8,
    trash_container=trash,
    tip_racks=[tip200_rack])

p300multi.pick_up_tip()

# Transfer 50 uL of Antibodies from column 1 of antibodies to plate #1,
# with same tips
p300multi.distribute(
    vol,
    antibodies.rows('1'),
    plate1.rows(),
    disposal_vol=extravol,
    new_tip='never')

# Transfer 50 uL of Antibodies from column 2 of antibodies to plate #2
# with same tips
p300multi.distribute(
    vol,
    antibodies.rows('2'),
    plate2.rows(),
    disposal_vol=extravol,
    new_tip='never')

# Transfer 50 uL of Antibodies from column 3 of antibodies to  plate #3
# with same tips
p300multi.distribute(
    vol,
    antibodies.rows('3'),
    plate3.rows(),
    disposal_vol=extravol,
    new_tip='never')

# Transfer 50 uL of Antibodies from column 4 of antibodies to plate #4
# and columns #1 and 2 of plate #11
# with same tips
p300multi.distribute(
    vol,
    antibodies.rows('4'),
    plate4.rows(),
    disposal_vol=extravol,
    new_tip='never')

p300multi.distribute(
    vol,
    antibodies.rows('4'),
    plate11.rows('1', to='2'),
    disposal_vol=extravol,
    new_tip='never')

p300multi.drop_tip()

p300multi.pick_up_tip()

# Transfer 50 uL of Antibodies from column 5 of antibodies to plate #5
# with same tips
p300multi.distribute(
    vol,
    antibodies.rows('5'),
    plate5.rows(),
    disposal_vol=extravol,
    new_tip='never')

# Transfer 50 uL of Antibodies from column 6 of antibodies to plate #6
# with same tips
p300multi.distribute(
    vol,
    antibodies.rows('6'),
    plate6.rows(),
    disposal_vol=extravol,
    new_tip='never')

# Transfer 50 uL of Antibodies from column 7 of antibodies to  plate#7
# (same tips).
p300multi.distribute(
    vol,
    antibodies.rows('7'),
    plate7.rows(),
    disposal_vol=extravol,
    new_tip='never')

# Transfer 50 uL of Antibodies from column 8 of antibodies to  plate#8
# and columns #3 and 4 of plate#11 (same tips).
p300multi.distribute(
    vol,
    antibodies.rows('8'),
    plate8.rows(),
    disposal_vol=extravol,
    new_tip='never')

p300multi.distribute(
    vol,
    antibodies.rows('8'),
    plate11.rows('3', to='4'),
    disposal_vol=extravol,
    new_tip='never')

p300multi.drop_tip()

p300multi.pick_up_tip()

# Transfer 50 uL of Antibodies from column 9 of antibodies to   plate#9
# with same tips
p300multi.distribute(
    vol,
    antibodies.rows('9'),
    plate9.rows(),
    disposal_vol=extravol,
    new_tip='never')

# Transfer 50 uL of Antibodies from column 10 of antibodies to  plate#10
# and column #5 of plate#11 (same tips).
p300multi.distribute(
    vol,
    antibodies.rows('10'),
    plate10.rows(),
    disposal_vol=extravol,
    new_tip='never')

p300multi.distribute(
    vol,
    antibodies.rows('10'),
    plate11.rows('5'),
    disposal_vol=extravol,
    new_tip='never')

p300multi.drop_tip()
