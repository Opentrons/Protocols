from opentrons import containers, instruments

# the number of plates with 19 mm diameter wells
num19plates = 1  # change here

# the number of plates with 32 mm diameter wells
num32plates = 1  # change here

# time to create liquid flow
time = 45  # change here

containers.create(
    '2x3_MaxwellPlate19mm',        # name of you container
    grid=(2, 3),                   # specify amount of (columns, rows)
    spacing=(38.4, 38.4),          # distances (mm) between each (column, row)
    diameter=19,                   # diameter (mm) of each well on the plate
    depth=8)                       # depth (mm) of each well on the plate

containers.create(
    '2x3_MaxwellPlate32mm',        # name of you container
    grid=(2, 3),                   # specify amount of (columns, rows)
    spacing=(38.4, 38.4),          # distances (mm) between each (column, row)
    diameter=32,                   # diameter (mm) of each well on the plate
    depth=8)                       # depth (mm) of each well on the plate

smallplates = []
largeplates = []
locations = ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2']
small_adjusted = []
large_adjusted = []

for plate in range(num19plates):
    smallplates.append(
        containers.load('2x3_MaxwellPlate19mm', locations[plate]))

for plate in range(num32plates):
    largeplates.append(containers.load(
        '2x3_MaxwellPlate32mm',
        locations[plate + num19plates]))

for plate in smallplates:
    temp_plate = []
    for well in plate.wells():
        temp_plate.append((well, well.from_center(.2, .2, -.8)))
    small_adjusted.append(temp_plate)

for plate in largeplates:
    temp_plate = []
    for well in plate.wells():
        temp_plate.append((well, well.from_center(.12, .12, -.8)))
    large_adjusted.append(temp_plate)

# chemical A, waste, and saline
reagents = containers.load('tube-rack-15_50ml', 'D3')

# tip rack for p200 pipette
tip1000_rack = containers.load('tiprack-1000ul', 'B3')

# plates with wash buffer and blocking buffer
water = containers.load('trough-1row-25ml', 'C3')

# trash to dispose of tips
trash = containers.load('trash-box', 'A3')

# p100 (10 - 100 uL) (single)
p1000 = instruments.Pipette(
    axis='b',
    name='p1000',
    max_volume=1000,
    min_volume=100,
    channels=1,
    trash_container=trash,
    tip_racks=[tip1000_rack],
    aspirate_speed=1200,
    dispense_speed=1200)


def wash_well(buffer, volume, reps, delay, well, pipette, trash):
    for washes in range(0, reps):  # wash rep number of times
        pipette.pick_up_tip()
        pipette.transfer(volume, buffer, well, new_tip='never')

        pipette.delay(minutes=delay)

        # mix and remove buffer at bottom
        pipette.transfer(
            volume, well, trash, mix_before=(3, 1000), new_tip='never')

        # remove any leftover
        pipette.transfer(
            pipette.max_volume, well, trash, new_tip='never')
        pipette.drop_tip()


# locations of 50ml tubes
chemA = reagents.wells('A3')
saline = reagents.wells('B3')
chemwaste = reagents.wells('A4')

# seconds to do 1 mix step, found experimentally
one_mix = 1.7

# 1. Add chemicalA from tube to a well until 1.5 ml (or 4 ml for large wells)
# is inside (Pipette 1).
#
# 2. Lower pipette to about 1 mm above ground and create a liquid flow over
# well center by pipetting in and out (fast) for 45 seconds
# (or an adjustable time)
# while an electrochemical process is occuring (Pipette 1, same tip).
#
# 3. Transfer as much as possible of chemicalA to the next well
# (Pipette 1, same tip). We need to test how much we can transfer,
# probably about 0.25 ml (0.5 ml) will remain.
# After one plate (6 wells) is done,
# transfer chemicalA to chemical-waste instead.
#
# 4. Wash out well 3 times with water from container,
# by filling 1 ml (3 ml), mix and transfer away as much as possible
# to normal-waste (Pipette 2, same tip)
#
# 5. Move to next well, start over at step 1 until one plate (6 wells) is done
# (remember that already some chemicalA is inside from step 3,
# just add some more from tube so it adds up to 1.5 ml (4 ml) again)
#
# 6. After repeating steps 1-5 for the entire plate (6 wells):
# Add 1 ml (3 ml) of Saline to each well (Pipette 2, new tip,
# same tip for all 6 wells)

for plate in small_adjusted:
    for num in range(6):
        p1000.pick_up_tip()
        well = plate[num]
        if num == 0:  # step 1 first well
            p1000.transfer(1500, chemA, well, new_tip='never')
        elif num != 0:  # step 1 other wells
            p1000.transfer(250, chemA, well, new_tip='never')
        p1000.mix(round(time/one_mix), 750, well)  # step 2 create liquid flow
        if num != 5:  # step 3 other wells
            p1000.transfer(1500, well, plate[num+1], new_tip='never')
        elif num == 5:  # step 3 last well
            p1000.transfer(1500, well, chemwaste, new_tip='never')
        p1000.drop_tip()
        wash_well(water, 1000, 3, 0, well, p1000, trash)  # step 4 wash well

    p1000.transfer(1000, saline, plate, new_tip='always')  # step 6 saline

for plate in large_adjusted:
    for num in range(6):
        p1000.pick_up_tip()
        well = plate[num]
        if num == 0:
            p1000.transfer(4000, chemA, well, new_tip='never')
        elif num != 0:
            p1000.transfer(500, chemA, well, new_tip='never')
        p1000.mix(round(time/one_mix), 750, well)
        if num != 5:
            p1000.transfer(4000, well, plate[num+1], new_tip='never')
        elif num == 5:
            p1000.transfer(4000, well, chemwaste, new_tip='never')
        p1000.drop_tip()
        wash_well(water, 3000, 3, 0, well, p1000, trash)

    p1000.transfer(3000, saline, plate, new_tip='always')
