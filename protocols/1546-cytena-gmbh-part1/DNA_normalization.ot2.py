from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'DNA Normalization',
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
tips10 = labware.load('tiprack-10ul', '7')
tips300 = labware.load('opentrons-tiprack-300ul', '8')

# pipettes
m10 = instruments.P10_Multi(mount='right', tip_racks=[tips10])
m300 = instruments.P300_Multi(mount='left', tip_racks=[tips300])

# reagent setup
solution = trough.wells('A8')

# transfer working solution to flat plate
m300.distribute(75, solution, [well.top() for well in flat_plate.rows('A')])

# transfer DNA from PCR plate to corresponding well of flat plate
for source_col, dest_col in zip(PCR_plate.columns('2', to='12'),
                                flat_plate.columns('2', to='12')):
    source = source_col[0]
    dest = dest_col[0]

    m10.pick_up_tip()
    m10.transfer(3, source, dest, blow_out=True, new_tip='never')
    m10.touch_tip(dest)
    m10.drop_tip()

tip_sources = tips10.wells('H12', to='F12')
for (tip, source, dest) in zip(tip_sources,
                               PCR_plate.wells('F1', length=3),
                               flat_plate.wells('F1', length=3)):
    m10.pick_up_tip(tip)
    m10.transfer(3,
                 source,
                 dest,
                 blow_out=True,
                 new_tip='never')
    m10.touch_tip(dest)
    m10.drop_tip()

robot.pause('Replace the 96-flat plate with a new empty 96-flat plate before '
            'resuming.')

m300.pick_up_tip(tips300.wells('G12'))
dests = [well.top() for well in flat_plate.rows('A')][0:5]
m300.distribute(75, solution, dests, blow_out=True, new_tip='never')
m300.drop_tip()

for (tip, source, dest) in zip(tips10.wells('E12', to='A12'),
                               PCR_plate.wells('A2', length=5),
                               flat_plate.wells('A2', length=5)):
    m10.pick_up_tip(tip)
    m10.transfer(3,
                 source,
                 dest,
                 blow_out=True,
                 new_tip='never')
    m10.touch_tip(dest)
    m10.drop_tip()
