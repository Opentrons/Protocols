from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Colorimetric Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tube_rack_1 = labware.load('tube-rack-2ml', '3')
tube_rack_2 = labware.load('tube-rack-2ml', '6')
tip_rack_200_s = labware.load('tiprack-200ul', '7')
tip_racks_200_m = [labware.load('tiprack-200ul', slot) for slot in ['9', '10']]
trough = labware.load('trough-12row', '8')
plate = labware.load('96-PCR-flat', '11')

# pipettes
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tip_rack_200_s]
    )

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tip_racks_200_m
    )

# creates a list of 32 sets of wells in triplicate corresponding to a max
# of 32 samples to be transferred
wells = [r[(c*3):(c*3+3)] for c in range(4) for r in plate.rows()]

# creates a list of 48 wells from both tube racks ordering across rows and
# then down columns
tubes_1 = [tube for row in tube_rack_1.rows() for tube in row]
tubes_2 = [tube for row in tube_rack_2.rows() for tube in row]
tubes_total = tubes_1 + tubes_2


def run_custom_protocol(
        sample_num: int = 32,
        sample_vol: int = 175,
        solution_vol_1: int = 50,
        solution_vol_2: int = 50
        ):

    for i in range(sample_num):
        p300.distribute(sample_vol, tubes_total[i], wells[i])

    # transfers solution 1 all columns of samples
    num_transfers = (math.ceil(sample_num/8))*3
    for col in range(num_transfers):
        m300.transfer(
                solution_vol_1,
                trough.wells('A1'),
                plate.rows['A'][col],
                mix_after=(3, 50)
                )

    # transfers solution 12 to all columns of samples
    for col in range(num_transfers):
        m300.transfer(
                solution_vol_2,
                trough.wells('A12'),
                plate.rows['A'][col],
                mix_after=(3, 50)
                )


run_custom_protocol()
