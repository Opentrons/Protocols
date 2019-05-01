from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'NGS Library Prep: DNA Target Amplification',
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
    sample_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
    tiprack_m10 = labware.load(tiprack_10ul_name, '4')
    tiprack_10 = labware.load(tiprack_10ul_name, '6')

    # instruments setup
    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=[tiprack_10])
    m10 = instruments.P10_Multi(
        mount='right',
        tip_racks=[tiprack_m10])

    # reagent setup
    hifi_mix = reagent_plate.cols('1')
    precision_id_panel = reagent_plate.cols('2')

    sample_col = math.ceil(sample_num / 8)

    # transfer Hifi Mix to plate
    m10.distribute(
        4, hifi_mix, plate.cols('1', length=sample_col), blow_out=hifi_mix)

    # transfer Precision ID Panel
    m10.transfer(10, precision_id_panel, plate.cols('1', length=sample_col))

    # transfer samples
    for sample, dest in zip(sample_rack.wells('A1', length=sample_num),
                            plate.wells('A1', length=sample_num)):
        p10.pick_up_tip()
        p10.transfer(6, sample, dest, new_tip='never')
        p10.mix(3, 10, dest)
        p10.blow_out(dest)
        p10.drop_tip()
