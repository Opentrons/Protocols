from opentrons import labware, instruments

metadata = {
    'protocolName': 'ELISA: Dilution',
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
tiprack_1000 = labware.load('tiprack-1000ul', '7')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '8')

# instrument setup
p1000 = instruments.P1000_Single(
    mount='left',
    tip_racks=[tiprack_1000])
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
dilution_buffer = tuberack_4.wells('A3')
water = tuberack_4.wells('A1')
antibody = trough.wells('A1')
TMB_substrate = trough.wells('A2')
stop_solution = trough.wells('A3')

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
Adding Dilution Buffer
"""
dest_720 = []
for key in elution_pool.keys():
    for dil_factor in ['10', '100', '1000', '10000']:
        if dil_factor in elution_pool[key]:
            dest_720.append(elution_pool[key][dil_factor])
p1000.transfer(720, dilution_buffer, dest_720)

dest_180 = []
for key in elution_pool.keys():
    for dil_factor in ['25', '25000']:
        if dil_factor in elution_pool[key]:
            dest_180.append(elution_pool[key][dil_factor])
p300.transfer(180, dilution_buffer, dest_180)

dest_320 = []
for key in elution_pool.keys():
    for dil_factor in ['5000', '50000']:
        if dil_factor in elution_pool[key]:
            dest_320.append(elution_pool[key][dil_factor])
p1000.distribute(320, dilution_buffer, dest_320)

"""
Adding elution sample
"""
for index in range(9):
    p300.pick_up_tip()
    for vol, source, dest in zip(
            [80, 80, 80, 120],
            ['1', '10', '100', '10'],
            ['10', '100', '1000', '25']):
        p300.transfer(
            vol,
            elution_pool[index][source],
            elution_pool[index][dest],
            new_tip='never')
        p300.mix(3, 150, elution_pool[index][dest])
        p300.blow_out(elution_pool[index][dest])
    p300.drop_tip()

p300.pick_up_tip()
for vol, source, dest in zip(
        [80, 80, 80, 120, 120, 80, 80],
        ['1', '10', '100', '1000', '10000', '1000', '10000'],
        ['10', '100', '1000', '10000', '25000', '5000', '50000']):
    p300.transfer(
        vol,
        elution_pool[9][source],
        elution_pool[9][dest],
        new_tip='never')
    p300.mix(3, 150, elution_pool[9][dest])
    p300.blow_out(elution_pool[9][dest])
p300.drop_tip()
