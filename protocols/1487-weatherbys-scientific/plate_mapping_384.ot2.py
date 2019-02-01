from opentrons import labware, instruments

metadata = {
    'protocolName': 'Plate Mapping',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

tiprack_name = 'tipone-starlab-tiprack-100ul'
if tiprack_name not in labware.list():
    labware.create(
        tiprack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60)


# labware setup
output = labware.load('384-plate', '2')
deep_plates = [labware.load('96-deep-well', slot)
               for slot in ['1', '3', '4', '6']]
tipracks = [labware.load(tiprack_name, slot)
            for slot in ['5', '7', '8', '9']]

# instruments setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=tipracks)


def run_custom_protocol(transfer_volume: float=50):

    dests_1 = [col[0] for col in output.cols[::2]]
    dests_2 = [col[0] for col in output.cols[1::2]]
    dests_3 = [col[1] for col in output.cols[::2]]
    dests_4 = [col[1] for col in output.cols[1::2]]

    dests = [dests_1, dests_2, dests_3, dests_4]

    for plate, dest in zip(deep_plates, dests):
        for source_col, dest_col in zip(plate.cols(), dest):
            m50.transfer(transfer_volume, source_col, dest_col)
