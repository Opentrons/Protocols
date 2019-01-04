from opentrons import labware, instruments

metadata = {
 'protocolName': 'Transfer serial dilution to 384 WP',
 'author': 'Laura <protocols@opentrons.com>',
 'source': 'Custom Protocol Request'
}


def run_custom_protocol(transfer_volume: int=20):
    if 'custom-resevoir' not in labware.list():
        labware.create(
             'custom-resevoir',
             grid=(1, 1),
             spacing=(63.88, 0),
             depth=25.5,
             diameter=2)
    initial_plate = labware.load('96-flat', '1')
    transfer_plate = labware.load('384-plate', '2')
    reagent = labware.load('custom-resevoir', '4')
    tiprack10 = labware.load('tiprack-10ul', '5')
    tiprack = labware.load('opentrons-tiprack-300ul', '3')

    if transfer_volume >= 50:
        multichannel = instruments.P300_Multi(
                mount='left', tip_racks=[tiprack])
    else:
        multichannel = instruments.P50_Multi(mount='left', tip_racks=[tiprack])
    p10 = instruments.P10_Single(mount='right', tip_racks=[tiprack10])

    alternating_wells_samples = []
    for col1, col2 in zip(
            transfer_plate.columns('2', length=7),
            transfer_plate.columns('10', length=7)):
        alternating_wells_samples.append(col1.wells('A'))
        alternating_wells_samples.append(col1.wells('B'))

        alternating_wells_samples.append(col2.wells('A'))
        alternating_wells_samples.append(col2.wells('B'))

    multichannel.transfer(
        transfer_volume,
        initial_plate.columns('2', length=7),
        alternating_wells_samples)

    alternating_wells_reagent = []
    for col1 in transfer_plate.columns('9', '16'):
        alternating_wells_reagent.append(col1.wells('A'))
        alternating_wells_reagent.append(col1.wells('B'))

    multichannel.transfer(
        transfer_volume, reagent, alternating_wells_reagent, new_tip='once')

    p1_wells = [well
                for column in transfer_plate.columns('17', '18')
                for well in column.wells('B', 'C')]
    p10.transfer(
        transfer_volume,
        initial_plate.columns('11')[0],
        p1_wells,
        new_tip='once')

    p2_wells = [well
                for column in transfer_plate.columns('17', '18')
                for well in column.wells('D', 'E')]
    p10.transfer(
        transfer_volume,
        initial_plate.columns('11')[1],
        p2_wells,
        new_tip='once')

    p3_wells = [well
                for column in transfer_plate.columns('21', '22')
                for well in column.wells('B', 'C')]
    p10.transfer(
        transfer_volume,
        initial_plate.columns('11')[2],
        p3_wells,
        new_tip='once')

    p4_wells = [well
                for column in transfer_plate.columns('21', '22')
                for well in column.wells('D', 'E')]
    p10.transfer(
        transfer_volume,
        initial_plate.columns('11')[3],
        p4_wells,
        new_tip='once')

    reagent_wells = [well
                     for row in transfer_plate.rows('A', 'F')
                     for well in row[16:23]]
    reagent_columns = [well
                       for column in transfer_plate.columns('23')
                       for well in column[1:5]]
    reagent_wells = reagent_wells + reagent_columns
    p10.transfer(transfer_volume, reagent, reagent_wells, new_tip='once')
