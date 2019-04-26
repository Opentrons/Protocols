from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'NGS Library Prep: Partically Digest Amplicons',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

pcr_plate_name = 'eppendorf-twin.tec-skirted-96-PCR'
if pcr_plate_name not in labware.list():
    labware.create(
        pcr_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.46,
        depth=14.6,
        volume=150)

tiprack_100ul_name = 'neptune-filter-tiprack-100ul'
if tiprack_100ul_name not in labware.list():
    labware.create(
        tiprack_100ul_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=40)

tiprack_10ul_name = 'neptune-filter-tiprack-10ul'
if tiprack_10ul_name not in labware.list():
    labware.create(
        tiprack_10ul_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5,
        depth=40)


def run_custom_protocol(
        sample_num: int=24):

    # labware setup
    reagent_plate = labware.load(pcr_plate_name, '1')
    plate = labware.load(pcr_plate_name, '2')
    ioncode_adapters = labware.load(
        'opentrons-aluminum-block-PCR-strips-200ul', '5')
    tipracks_10 = [labware.load(tiprack_10ul_name, slot)
                   for slot in ['3', '6', '9']]

    # instruments setup
    m10 = instruments.P10_Multi(
        mount='right',
        tip_racks=tipracks_10)

    # reagent setup
    switch_solution = reagent_plate.cols('1')
    dna_ligase = reagent_plate.cols('2')

    sample_col = math.ceil(sample_num / 8)

    # transfer Swtich Solution to each sample
    for col in plate.cols('1', length=sample_col):
        m10.transfer(4, switch_solution, col)

    # transfer IonCode Adapters to each sample
    for source, dest in zip(
            ioncode_adapters.cols('1', length=sample_col),
            plate.cols('1', length=sample_col)):
        m10.transfer(2, source, dest)

    # transfer DNA Ligase to each sample
    for col in plate.cols('1', length=sample_col):
        m10.pick_up_tip()
        m10.transfer(
            2, dna_ligase, col, mix_after=(3, 10), new_tip='never')
        m10.blow_out(col)
        m10.drop_tip()
