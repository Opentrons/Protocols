from opentrons import labware, instruments
from otcustomizers import FileInput
import math

metadata = {
    'protocolName': 'ELISA',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

deep_plate_name = 'usa-scientific-tuberack-1.2ml'
if deep_plate_name not in labware.list():
    labware.create(
        deep_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=44)


example_csv = """
50,500,5000
10,10000,100000
100,,
"""


def run_custom_protocol(
        number_of_standards: int=6,
        concentration_csv: FileInput=example_csv):

    # labware setup
    tuberack_4 = labware.load('opentrons-tuberack-2ml-eppendorf', '4')
    deep_plates = [labware.load(deep_plate_name, slot)
                   for slot in ['5', '6']]
    trough = labware.load('trough-12row', '8')
    plate = labware.load('96-flat', '9')

    tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['3', '10']]
    tiprack_m300 = labware.load('opentrons-tiprack-300ul', '7')

    # instrument setup
    m300 = instruments.P300_Multi(
        mount='left',
        tip_racks=[tiprack_m300])
    p300 = instruments.P300_Single(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    tubes = [well for row in tuberack_4.rows() for well in row]
    water = tubes[0]
    diluent = tubes[1]
    standards = tubes[2:2 + number_of_standards]
    samples = tubes[2 + number_of_standards:]
    antibody = trough.wells('A1')

    # define elution pool
    dil_dests = [row for deep_plate in deep_plates
                 for row in deep_plate.rows()]
    conc_lists = [[int(cell) for cell in line.split(',') if cell]
                  for line in concentration_csv.splitlines() if line]
    concs = [5, 10, 25, 50, 100, 500, 1000, 5000, 10000, 25000, 50000, 100000]

    samples = [
        row.wells(concs.index(conc))
        for concentrations, row in zip(conc_lists, dil_dests)
        for conc in concentrations
        ]

    dests = [
        [plate.cols(index)[num], plate.cols(index+1)[num]]
        for index in range(0, 12, 2) for num in range(8)
        ]

    """
    Adding Enzyme Conjugate Reagent
    """
    num_cols = math.ceil((2 + number_of_standards + len(samples)) / 8) * 2
    m300.distribute(100, antibody, plate.cols[:num_cols], blow_out=antibody)

    """
    Adding Water
    """
    p300.distribute(50, water, dests[0])
    dests.pop(0)

    """
    Adding Dilution Buffer
    """
    p300.distribute(50, diluent, dests[0])
    dests.pop(0)

    """
    Adding HCP Standards
    """
    for standard in standards:
        p300.distribute(50, standard, dests[0])
        dests.pop(0)

    """
    Adding Samples
    """
    for sample in samples:
        p300.pick_up_tip()
        p300.aspirate(130, sample)
        for dest in dests[0]:
            p300.dispense(50, dest)
        p300.drop_tip()
        dests.pop(0)
