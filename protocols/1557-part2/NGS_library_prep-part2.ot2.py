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
    tiprack_10 = labware.load(tiprack_10ul_name, '6')

    # instruments setup
    m10 = instruments.P10_Multi(
        mount='right',
        tip_racks=[tiprack_10])

    # reagent setup
    fupa_reagent = reagent_plate.cols('1')

    sample_col = math.ceil(sample_num / 8)

    # distribute FuPa reagent to each sample
    for col in plate.cols('1', length=sample_col):
        m10.pick_up_tip()
        m10.transfer(2, fupa_reagent, col, new_tip='never')
        m10.mix(3, 10, col)
        m10.blow_out(col)
        m10.drop_tip()
