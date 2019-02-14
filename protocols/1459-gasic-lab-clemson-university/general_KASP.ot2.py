from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'PCR/qPCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

plate_name = "96-PCR-flat-semi-skirted"
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=20.2)

# labware setup
dna_stock = labware.load(plate_name, '1', 'DNA Source')
outputs = [labware.load(plate_name, slot)
           for slot in ['2', '3', '5', '6', '8', '9', '11']]
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '4')

tiprack_p10 = labware.load('tiprack-10ul', '7')
tiprack_m10 = labware.load('tiprack-10ul', '10')

# instruments setup
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_m10])

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_p10])


def run_custom_protocol(
        number_of_mastermixes: int=7,
        number_of_samples: int=96):

    output_plates = outputs[:number_of_mastermixes]
    mastermixes = tuberack.wells('A1', length=number_of_mastermixes)
    sample_cols = math.ceil(number_of_samples / 8)

    # transfer samples
    for col_num in range(sample_cols):
        source = dna_stock.cols(col_num)
        dests = [plate.cols(col_num)[0].bottom(0.5) for plate in output_plates]
        m10.distribute(4, source, dests, disposal_vol=0)

    # transfer master mixes
    for mastermix, plate in zip(mastermixes, output_plates):
        dests = [well.top()
                 for well in plate.wells('A1', length=number_of_samples)]
        p10.distribute(4, mastermix, dests, disposal_vol=0)
