from opentrons import containers, instruments

# source of buffer
media = containers.load('trough-1row-25ml', 'B2')
drugmedia = containers.load('trough-1row-25ml', 'D2')

# plate dilution will happen in
plate = containers.load('96-PCR-flat', 'C1')

# tip rack for p200 pipette
m200rack = containers.load('tiprack-200ul', 'A1')

# trash location
trash = containers.load('point', 'E1')

p300multi = instruments.Pipette(
    trash_container=trash,
    name='p300m',
    tip_racks=[m200rack],
    min_volume=30,
    max_volume=300,
    axis="a",
    channels=8
)

p300multi.pick_up_tip()

# Workflow description: Step 1: Tranfer 172.5 uL media from Basin (Media)
# to well A2 of plate using multi-channel
# Step 2: Tranfer 172.5 uL media from Basin (Media) to well A3 of plate
# using multi-channel (same tips)
p300multi.transfer(172.5, media, plate.rows(1, length=2), new_tip='never')

# Using multi-channel (same tips)...
# Step 3:Tranfer 115 uL media from Basin (Media) to well A4 of plate
# Step 4:Tranfer 115 uL media from Basin (Media) to well A5 of plate
# Step 5:Tranfer 115 uL media from Basin (Media) to well A6 of plate
# Step 6:Tranfer 115 uL media from Basin (Media) to well A7 of plate
# Step 7:Tranfer 115 uL media from Basin (Media) to well A8 of plate
# Step 8:Tranfer 115 uL media from Basin (Media) to well A9 of plate
# Step 9:Tranfer 115 uL media from Basin (Media) to well A10 of plate
p300multi.transfer(115, media, plate.rows(3, length=7), new_tip='never')

# Step 10: Eject multi-channel tips and pick up new multi-channel tips
p300multi.drop_tip()
p300multi.pick_up_tip()

# Step 11:Transfer 210 uL from Basin (Drugged media) to A1 of plate
# using multi-channel
p300multi.transfer(210, drugmedia, plate.rows(0), new_tip='never')

# mix 120 uL 6x (same tips)...
# Step 12:Transfer 57.5 uL from A1 of plate to A2 of plate
# Step 13:Transfer 57.5 uL from A2 of plate to A3 of plate
p300multi.transfer(
    57.5,
    plate.rows(0, length=2),
    plate.rows(1, length=2),
    mix_after=(6, 120),
    new_tips='never')

# mix 120 uL 6x (same tips)...
# Step 14:Transfer 115 uL from A3 of plate to A4 of plate
# Step 15:Transfer 115 uL from A4 of plate to A5 of plate
# Step 16:Transfer 115 uL from A5 of plate to A6 of plate
# Step 17:Transfer 115 uL from A6 of plate to A7 of plate
# Step 18:Transfer 115 uL from A7 of plate to A8 of plate
# Step 19:Transfer 115 uL from A8 of plate to A9 of plate
# Step 20:Transfer 115 uL from A9 of plate to A10 of plate
p300multi.transfer(
    115,
    plate.rows(2, length=7),
    plate.rows(3, length=7),
    mix_after=(6, 120),
    new_tips='never')

p300multi.drop_tip()
