from opentrons import labware, instruments


def run_custom_protocol(transfer_volume: int=20):

    if 'custom-resevoir' not in labware.list():
        labware.create(
             'custom-resevoir',
             grid=(1, 1),
             spacing=(63.88, 0),
             depth=25.5,
             diameter=2)

    reagent = labware.load('custom-resevoir', '4')
    transfer_plate = labware.load('384-plate', '2')
    tiprack10 = labware.load('tiprack-10ul', '5')
    tiprack = labware.load('opentrons-tiprack-300ul', '3')

    if transfer_volume >= 50:
        multichannel = instruments.P300_Multi(
                mount='left', tip_racks=[tiprack])
    else:
        multichannel = instruments.P50_Multi(mount='left', tip_racks=[tiprack])
    p10 = instruments.P10_Single(mount='right', tip_racks=[tiprack10])

    alternating_wells_samples = []
    for col1 in transfer_plate.columns('2', to='16'):
        alternating_wells_samples.append(col1.wells('A'))
        alternating_wells_samples.append(col1.wells('B'))

    multichannel.transfer(
        transfer_volume,
        reagent,
        alternating_wells_samples,
        new_tip='once')

    alternating_wells_reagent = []
    for column in transfer_plate.columns('17', to='23'):
        alternating_wells_reagent.append(
            column.wells('A', 'B', 'C', 'D', 'E', 'F'))

    p10.transfer(
        transfer_volume, reagent, alternating_wells_reagent, new_tip='once')
