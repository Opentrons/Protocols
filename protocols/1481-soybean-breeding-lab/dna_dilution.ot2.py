from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'DNA Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

csv_example = """
Samples,DNA VOLUME OF STOCK,H2O VOLUME OF STOCK,WELL
SOY1,1.17,98.83,A1
SOY2,1.99,98.01,A2
SOY3,1.80,98.20,A3
SOY4,1.56,98.44,A4
SOY5,3.76,96.24,A5
SOY6,1.66,98.34,A6
SOY7,2.32,97.68,A7
SOY8,1.55,98.45,A8
SOY9,1.33,98.67,A9
SOY10,1.79,98.21,A10
"""


def csv_to_lists(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    dna_vols, water_vols, dests = [], [], []
    for line in info_list[1:]:
        dna_vol = round(float(line[1]), 1)
        water_vol = round(float(line[2]), 1)
        dest = line[3]

        dna_vols.append(dna_vol)
        water_vols.append(water_vol)
        dests.append(dest)
    return dna_vols, water_vols, dests


def run_custom_protocol(
        reservoir_depth: float=25,
        volume_csv: FileInput=csv_example):

    deep_block_name = 'vwr-96-deep-well-2ml'
    if deep_block_name not in labware.list():
        labware.create(
            deep_block_name,
            grid=(12, 8),
            spacing=(9, 9),
            diameter=8.25,
            depth=39.9)

    reservoir_name = 'texan-reagent-reservoir-' + str(reservoir_depth) + 'mm'
    if reservoir_name not in labware.list():
        labware.create(
            reservoir_name,
            grid=(1, 1),
            spacing=(0, 0),
            diameter=85,
            depth=reservoir_depth)

    # labware setup
    plate = labware.load('96-PCR-flat', '2')
    dna_stock = labware.load(deep_block_name, '5')
    water = labware.load(reservoir_name, '1').wells('A1')

    tiprack_10 = labware.load('tiprack-10ul', '3')
    tiprack_300 = labware.load('tiprack-200ul', '6')

    # instrument setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=[tiprack_10])

    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=[tiprack_300])

    dna_vols, water_vols, dests_name = csv_to_lists(volume_csv)

    dests = [plate.wells(dest) for dest in dests_name]
    samples = [dna_stock.wells(dest) for dest in dests_name]

    # distribute water to destination wells
    p300.distribute(water_vols, water, dests, disposal_vol=0)

    # transfer DNA sample to destination wells
    for vol, source, dest in zip(dna_vols, samples, dests):
        p10.transfer(vol, source, dest)
