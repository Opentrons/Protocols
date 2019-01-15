from opentrons import labware, instruments

metadata = {
    'protocolName': 'ELISA',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
tuberack_1 = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
tuberack_2 = labware.load('opentrons-tuberack-2ml-eppendorf', '2')
tuberack_3 = labware.load('opentrons-tuberack-2ml-eppendorf', '3')
tuberacks = [tuberack_1, tuberack_2, tuberack_3]

tuberack_4 = labware.load('opentrons-tuberack-15_50ml', '4')
plate = labware.load('96-flat', '5')
trough = labware.load('trough-12row', '6')
tiprack_m300 = labware.load('opentrons-tiprack-300ul', '7')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '8')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack_m300])
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
dilution_buffer = tuberack_4.wells('A3')
water = tuberack_4.wells('A1')
antibody = trough.wells('A1')
TMB_substrate = trough.wells('A2')
stop_solution = trough.wells('A3')
standards = tuberack_3.rows('D').wells('1', to='6')

# define elution pool
elution_pool = {index: {} for index in range(0, 9)}
for key, row in zip(
    elution_pool.keys(),
        [row for tuberack in tuberacks for row in tuberack.rows()]):
    for dil_factor, num in zip(['1', '10', '25', '100', '1000'], row[:5]):
        elution_pool[key][dil_factor] = num

elution_pool[9] = {
    dil_factor: num for dil_factor, num in zip(
        ['1', '10', '100', '1000', '5000', '10000', '25000', '50000'],
        [num for row in tuberack_3.rows('B', to='C') for num in row])}

"""
Adding Enzyme Conjugate Reagent
"""
m300.distribute(100, antibody, plate.cols(), blow_out=antibody)

"""
Adding Water
"""
p300.distribute(50, water, plate.wells('A1', 'A2'))

"""
Adding Dilution Buffer
"""
p300.distribute(50, dilution_buffer, plate.wells('B1', 'B2'))

"""
Adding HCP Standards
"""
for standard, row in zip(standards, plate.rows('C', to='H')):
    p300.distribute(50, standard, row[:2])

"""
Adding Samples
"""
dests = [[plate.cols(index)[num], plate.cols(index+1)[num]]
         for index in range(2, 12, 2) for num in range(8)]

sources = [elution_pool[index][dil_factor] for index in range(9)
           for dil_factor in ['10', '25', '100', '1000']]
sources += [elution_pool[9][dil_factor]
            for dil_factor in ['5000', '10000', '25000', '50000']]

for source, dest in zip(sources, dests):
    p300.distribute(50, source, [well.top() for well in dest])
