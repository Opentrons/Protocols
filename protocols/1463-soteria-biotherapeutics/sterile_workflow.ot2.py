from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Sterile Workflow',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate_name = 'falcon-96-well-u-bottom'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.85,
        depth=10.59
        )

# labware setup
assay_plate = labware.load(plate_name, '1')
dd_plate = labware.load('96-deep-well', '4')
trough = labware.load('trough-12row', '2')
tiprack_50 = labware.load('tiprack-200ul', '5')
tiprack_300 = labware.load('tiprack-200ul', '6')

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
cells = trough.wells('A1')
growth_media = trough.wells('A2')
stimulation_media = trough.wells('A3')
drug_A = dd_plate.wells('A11', to='C1')
drug_B = dd_plate.wells('A12', to='C12')

m300.transfer(900, growth_media, dd_plate.cols('1', to='10'))

for drug_1, drug_2, row in zip(drug_A, drug_B, dd_plate.rows('A', 'B', 'C')):
    p50.pick_up_tip()
    p50.transfer(50, drug_1, row.wells('10'), new_tip='never')
    p50.mix(5, 50, row.wells('10'))
    p50.drop_tip()

    p50.pick_up_tip()
    p50.transfer(50, drug_2, row.wells('10'), new_tip='never')
    p50.mix(5, 50, row.wells('10'))
    p50.drop_tip()

    p50.pick_up_tip()
    for source, dest in zip(row.wells('10', to='3'), row.wells('9', to='2')):
        p50.transfer(100, source, dest, new_tip='never')
        p50.mix(5, 50, dest)
    p50.drop_tip()

m300.pick_up_tip()
m300.mix(10, 300, cells)
m300.distribute(33, cells, assay_plate.cols('2', to='11'), new_tip='never')
m300.drop_tip()

m300.transfer(33, dd_plate.cols('1', to='10'), assay_plate.cols('2', to='11'))

robot.pause("Transfer plates to the incubator for 10 minutes. Resume after \
returning the Assay Plate back in slot 2.")

m300.distribute(
    33,
    stimulation_media,
    [col[0].top() for col in assay_plate.cols('2', to='11')],
    blow_out=stimulation_media)
