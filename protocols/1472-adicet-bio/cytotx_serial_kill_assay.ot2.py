from opentrons import labware, instruments

metadata = {
    'protocolName': 'Cytotox Serial-Kill Assay',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate_name = 'corning-384-well'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.63,
        depth=11.56
        )

# labware setup
plate = labware.load('384-plate', '1')
tipracks = [labware.load('opentrons-tiprack-300ul', slot)
            for slot in ['2', '3', '4', '5', '6', '8', '9']]
fresh_media = labware.load('96-deep-well', '7')
waste_media = labware.load('96-deep-well', '10')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks)


source = [col[index].top(-8.35)
          for col in plate.cols('2', to='23') for index in range(1, 3)]

m300.set_flow_rate(aspirate=40)
m300.consolidate(40, source, waste_media.cols('1'))

for col in plate.cols('2', to='23'):
    for index, drug in zip(range(1, 3), fresh_media.cols('1', '2')):
        m300.pick_up_tip()
        m300.transfer(40, drug, col[index].top(-8.35), new_tip='never')
        m300.mix(10, 40, col[index])
        m300.blow_out(col[index].top(-8.35))
        m300.drop_tip()
