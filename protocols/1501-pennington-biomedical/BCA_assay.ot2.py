from opentrons import labware, instruments

metadata = {
    'protocolName': 'BCA Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tube_rack_1 = labware.load('tube-rack-2ml', slot='3')
tube_rack_2 = labware.load('tube-rack-2ml', slot='6')
tip_rack_200 = [labware.load('tiprack-200ul', slot) for slot in ['7', '10']]
trough = labware.load('trough-12row', slot='8')
plate = labware.load('96-PCR-flat', slot='11')

# pipettes
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=tip_rack_200
    )

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tip_rack_200
    )


"""
create_tube_order outputs the well indices of a 24-well tube rack ordering
across rows and then down columns
"""


def create_tube_order():
    new_ind = []
    for row in range(4):
        for col in range(6):
            new_ind.append(col*4 + row)
    return new_ind


def run_custom_protocol(
        sample_num: int = 32):

    # creates a list of 32 sets of wells in triplicate corresponding to a max
    # of 32 samples to be transferred
    well_order = []
    for move in range(4):
        for row in range(8):
            triplicate_block = [row+move*24, row+move*24+8, row+move*24+16]
            well_order.append(triplicate_block)

    # creates a list of 48 wells from both tube racks ordering across rows and
    # then down columns
    tubes_1 = [tube for tube in tube_rack_1.wells(create_tube_order())]
    tubes_2 = [tube for tube in tube_rack_2.wells(create_tube_order())]
    tubes_temp = tubes_1 + tubes_2
    tubes_total = tubes_temp[0:sample_num]

    # distributes each sample to 96-well plate in triplicate for user-input
    # number of samples
    for sample, target in zip(tubes_total, well_order):
        wells = [well for well in plate(target)]
        p300.distribute(30, sample, wells)

    # transfers solution from trough to corresponding column of samples
    num_transfers = (int((sample_num-1)/8)+1)*3
    for col in range(num_transfers):
        m300.transfer(
                200,
                trough.wells('A1'),
                plate.rows['A'][col],
                mix_after=(3, 75)
                )
