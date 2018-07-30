from opentrons import labware, instruments

# Customization
strip_num = 10

# Labware setup
plate = labware.load('96-flat', '2')
trough_12 = labware.load('trough-12row', '1')
trough_1 = labware.load('trough-1row-25ml', '3')
liquid_trash = labware.load('trough-1row-25ml', '4')
tiprack = labware.load('tiprack-200ul', '6')

dilution_buffer = trough_12.wells('A1')
conjugate = trough_12.wells('A2')
substrate = trough_12.wells('A3')
stop_solution = trough_12.wells('A4')

target_strips = plate.cols(0, length=strip_num)

# Pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])


# Transfer dilution buffer
m300.transfer(90, dilution_buffer, target_strips)

m300.delay(minutes=45)

# Empty wells
m300.transfer(90, target_strips, liquid_trash)

# Wash wells with wash buffer 5 times
m300.pick_up_tip()
for each_strip in target_strips:
    for mix_repetition in range(5):
        m300.transfer(300, trough_1, each_strip, new_tip='never')
        m300.transfer(300, each_strip, liquid_trash, new_tip='never')
m300.drop_tip()

# Transfer conjugate
m300.transfer(100, conjugate, target_strips)

m300.delay(minutes=30)

# Empty wells
m300.transfer(100, target_strips, liquid_trash)

# Wash wells with wash buffer 5 times
m300.pick_up_tip()
for each_strip in target_strips:
    for mix_repetition in range(5):
        m300.transfer(300, trough_1, each_strip, new_tip='never')
        m300.transfer(300, each_strip, liquid_trash, new_tip='never')
m300.drop_tip()

# Transfer substrate
m300.transfer(100, substrate, target_strips)

m300.delay(minutes=15)

# Transfer stop solution
m300.transfer(100, stop_solution, target_strips)
