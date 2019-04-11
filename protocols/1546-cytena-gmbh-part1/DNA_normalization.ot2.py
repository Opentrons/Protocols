from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'CSV Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
PCR_plate_name = 'FrameStar-96-PCR'
if PCR_plate_name not in labware.list():
    labware.create(
        PCR_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.50,
        depth=15.10,
        volume=200
    )

flat_plate_name = '4titude-96-flat'
if flat_plate_name not in labware.list():
    labware.create(
        flat_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.3,
        depth=10.8,
        volume=350
    )

# load labware
trough = labware.load('trough-12row', '1')
PCR_plate = labware.load(PCR_plate_name, '2')
flat_plate = labware.load(flat_plate_name, '3')
tips10 = labware.load('tiprack-10ul', '4')
tips300 = labware.load('opentrons-tiprack-300ul', '5')

# pipettes
p10 = instruments.P10_Single(mount='right', tip_racks=[tips10])
p300 = instruments.P300_Single(mount='left', tip_racks=[tips300])

# reagent setup
solution = trough.wells('A8')

# transfer working solution to flat plate
p300.distribute(75, solution, [well.top() for well in flat_plate.wells()])

# transfer DNA from PCR plate to corresponding well of flat plate
for source_col, dest_col in zip(PCR_plate.columns('2', to='12'),
                                flat_plate.columns('2', to='12')):
    for source, dest in zip(source_col, dest_col):
        p10.pick_up_tip()
        p10.transfer(3, source, dest, blow_out=True, new_tip='never')
        p10.touch_tip(dest)
        p10.drop_tip()

for source, dest in zip(PCR_plate.wells('F1', length=3),
                        flat_plate.wells('F1', length=3)):
    p10.pick_up_tip()
    p10.transfer(3,
                 source,
                 dest,
                 blow_out=True,
                 new_tip='never')
    p10.touch_tip(dest)
    p10.drop_tip()

robot.pause('Replace the 96-flat plate with a new empty 96-flat plate before '
            'resuming.')

p300.pick_up_tip()
for row in flat_plate.rows('A', length=5):
    p300.transfer(75, solution, row[0:2], new_tip='never')
p300.drop_tip()

for source, dest in zip(PCR_plate.wells('A2', length=5),
                        flat_plate.wells('A2', length=5)):
    p10.pick_up_tip()
    p10.transfer(3,
                 source,
                 dest,
                 blow_out=True,
                 new_tip='never')
    p10.touch_tip(dest)
    p10.drop_tip()
