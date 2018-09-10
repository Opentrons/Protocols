from opentrons import labware, instruments

plates = [
    labware.load('96-flat', '1'),
    labware.load('96-flat', '2'),
    labware.load('96-flat', '3'),
    labware.load('96-flat', '4'),
    labware.load('96-flat', '5'),
    labware.load('96-flat', '6'),
    labware.load('96-flat', '7')
    ]

trough = labware.load('trough-12row', '10')

tiprack1 = labware.load('tiprack-200ul', '8')
tiprack2 = labware.load('tiprack-200ul', '9')

m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack1, tiprack2])

# transfer culture media to columns 2-9 of all plates
m50.pick_up_tip(tiprack1.cols('1'))
for plate in plates:
    m50.distribute(
        20, trough.wells('A7'), plate.cols('1', to='9'), new_tip='never')
m50.drop_tip()

# transfer culture media to columns G10-H10
m50.pick_up_tip(tiprack1.cols('5'))
m50.distribute(
    20,
    trough.wells('A7'),
    [plate.cols('10') for plate in plates],
    new_tip='never')
m50.drop_tip()

# transfer fungal inoculum to column 11 of all plates
m50.start_at_tip(tiprack1.cols('2'))
m50.distribute(
    20,
    trough.wells('A1'),
    [plate.cols('11') for plate in plates],
    new_tip='once')

# transfer fungal inoculum to A10-F10 of all plates
m50.distribute(
    20,
    trough.wells('A1'),
    [plate.cols('10') for plate in plates],
    new_tip='once')

# transfer fungal inoculum to B9-D9, F9-H9 of all plates
m50.distribute(
    20,
    trough.wells('A1'),
    [plate.cols('9') for plate in plates],
    new_tip='once')
