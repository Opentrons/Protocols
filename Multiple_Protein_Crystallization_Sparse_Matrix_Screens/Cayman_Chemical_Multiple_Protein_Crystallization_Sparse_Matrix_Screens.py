from opentrons import robot, containers, instruments

p20rack = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'E1', 
    'p20rack'
)
p20rack2 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'E2', 
    'p20rack2'
)
p20rack3 = containers.load(
    'tiprack-10ul', # make p20 rack container and change
    'E3', 
    'p20rack3'
)
p1000rack = containers.load(
    'tiprack-1000ul', 
    'A1', 
    'p1000rack'
)
p1000rack2 = containers.load(
    'tiprack-1000ul', 
    'A2', 
    'p1000rack2'
)
cooldeck = containers.load(
    'alum-block-pcr-strips', # using the PCR tubes section
    'C3',
    'cooldeck'
) 
plate = containers.load(
    'rigaku-compact-crystallization-plate', # make crystallization plate container and change
    'C1',
    'plate'
)
plate2 = containers.load(
    'rigaku-compact-crystallization-plate', # make crystallization plate container and change
    'C2',
    'plate2'
)
matrix_index = containers.load(
    'hampton-1ml-deep-block', # make matrix block container and change
    'B1',
    'matrix_index'
)
matrix_peg = containers.load(
    'hampton-1ml-deep-block', # make matrix block container and change
    'B2',
    'matrix_peg'
)
trash = containers.load(
    'point',
    'A3',
    'trash'
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
        tip_racks=[p20rack, p20rack2, p20rack3],
        trash_container=trash,
        channels=8,
        name="p10"
)

# Using 1 mL pipette head on the left axis, robot collects tip from 1 mL rack 
# and then robot individually draws up 100 uL from well A1 of Hampton Index HT 1 mL deep well block 
# and distributes it to lower compartment of well A1 Rigaku Compact 300 Crystallization Plate 1 (XJR). 
# Robot discards pipette tip and retrieves a fresh tip. Repeats process with B1. Repeats all the way to H12. 
# (96 individual distributions of 100 uL from screen to crystal plate). 
# No blow-out or aspiration following distribution. Robot discards final pipette tip.


# runs from 18:54 to 20:31
for i in range(96):
    p1000.pick_up_tip().aspirate(100, matrix_index[i]).dispense(plate[i+96]).drop_tip()
    
# Using 10 uL multi channel pipette head on the center axis, robot collects tip from 10 uL rack. 
# Protein will be stored in 8 PCR tubes inside cool deck aluminum block (15 uL in each tube). 
# The robot draws up 7 uL of protein solution stored on cool deck and using repeating functionality 
# distributes 1 uL to the upper compartment of A1-H1 Rigaku Compact 300 Crystallization Plate 1 
# then shifts to A2-H2 and distributes again repeats until A6-H6. The robot then collects an 
# additional 7 uL and continues to distribute beginning with the upper compartment of A7-H7 Rigaku 
# Compact 300 Crystallization Plate 1 and repeating until A12-H12. Robot discards pipette tip.
# No blow-out or aspiration following distribution.

p10.pick_up_tip().aspirate(7, cooldeck['A1'])
dispense_volume = 2
for i in range(12):
    if p10.current_volume < dispense_volume:
        p10.aspirate(7, cooldeck['A1'])
    p10.dispense(1, plate.rows[i][0].top())
p10.drop_tip()

# Using 10 uL multichannel pipette head on the center axis, robot collects tip from 10 uL rack 
# and then robot individually draws up 1 uL from lower compartment of well A1-H1 Rigaku Compact 
# 300 Crystallization Plate 1 and distributes it to upper compartment of well A1-H1 Rigaku Compact 
# 300 Crystallization Plate 1 (XJR). Robot discards pipette tips and retrieves set of fresh tips. 
# Repeats process with A2-H2. Repeats all the way to A12-H12. (12 multichannel distributions of 1 uL 
# from lower compartment to upper compartment of plate). No blow-out or aspiration following distribution. 
# If possible, after each distribution if pipette head could move back and forth a small amount to gently mix.

for i in range(12):
    p10.pick_up_tip().aspirate(1, plate.rows[i][0]).dispense(plate.rows[i+12][0].top()).touch_tip().drop_tip()
    
# Using 1 mL pipette head on the left axis, robot collects tip from 1 mL rack 
# and then robot individually draws up 100 uL from well A1 of Hampton PegRX HT 1 mL deep well block 
# and distributes it to lower compartment of well A1 Rigaku Compact 300 Crystallization Plate 2 (XJR). 
# Robot discards pipette tip and retrieves a fresh tip. Repeats process with B1. Repeats all the way to H12. 
# (96 individual distributions of 100 uL from screen to crystal plate 2). 
# No blow-out or aspiration following distribution. Robot discards final pipette tip.

for i in range(96):
    p1000.pick_up_tip().aspirate(100, matrix_peg[i]).dispense(plate2[i+96]).drop_tip()
    
# Using 10 uL multi channel pipette head on the center axis, robot collects tip from 10 uL rack. 
# Protein will be stored in 8 PCR tubes inside cool deck aluminum block (15 uL in each tube). 
# The robot draws up 7 uL of protein solution stored on cool deck and using repeating functionality 
# distributes 1 uL to the upper compartment of A1-H1 Rigaku Compact 300 Crystallization Plate 2 
# then shifts to A2-H2 and distributes again repeats until A6-H6. The robot then collects an 
# additional 7 uL and continues to distribute beginning with the upper compartment of A7-H7 Rigaku 
# Compact 300 Crystallization Plate 2 and repeating until A12-H12. Robot discards pipette tip. 
# No blow-out or aspiration following distribution.

p10.pick_up_tip().aspirate(7, cooldeck['A1'])
dispense_volume = 2
for i in range(12):
    if p10.current_volume < dispense_volume:
        p10.aspirate(7, cooldeck['A1'])
    p10.dispense(1, plate2.rows[i][0].top())
p10.drop_tip()

# Using 10 uL multichannel pipette head on the center axis, robot collects tip from 10 uL rack 
# and then robot individually draws up 1 uL from lower compartment of well A1-H1 Rigaku Compact 
# 300 Crystallization Plate 2 and distributes it to upper compartment of well A1-H1 Rigaku Compact 
# 300 Crystallization Plate (XJR). Robot discards pipette tips and retrieves set of fresh tips. 
# Repeats process with A2-H2. Repeats all the way to A12-H12. (12 multichannel distributions of 1 uL 
# from lower compartment to upper compartment of plate 2). No blow-out or aspiration following distribution. 
# If possible, after each distribution if pipette head could move back and forth a small amount to gently mix.

for i in range(12):
    p10.pick_up_tip().aspirate(1, plate2.rows[i][0]).dispense(plate2.rows[i+12][0].top()).touch_tip().drop_tip()
