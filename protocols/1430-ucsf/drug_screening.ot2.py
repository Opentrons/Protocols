from opentrons import labware, instruments

# labware setup
plate = labware.load('96-flat', '2')
trough = labware.load('trough-12row', '4')
tipracks = [labware.load('tiprack-200ul', slot)
            for slot in ['1', '3']]

# instruments setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)

# remove solution from columns and add drug
for index in range(0, 12, 3):
    m300.consolidate(
        150, plate.cols(index, length=3), m300.trash_container.top())
    m300.distribute(
        150, trough.wells(index), plate.cols(index, length=3), disposal_vol=0)

m300.delay(minutes=30)

# remove drug from columns and add new drug
for index in range(0, 12, 3):
    m300.consolidate(
        150, plate.cols(index, length=3), m300.trash_container.top())
    m300.distribute(
        150, trough.wells('A5'), plate.cols(index, length=3), disposal_vol=0)
