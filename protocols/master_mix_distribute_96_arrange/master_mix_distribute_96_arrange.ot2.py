from opentrons import labware, instruments


source = labware.load('96-deep-well', '11', 'source')
p10rack = labware.load('tiprack-10ul', '10', 'p10rack')


p10 = instruments.P10_Multi(
    tip_racks=[p10rack],
    mount="left",
)

# target_slots = ['D1', 'E1', 'A2', 'A3', 'B2', 'C2', 'D2', 'D3', 'E2', 'E3']
# plate_type = 'PCR-strip-tall'
# HACK: need to explicitly load each container like this
# instead of using a for loop, so that deck map can be parsed out
# for protocol library
# targets = [
#     c o n t a i n e r s.load(plate_type, slot) for slot in target_slots]
targets = [
    labware.load('PCR-strip-tall', '1'),
    labware.load('PCR-strip-tall', '2'),
    labware.load('PCR-strip-tall', '3'),
    labware.load('PCR-strip-tall', '4'),
    labware.load('PCR-strip-tall', '5'),
    labware.load('PCR-strip-tall', '6'),
    labware.load('PCR-strip-tall', '7'),
    labware.load('PCR-strip-tall', '8'),
    labware.load('PCR-strip-tall', '9')
]

# print(targets)

dest1 = [col for plate in targets for col in plate.cols('1', to='11')]
dest2 = [col for plate in targets for col in plate.cols('4', '8', '12')]
dest3 = [col for plate in targets for col in plate.cols('1', '5', '9')]
dest4 = [col for plate in targets for col in plate.cols('2', '6', '10')]
dest5 = [col for plate in targets for col in plate.cols('3', '7', '11')]
dest6 = [col for plate in targets for col in plate.cols('4', '8', '12')]
dest7 = [col for plate in targets for col in plate.cols('5')]
dest8 = [col for plate in targets for col in plate.cols('6')]
dest9 = [col for plate in targets for col in plate.cols('7')]
dest10 = [col for plate in targets for col in plate.cols('8')]

# Coat the pipette tips
p10.pick_up_tip()
p10.mix(3, 10, source.cols('1'))

# Transfer row 1 of source to their target rows
p10.transfer(6, source.cols('1'), dest1, new_tip='once')

# Transfer row 2 of source to their target rows
p10.transfer(6, source.cols('2'), dest2, new_tip='once')

# Transfer row 4 of source to their target rows
p10.transfer(1, source.cols('4'), dest3, new_tip='once')

# Transfer row 5 of source to their target rows
p10.transfer(1, source.cols('5'), dest4, new_tip='once')

# Transfer row 6 of source to their target rows
p10.transfer(1, source.cols('6'), dest5, new_tip='once')

# Transfer row 7 of source to their target rows
p10.transfer(1, source.cols('7'), dest6, new_tip='once')

# Transfer row 9 of source to their target rows
p10.transfer(1, source.cols('9'), dest7, new_tip='once')

# Transfer row 10 of source to their target rows
p10.transfer(1, source.cols('10'), dest8, new_tip='once')

# Transfer row 11 of source to their target rows
p10.transfer(1, source.cols('11'), dest9, new_tip='once')

# Transfer row 12 of source to their target rows
p10.transfer(1, source.cols('12'), dest10, new_tip='once')
