from opentrons import labware, instruments

metadata = {
    'protocolName': 'Dilution Series for Biophysical Assays',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
trough = labware.load('trough-12row', '1')
plate = labware.load('96-flat', '2')
tiprack = labware.load('tiprack-200ul', '4')

# reagent setup
buffer = trough.wells('A1')
solvent = trough.wells('A2')

# instruments setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])

m300.distribute(90, buffer, plate.cols())

m50.pick_up_tip(tiprack.cols('2'))
m50.transfer(10, solvent, plate.cols('1'), new_tip='never')
m50.mix(5, 50, plate.cols('1'))
for source, dest in zip(plate.cols('1', to='5'), plate.cols('2', to='6')):
    m50.transfer(50, source, dest, new_tip='never')
    m50.mix(5, 50, dest)
m50.drop_tip()
