from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Cell Painting',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

reservior_4_name = 'agilent-trough-4row'
if reservior_4_name not in labware.list():
    labware.create(
        reservior_4_name,
        grid=(4, 1),
        spacing=(27, 0),
        diameter=26,
        depth=42)

reservoir_1_name = 'agilent-trough-1row'
if reservoir_1_name not in labware.list():
    labware.create(
        reservoir_1_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=39)

# labware setup
reservoir = labware.load(reservior_4_name, '5')
plate = labware.load('96-flat', '2')
pbs1 = labware.load(reservoir_1_name, '3').wells('A1')
pbs2 = labware.load(reservoir_1_name, '6').wells('A1')
pbs3 = labware.load(reservoir_1_name, '9').wells('A1')
wc1 = labware.load(reservoir_1_name, '1').wells('A1')
wc2 = labware.load(reservoir_1_name, '4').wells('A1')
wc3 = labware.load(reservoir_1_name, '7').wells('A1')
wc4 = labware.load(reservoir_1_name, '10').wells('A1')
tiprack = labware.load('tiprack-200ul', '8')

# instruments setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])

# reagent setup
mitotracker = reservoir.wells('A1')
pfa = reservoir.wells('A2')
triton = reservoir.wells('A3')
staining_sol = reservoir.wells('A4')

targets = plate.cols('2', to='11')

# mix mitotracker, remove plate contents, add mitotracker
m300.pick_up_tip()
m300.mix(5, 300, mitotracker)
m300.consolidate(70, targets, wc1.top(), new_tip='never')
m300.distribute(30, mitotracker, targets, disposal_vol=0, new_tip='never')
m300.drop_tip(wc2.top())

robot.pause("Pause for 30 minutes. Resume when you are ready.")

# remove plate contents, wash plate with PBS 1 twice, add PFA
m300.pick_up_tip()
m300.consolidate(30, targets, wc1.top(), new_tip='never')
for _ in range(2):
    m300.distribute(60, pbs1, targets, disposal_vol=0, new_tip='never')
    m300.consolidate(60, targets, wc1.top(), new_tip='never')
m300.distribute(50, pfa, targets, disposal_vol=0, new_tip='never')

m300.delay(minutes=20)

# remove plate contents, wash plate with PBS 2 twice
m300.consolidate(50, targets, wc3.top(), new_tip='never')
for _ in range(2):
    m300.distribute(60, pbs2, targets, disposal_vol=0, new_tip='never')
    m300.consolidate(60, targets, wc3.top(), new_tip='never')
m300.drop_tip(wc4.top())

# mix and add triton
m300.pick_up_tip()
m300.mix(3, 300, triton)
m300.distribute(50, triton, targets, disposal_vol=0, new_tip='never')

m300.delay(minutes=20)

# remove plate contents, wash plate with PBS 1 twice
m300.consolidate(50, targets, wc1.top(), new_tip='never')
for _ in range(2):
    m300.distribute(60, pbs1, targets, disposal_vol=0, new_tip='never')
    m300.consolidate(60, targets, wc1.top(), new_tip='never')
m300.drop_tip(wc2.top())

# mix and addstaining solution
m300.pick_up_tip()
m300.mix(5, 300, staining_sol)
m300.distribute(50, staining_sol, targets, disposal_vol=0, new_tip='never')

robot.pause("Resume when you are ready.")

# remove plate contents, wash plate with twice with PBS 3
m300.transfer(50, targets, wc1.top(), new_tip='never')
for _ in range(2):
    m300.distribute(60, pbs3, targets, disposal_vol=0, new_tip='never')
    m300.consolidate(60, targets, wc1.top(), new_tip='never')
m300.drop_tip(wc2.top())

# add PBS 3
m300.pick_up_tip()
m300.distribute(90, pbs3, targets, disposal_vol=0, new_tip='never')
m300.drop_tip(wc2.top())
