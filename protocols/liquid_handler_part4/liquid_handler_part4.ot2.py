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

m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack1])

# transfer biological dye to columns 12-1 of all plates
m50.pick_up_tip()
for plate in plates:
    m50.distribute(
        12, trough.wells('A1'), plate.cols('12', to='1'), new_tip='never')
m50.drop_tip()
