from opentrons import labware, instruments

metadata = {
    'protocolName': '24- to 96-Well Plate Consolidation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name_96 = 'USA-Scientific-96-deepwell'
if plate_name_96 not in labware.list():
    labware.create(plate_name_96,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=8.2,
                   depth=41.3,
                   volume=2000)

plate_name_24 = 'EnzyScreen-24-deepwell'
if plate_name_24 not in labware.list():
    labware.create(plate_name_24,
                   grid=(6, 4),
                   spacing=(18, 18),
                   diameter=17,
                   depth=40,
                   volume=11000)

# load labware
source_plates = [labware.load(plate_name_24, slot)
                 for slot in ['1', '2', '4', '5']]
dest_plate = labware.load(plate_name_96, '3')


def run_custom_protocol(transfer_volume: float = 100.0):

    # set up pipettes
    if transfer_volume >= 30:
        tips = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['7', '8']]
        pipette = instruments.P300_Multi(mount='right', tip_racks=tips)
    else:
        tips = [labware.load('tiprack-10ul', slot)
                for slot in ['7', '8']]
        pipette = instruments.P300_Single(mount='right', tip_racks=tips)

    sources = [well for plate in source_plates for well in plate.rows('A')]
    dests = [well for row in dest_plate.rows('A', length=2) for well in row]

    pipette.transfer(transfer_volume, sources, dests, new_tip='always')
