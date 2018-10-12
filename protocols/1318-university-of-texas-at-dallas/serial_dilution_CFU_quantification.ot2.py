from opentrons import labware, instruments, robot

# labware setup
trough = labware.load('trough-12row', '1')
plate = labware.load('96-flat', '2')
tiprack_50 = labware.load('opentrons-tiprack-300ul', '4')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])


# make sure to take the first tip off the tiprack
m300.distribute(180, trough.wells('A1'), plate.cols())

for col in plate.cols():
    for well in col[:-1]:
        p50.transfer(20, well, next(well), mix_after=(5, 50))
