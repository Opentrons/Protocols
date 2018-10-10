from opentrons import labware, instruments

# labware setup
plate_1 = labware.load('96-flat', '1')
plate_2 = labware.load('96-flat', '2')
plate_3 = labware.load('96-flat', '4')
plate_4 = labware.load('96-flat', '5')
output_384 = labware.load('384-plate', '3')

tipracks = [labware.load('opentrons-tiprack-300ul', slot)
            for slot in ['6', '7', '8', '9', '10', '11']]


def run_custom_protocol(transfer_volume: float=300):

    if transfer_volume > 50:
        pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=tipracks)
    else:
        pipette = instruments.P50_Multi(
            mount='right',
            tip_racks=tipracks)

    dest_1 = [well for well in output_384.rows(0)[::2]]
    for source, dest in zip(plate_1, dest_1):
        pipette.transfer(transfer_volume, source, dest)

    dest_2 = [well for well in output_384.rows(0)[1::2]]
    for source, dest in zip(plate_2, dest_2):
        pipette.transfer(transfer_volume, source, dest)

    dest_3 = [well for well in output_384.rows(1)[::2]]
    for source, dest in zip(plate_3, dest_3):
        pipette.transfer(transfer_volume, source, dest)

    dest_4 = [well for well in output_384.rows(1)[1::2]]
    for source, dest in zip(plate_4, dest_4):
        pipette.transfer(transfer_volume, source, dest)
