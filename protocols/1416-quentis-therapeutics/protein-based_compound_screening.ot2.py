from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Protein-based Compound Screening',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

plate_name = 'corning-384-well-standard-flat'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        depth=14.5,
        diameter=3.63
        )

# labware setup
plate_1 = labware.load(plate_name, '1')
plate_2 = labware.load(plate_name, '2')
for plate in [plate_1, plate_2]:
    for well in plate.wells():
        well.properties['height'] = 11.6

trough = labware.load('trough-12row', '4')

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['3', '5', '7', '8']]
tiprack_50 = labware.load('opentrons-tiprack-300ul', '6')

# instrument setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks_10)

m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tiprack_50])

# reagent setup
DMSO = trough.wells('A1')
buff = trough.wells('A2')
protein = trough.wells('A3')
substrate = trough.wells('A4')

# add DMSO to column 2-16
m50.distribute(
    10,
    DMSO,
    [col[0] for col in plate_1.cols('2', to='16')],
    disposal_vol=0)

# perform serial dilutions
sources = [col[0] for col in plate_1.cols('1', to='15')]
dests = [col[0] for col in plate_1.cols('2', to='16')]
m10.pick_up_tip()
for source, dest in zip(sources, dests):
    m10.transfer(5, source, dest, new_tip='never')
    m10.mix(5, 10, dest)
    m10.blow_out(dest)
m10.drop_tip()

# transfer dilutions down 1 row
sources = [col[0] for col in plate_1.cols('1', to='16')]
dests = [col[1] for col in plate_1.cols('1', to='16')]
for source, dest in zip(sources, dests):
    m10.pick_up_tip()
    m10.transfer(2, source, dest, new_tip='never')
    m10.blow_out(dest.top())
    m10.drop_tip()

# distribute buffer at top of wells
dests = [col[1].top() for col in plate_1.cols('1', to='16')]
m50.transfer(98, buff, dests)

# mix compound and buffer and transfer in duplicate to new plate
sources = [col[1] for col in plate_1.cols('1', to='16')]
dests = [col[:2] for col in plate_2.cols('1', to='16')]
for source, dest in zip(sources, dests):
    m10.pick_up_tip()
    m10.mix(3, 10, source)
    m10.transfer(10, source, [well for well in dest], new_tip='never')
    m10.drop_tip()

# distribute protein to each well from right to left, change tip between rows
dests = [[col[index] for col in plate_2.cols[15::-1]] for index in range(2)]
for dest in dests:
    m10.pick_up_tip()
    m10.distribute(5, protein, dest, disposal_vol=0, new_tip='never')
    m10.drop_tip()

robot.pause('Remove plate in slot 2 and spin it down. Place the plate back in \
slot 2.')

# distribute substrate to each well from right to left, change tip between rows
for dest in dests:
    m10.pick_up_tip()
    m10.distribute(5, substrate, dest, disposal_vol=0, new_tip='never')
    m10.drop_tip()
