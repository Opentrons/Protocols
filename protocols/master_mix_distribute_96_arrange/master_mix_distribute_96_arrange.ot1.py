from opentrons import containers, instruments


source = containers.load('96-deep-well', 'C3', 'source')
p10rack = containers.load('tiprack-10ul', 'B3', 'p10rack')
trash = containers.load('point', 'A1', 'trash')

p10 = instruments.Pipette(
    name="p10",
    trash_container=trash,
    tip_racks=[p10rack],
    min_volume=1,
    max_volume=10,
    axis="a",
    channels=8

)

# target_slots = ['D1', 'E1', 'A2', 'A3', 'B2', 'C2', 'D2', 'D3', 'E2', 'E3']
# plate_type = 'PCR-strip-tall'
# HACK: need to explicitly load each container like this
# instead of using a for loop, so that deck map can be parsed out
# for protocol library
# targets = [
#     c o n t a i n e r s.load(plate_type, slot) for slot in target_slots]
targets = [
    containers.load('PCR-strip-tall', 'D1'),
    containers.load('PCR-strip-tall', 'E1'),
    containers.load('PCR-strip-tall', 'A2'),
    containers.load('PCR-strip-tall', 'A3'),
    containers.load('PCR-strip-tall', 'B2'),
    containers.load('PCR-strip-tall', 'C2'),
    containers.load('PCR-strip-tall', 'D2'),
    containers.load('PCR-strip-tall', 'D3'),
    containers.load('PCR-strip-tall', 'E2'),
    containers.load('PCR-strip-tall', 'E3')
]

# print(targets)

dest1 = [row for plate in targets for row in plate.rows('1', to='11')]
dest2 = [row for plate in targets for row in plate.rows('4', '8', '12')]
dest3 = [row for plate in targets for row in plate.rows('1', '5', '9')]
dest4 = [row for plate in targets for row in plate.rows('2', '6', '10')]
dest5 = [row for plate in targets for row in plate.rows('3', '7', '11')]
dest6 = [row for plate in targets for row in plate.rows('4', '8', '12')]
dest7 = [row for plate in targets for row in plate.rows('5')]
dest8 = [row for plate in targets for row in plate.rows('6')]
dest9 = [row for plate in targets for row in plate.rows('7')]
dest10 = [row for plate in targets for row in plate.rows('8')]

# Coat the pipette tips
p10.pick_up_tip()
p10.mix(3, 10, source.rows('1'))

# Transfer row 1 of source to their target rows
p10.transfer(6, source.rows('1'), dest1, new_tip='once')

# Transfer row 2 of source to their target rows
p10.transfer(6, source.rows('2'), dest2, new_tip='once')

# Transfer row 4 of source to their target rows
p10.transfer(1, source.rows('4'), dest3, new_tip='once')

# Transfer row 5 of source to their target rows
p10.transfer(1, source.rows('5'), dest4, new_tip='once')

# Transfer row 6 of source to their target rows
p10.transfer(1, source.rows('6'), dest5, new_tip='once')

# Transfer row 7 of source to their target rows
p10.transfer(1, source.rows('7'), dest6, new_tip='once')

# Transfer row 9 of source to their target rows
p10.transfer(1, source.rows('9'), dest7, new_tip='once')

# Transfer row 10 of source to their target rows
p10.transfer(1, source.rows('10'), dest8, new_tip='once')

# Transfer row 11 of source to their target rows
p10.transfer(1, source.rows('11'), dest9, new_tip='once')

# Transfer row 12 of source to their target rows
p10.transfer(1, source.rows('12'), dest10, new_tip='once')
