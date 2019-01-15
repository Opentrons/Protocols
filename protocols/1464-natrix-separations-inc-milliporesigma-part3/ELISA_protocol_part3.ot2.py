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
tiprack_m300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['7', '8']]

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tiprack_m300)

# reagent setup
dilution_buffer = tuberack_4.wells('A3')
water = tuberack_4.wells('A1')
antibody = trough.wells('A1')
TMB_substrate = trough.wells('A2')
stop_solution = trough.wells('A3')
standards = tuberack_3.rows('D').wells('1', to='6')

"""
Adding TMB substrate
"""
m300.distribute(
    100, TMB_substrate, [col[0].top() for col in plate.cols()],
    blow_out=TMB_substrate)

m300.delay(minutes=30)

"""
Adding Stop Solution
"""
for col in plate.cols():
    m300.pick_up_tip()
    m300.transfer(100, stop_solution, col, new_tip='never')
    m300.mix(10, 100, col)
    m300.drop_tip()
