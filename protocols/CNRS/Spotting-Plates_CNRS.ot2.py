from opentrons import instruments, labware

petri_6 = 'petri-dish-6cm'
petri_10 = 'petri-dish-10cm'
if petri_10 not in labware.list():
    labware.create(petri_10,
                   grid=(1, 1),  # specify amount of (columns, rows)
                   spacing=(0, 0),  # distances (mm) between each
                   diameter=100,
                   depth=10)

if petri_6 not in labware.list():
    labware.create(petri_6,
                   grid=(1, 1),  # specify amount of (columns, rows)
                   spacing=(0, 0),  # distances (mm) between each
                   diameter=60,
                   depth=10)

tubes = labware.load('tube-rack-15_50ml', '5')
dish1 = labware.load(petri_6, '1')
dish2 = labware.load(petri_6, '2')
dish3 = labware.load(petri_10, '3')
dish4 = labware.load(petri_10, '4')

petri_dishes = [dish1, dish2, dish3, dish4]
tips_p1000 = labware.load('tiprack-1000ul', '8')
tips_p50 = labware.load('tiprack-200ul', '9')

# instrument setup
p1000 = instruments.P1000_Single(
    tip_racks=[tips_p1000],
    mount='left')

p50 = instruments.P50_Single(
    tip_racks=[tips_p50],
    mount='right')

# variables and reagents setup
culture_loc = tubes.wells('A1')
# protocol begins

for dish in petri_dishes:
    # grab actual well from container
    dish_loc = dish.wells('A1')
    dish_size = dish_loc.properties['diameter']

    # Bacteria culture 1
    p1000.pick_up_tip()
    p1000.mix(5, 1000, culture_loc)
    p1000.return_tip()

    p50.pick_up_tip()
    p50.aspirate(40, culture_loc)
    # Dispenses culture at a distance measured using percentage difference
    # from the center of the well
    p50.dispense(
        40, (dish_loc, dish_loc.from_center(x=(1/dish_size), y=0, z=0)))
    p50.drop_tip()

    # Bacteria culture 2
    p1000.pick_up_tip(tips_p1000.wells('A1'))
    p1000.mix(5, 1000, next(culture_loc))
    p1000.return_tip()

    p50.pick_up_tip()
    p50.aspirate(40, next(culture_loc))
    # Dispenses culture at a distance measured using percentage difference
    # from the center of the well
    p50.dispense(
        40, (dish_loc, dish_loc.from_center(x=-(1/dish_size), y=0, z=0)))
    p50.drop_tip()
