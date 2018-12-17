from opentrons import labware, instruments

metadata = {
    'protocolName': 'Serial Dilution of Inhibitor in Media',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }

# labware setup
trough = labware.load('trough-12row', '1')
plate = labware.load('96-deep-well', '2')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '4')
tiprack_50 = labware.load('opentrons-tiprack-300ul', '6')


# instruments setup
m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tiprack_50])

p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack_300])

# reagent setup
solution_1 = trough.wells('A1')
solution_2 = trough.wells('A2')
samples = trough.wells('A3', length=4)

m50.transfer(250, solution_1, plate.cols())

for col in plate.cols():
    p300.pick_up_tip()
    p300.transfer(250, solution_2, col[0], new_tip='never')
    p300.mix(3, 300, col[0])
    for source, dest in zip(
            col.wells('A', to='F'), col.wells('B', to='G')):
        p300.transfer(250, source, dest, new_tip='never')
        p300.mix(3, 300, dest)
    p300.transfer(250, col.wells('G'), p300.trash_container.top(),
                  new_tip='never')
    p300.drop_tip()

for sample, dest in zip(
        samples, [plate.cols(index, length=3) for index in range(0, 12, 3)]):
    m50.distribute(20, sample, [col[0] for col in dest], disposal_vol=0)
