from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 5',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        number_of_samples: StringSelection('16', '48', '96')='96',
        pool_volume: float=5):

    number_of_samples = int(number_of_samples)

    # labware setup
    rt_tuberack = labware.load('opentrons-tuberack-2ml-screwcap', '5')
    temp_module = modules.load('tempdeck', '7')
    temp_plate = labware.load(
        'opentrons-aluminum-block-96-PCR-plate', '7', share=True)
    tuberack = labware.load('opentrons-aluminum-block-2ml-eppendorf', '8')
    tipracks_50 = [labware.load('opentrons-tiprack-300ul', slot)
                   for slot in ['6', '9']]
    tipracks_10 = [labware.load('opentrons-tiprack-10ul', slot)
                   for slot in ['10', '11']]

    # instrument setup
    p50 = instruments.P50_Single(
        mount='left',
        tip_racks=tipracks_50)
    p10 = instruments.P10_Single(
        mount='right',
        tip_racks=tipracks_10)

    # reagent setup
    cot_1_human_dna = rt_tuberack.wells('A1')
    universal_blockers = rt_tuberack.wells('B1')
    pool_sample = tuberack.wells('A1')

    temp_module.set_temperature(4)
    temp_module.wait_for_temp()

    samples = temp_plate.wells('A1', length=number_of_samples)

    # pool equal amount of individual sample
    if pool_volume > 10:
        pipette = p50
    else:
        pipette = p10
    for sample in samples:
        pipette.transfer(pool_volume, sample, pool_sample, blow_out=True)

    # add COT-1 Human DNA to the library pool
    p10.transfer(5, cot_1_human_dna, pool_sample, blow_out=True)

    # add Universal Blockers to the library pool
    p10.transfer(2, universal_blockers, pool_sample, blow_out=True)
