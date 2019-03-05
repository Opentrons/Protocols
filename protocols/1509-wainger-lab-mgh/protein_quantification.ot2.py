from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Protein Quantification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware
tipslots = ['1', '2', '3', '4', '5', '6']
tips300 = [labware.load('opentrons-tiprack-300ul', s) for s in tipslots]
trough = labware.load('trough-12row', '7')
plate = labware.load('96-PCR-flat', '8')

# pipettes
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tips300
)

# set up list of plate well tops and trough columns
plate_tops = [col for col in plate.rows('A')]

# dispose of 180ul from all wells
m300.transfer(180, plate_tops, m300.trash_container.top(), new_tip='always')

# add 60ul from trough column 1 to all wells
m300.transfer(60,
              trough.wells('A1'),
              [well.top() for well in plate_tops],
              blow_out=True)

# pause and prompt user to resume when ready
robot.pause('Waiting to resume second part of protocol')

# dispose of 70ul from all wells of plate
m300.transfer(70, plate_tops, m300.trash_container.top(), new_tip='always')

# perform following wash step twice
for _ in range(2):
    # for each of troughs columns 4-12, transfer 140ul to all plate wells
    for col in trough.rows['A']['4':]:
        m300.transfer(140,
                      col,
                      [well.top() for well in plate_tops],
                      blow_out=True)
    # dispose of 150ul from all wells
    m300.transfer(150, plate_tops, m300.trash_container.top(),
                  new_tip='always')

# add 60ul from trough column 3 to all wells
m300.transfer(60,
              trough.wells('A3'),
              [well.top() for well in plate_tops],
              blow_out=True)
