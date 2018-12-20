from opentrons import labware, instruments

metadata = {
    'protocolName': 'Cell Culture',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

reservoir_name = 'biotix-reservoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=23)

microplate_name = 'greiner-384-square-1'
if microplate_name not in labware.list():
    labware.create(
        microplate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.7,
        depth=11.5)

# labware setup
destination = [labware.load(microplate_name, slot)
               for slot in ['1', '2', '4', '5', '7', '8', '10', '11']]
for plate in destination:
    plate.properties['height'] = 14.5

medium = labware.load(reservoir_name, '3', 'Medium').wells('A1')
cells = labware.load(reservoir_name, '6', 'Cells').wells('A1')


tiprack = labware.load('opentrons-tiprack-300ul', '9')

# instruments setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])


def run_custom_protocol(
        medium_volume: float=50,
        cell_volume: float=50,
        number_of_plates: int=8):

    if number_of_plates > 8:
        raise Exception("Number of plates must be 1-8.")

    # transfer medium
    multi_dest = [plate.cols(col_num)[index]
                  for plate in destination[:number_of_plates]
                  for col_num in ['1', '12']
                  for index in range(2)]
    m300.distribute(medium_volume, medium, multi_dest, disposal_vol=0)

    p300.start_at_tip(tiprack.wells('A4'))
    single_dest = [well
                   for plate in destination[:number_of_plates]
                   for row_alpha in ['A', 'P']
                   for well in plate.rows(row_alpha).wells('2', to='23')]
    p300.distribute(medium_volume, medium, single_dest, disposal_vol=0)

    # transfer cells
    count = 0
    m300.pick_up_tip()
    for plate in destination:
        for col_num in range(1, 23):
            well_num = 0
            if count == 0 or count % 5 == 0:
                m300.mix(3, 100, cells)
            count += 1
            m300.transfer(
                cell_volume,
                cells,
                plate.cols(col_num)[well_num],
                new_tip='never')
    m300.drop_tip()

    # transfer cells
    count = 0
    m300.pick_up_tip()
    for plate in destination:
        for col_num in range(1, 23):
            well_num = 1
            if count == 0 or count % 5 == 0:
                m300.mix(3, 100, cells)
            count += 1
            m300.transfer(
                cell_volume,
                cells,
                plate.cols(col_num)[well_num],
                new_tip='never')
    m300.drop_tip()
