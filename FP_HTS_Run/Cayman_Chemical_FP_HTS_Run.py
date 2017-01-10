from opentrons import robot, containers, instruments

p20rack = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'A1', 
    'p20rack'
)
p20rack2 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'A2', 
    'p20rack2'
)
p20rack3 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'A3', 
    'p20rack3'
)
p20rack4 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'A3', 
    'p20rack4'
)
p20rack5 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'A3', 
    'p20rack5'
)
p20rack6 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'A3', 
    'p20rack6'
)
p20rack7 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'A3', 
    'p20rack7'
)
p1000rack = containers.load(
    'tiprack-1000ul', 
    'E1', 
    'p1000rack'
)
p1000rack2 = containers.load(
    'tiprack-1000ul', 
    'E2', 
    'p1000rack2'
)
cooldeck = containers.load(
    'alum-block-pcr-strips', # using the PCR tubes section
    'C1',
    'cooldeck'
)
compounds_plate = containers.load(
    '96-PCR-flat', 
    'C2',
    'compounds_plate'
)
dilution_plate = containers.load(
    '384-plate',
    'C2',
    'dilution_plate'
)
assay_plate = containers.load(
    '384-plate',
    'C2',
    'assay_plate'
)
trash = containers.load(
    'point',
    'B2',
    'trash'
)
DMSO = containers.load(
    'trough-12row',
    'B2',
    'DMSO'
)
reagents = containers.load(
    'trough-12row',
    'B2',
    'reagents'
)
p1000 = instruments.Pipette(   
        axis="b",
        max_volume=1000,
        min_volume=100,
        tip_racks=[p1000rack, p1000rack2],
        trash_container=trash,
        channels=1,
        name="p1000"
)
p10 = instruments.Pipette(   
        axis="a",
        max_volume=10,
        min_volume=1,
        tip_racks=[p20rack, p20rack2, p20rack3, p20rack4, p20rack5, p20rack6, p20rack7],
        trash_container=trash,
        channels=8,
        name="p10"
)

# 16 compounds will be present in a PCR plate dissolved in DMSO in columns 1 and 2. 
# Using 10 uL multi channel pipette head on the center axis, robot collects tip from 10 uL rack. 
# The robot will fill all wells in columns 1-20 with 10 uL DMSO. There is no need to discard tips between placements.

p10.pick_up_tip()
for i in range(20):
    p10.aspirate(10, DMSO['A1']).dispense(dilution_plate.rows[i][0])
    p10.aspirate(10, DMSO['A1']).dispense(dilution_plate.rows[i][1])
p10.drop_tip()

# The robot will pick up 10 uL of compounds in column 1 (A1-H1) and distribute it to 384 dilution plate 
# into wells A1, C1, E1, G1, I1, K1, M1, O1. The robot will mix the wells by pipetting up and down. 

p10.pick_up_tip().aspirate(10, compounds_plate.rows[0][0]).dispense(dilution_plate[0]).mix(10, 3, dilution_plate[0]).drop_tip()
    
# The robot will discard tips and retrieve fresh 10 uL tips on multichannel pipette. 
# The robot will pick up 10 uL of compounds in column 2 (A2-H2) and distribute it to 384 dilution plate 
# into wells B1, D1, F1, H1, J1, L1, N1, P1. The robot will mix the wells by pipetting up and down. 

p10.pick_up_tip().aspirate(10, compounds_plate.rows[1][0]).dispense(dilution_plate[1]).mix(10, 3, dilution_plate[1]).drop_tip()

# The robot will discard tips and retrieve fresh 10 uL tips on multichannel pipette. 
# The robot will draw 10 uL up from wells A1, C1, E1, G1, I1, K1, M1, O1 and transfer it to 
# wells A2, C2, E2, G2, I2, K2, M2, O2, the robot will mix the wells by pipetting up and down. 
# The robot will discard tips and retrieve fresh 10 uL tips on multichannel pipette. 
# The robot will draw 10 uL up from wells B1, D1, F1, H1, J1, L1, N1, P1 and transfer it to wells 
# B2, D2, F2, H2, J2, L2, N2, P2 the robot will mix the wells by pipetting up and down. 
# The robot will discard tips and retrieve fresh 10 uL tips on multichannel pipette. 
# This process will be repeated until row 22.

for i in range(21):
    p10.pick_up_tip().aspirate(10, dilution_plate.rows[i][0]).dispense(dilution_plate.rows[i+1][0])
    p10.mix(10, 3, dilution_plate.rows[i+1][0]).drop_tip()
    p10.pick_up_tip().aspirate(10, dilution_plate.rows[i][1]).dispense(dilution_plate.rows[i+1][1])
    p10.mix(10, 3, dilution_plate.rows[i+1][1]).drop_tip()
    
# Using 1 mL pipette head on the left axis, robot collects tip from 1 mL rack 
# and then robot individually draws up 1000 mL of assay mix from Reagent mix boat. 
# Using repeater functionality, 58.8 µL is dispensed into all 16 wells of column 1 of 384 well assay plate. 
# The robot returns to the reagent boat and does tip bowl out to discard any additional reagent. 
# Then draws up additional 1000 uL and proceeds to dispense 58.8 µL into all 16 wells of 
# column 2 of 384 well assay plate. This is repeated for all columns 3-22.

p1000.pick_up_tip()
dispense_volume = 58.8
for i in range(352):
    if p1000.current_volume < dispense_volume:
        p1000.blow_out(reagents['A1']).aspirate(1000, reagents['A1'])
    p1000.dispense(58.8, assay_plate[i])
p1000.drop_tip()

# Using 10 uL multichannel pipette head on the center axis, robot collects tip from 10 uL rack. 
# Draws up 1.2 uL from wells A1, C1, E1, G1, I1, K1, M1, O1 of 384 dilution plate 
# and transfers it to wells A1, C1, E1, G1, I1, K1, M1, O1 of 384 well assay plate. 
# The robot will discard tips and retrieve fresh 10 uL tips on multichannel pipette. 
# Draws up 1.2 uL from wells B1, D1, F1, H1, J1, L1, N1, P1 of 384 dilution plate 
# and transfers it to wells B1, D1, F1, H1, J1, L1, N1, P1 of 384 well assay plate. 
# This is repeated for all columns 2-22.

for i in range(22):
    p10.pick_up_tip().aspirate(1.2, dilution_plate.rows[i][0]).dispense(assay_plate.rows[i][0]).drop_tip()
    p10.pick_up_tip().aspirate(1.2, dilution_plate.rows[i][1]).dispense(assay_plate.rows[i][1]).drop_tip()

# Using 1 mL pipette head on the left axis, robot collects tip from 1 mL rack 
# and then robot individually draws up 1000 mL of assay mix from Reagent mix boat. 
# Using repeater functionality 60 uL is distributed to all wells in column 23 (16 wells). 
# This corresponds to the negative control. Tip is discarded.

p1000.pick_up_tip().aspirate(1000, reagents['A1'])
for i in range(16):
    p1000.dispense(60, assay_plate.rows[22][i])
p1000.drop_tip()

# Using 1 mL pipette head on the left axis, robot collects tip from 1 mL rack 
# and then robot individually draws up 1000 mL of positive control mix from 1.5 mL PCR tube stored on cold deck. 
# Using repeater functionality 60 uL is distributed to all wells in column 24 (16 wells). 
# This corresponds to the positive control. Tip is discarded.

p1000.pick_up_tip().aspirate(1000, cooldeck['A1']) # adjust once proper cold deck container created
for i in range(16):
    p1000.dispense(60, assay_plate.rows[23][i])
p1000.drop_tip()