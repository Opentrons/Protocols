from opentrons import labware, instruments, robot

# create custom labware
tuberack_name = 'custom-pyrotube-rack'
if tuberack_name not in labware.list():
    labware.create(
        tuberack_name,
        grid=(6, 4),
        spacing=(20, 20),
        diameter=11.8,
        depth=75)

# labware setup
SP = labware.load('96-flat', '4', 'Source Plate')
destination = labware.load('96-flat', '5', 'Destination Plate')
tuberack = labware.load(tuberack_name, '6')
trough = labware.load('trough-12row', '2')

# reagent setup
RGW = tuberack.wells('A1')
APTS = tuberack.wells('B1')
BG_STD = tuberack.wells('C1')
fungitell = trough.wells('A1')

tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['7', '8']]
tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['9', '10']]

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks_50)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_300)

# create standard curve
STDs = [well for well in SP.wells('C2', 'D2', 'E2', 'F2')]


# remove A, B, G, H from col 1 of 300 uL tiprack
p50.transfer(100, RGW, SP.cols('2').wells('C', 'D', 'E', 'F'))
p50.pick_up_tip()
p50.transfer(100, BG_STD, SP.wells('B2'), new_tip='never')
p50.transfer(100, BG_STD, STDs[0], new_tip='never')
p50.mix(5, 50, STDs[0])
for source, dest in zip(STDs[0:3], STDs[1:]):
    p50.transfer(100, source, dest, new_tip='never')
    p50.mix(5, 50, dest)
p50.drop_tip()


# addition of standard curve concentrations in duplicate
dests = [[destination[i], destination[i+1]] for i in range(0, 10, 2)]
sources = SP.wells('B2', to='F2')

for source, dest in zip(sources, dests):
    p50.pick_up_tip()
    p50.distribute(25, source, dest, new_tip='never')
    p50.drop_tip()

# addition of negative controls
p50.distribute(25, RGW, [well for well in SP.wells('C2', 'D2')])

# patient serum transfer
dests = [[destination[i], destination[i+1]] for i in range(12, 30, 2)]
dests += [[destination[i], destination[i+1]] for i in range(32, 55, 2)]

sources = [well for col in SP.cols('5', to='7') for well in col[1:7]]
sources += [well for well in SP.cols('8')[1:4]]

p50.set_flow_rate(aspirate=10, dispense=15)

for source, dest in zip(sources, dests):
    p50.distribute(5, source, dest)

p50.set_flow_rate(aspirate=25, dispense=50)
# alkaline pre-treatment addition
all_wells = [well for subdests in dests for well in subdests]
p50.pick_up_tip()
for well in all_wells:
    if p50.current_volume <= 20:
        p50.aspirate(APTS)
    p50.dispense(20, well.top())
p50.drop_tip()

robot.pause("Off robot: Sequence Hold for Alkaline Pre-treatment of Serum \
Samples and Fungitell Reconstitution.")

# fungitell addition
for col in destination.cols('1', to='7'):
    m300.transfer(100, fungitell, col)
