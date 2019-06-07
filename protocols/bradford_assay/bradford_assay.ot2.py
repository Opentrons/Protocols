from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Bradford Assay',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

tiprack = labware.load('tiprack-200ul', '7')
tiprack2 = labware.load('tiprack-200ul', '11')

trash = robot.fixed_trash

trough = labware.load('trough-12row', '8')
plate = labware.load('96-PCR-flat', '9')
tuberack = labware.load('tube-rack-2ml', '10')

# Needs to have individual constructor
m50 = instruments.P50_Multi(
    tip_racks=[tiprack, tiprack2],
    mount="left")

p200 = instruments.P300_Single(
    tip_racks=[tiprack],
    mount="right"
)

# dispense 6 standards from tube racks (A1, B1, C1, D1, A2, B2)
# to first two rows of 96 well plate (duplicates, A1/A2, B1/B2 etc.)
for i in range(6):
    p200.distribute(
        25, tuberack.wells(i), plate.rows(i)[0:2])

# dispense 4 samples from tube rack (C2, D2, A3, B3)
# to row 3 of 96 well plate (duplicates, A3/B3, C3/D3, E3/F3, G3/H3)
p200.distribute(
    50,
    tuberack.wells('C2', 'D2', 'A3', 'B3'),
    plate.cols('3'))

# fill columns 4 to 11 with 25 uL of dilutent each
m50.distribute(
    25,
    trough['A1'],
    plate.cols('4', length=8))

# dilute samples down all columns
m50.pick_up_tip()

m50.transfer(
    25,
    plate.cols('3', length=8),
    plate.cols('4', length=8),
    mix_after=(3, 25),
    new_tip='never')

# remove 25uL from last row
m50.aspirate(25, plate.cols('11')).dispense(trash)
m50.drop_tip()

# fill rows 1 to 11 with 200 uL of Bradford reagent
m50.transfer(200, trough['A2'], plate.cols('1', length=11))
