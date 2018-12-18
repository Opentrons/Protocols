from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
source_plate = labware.load('96-PCR-tall', '4', 'Source Plate')
output_plate = labware.load('96-PCR-tall', '2', 'Master Plate')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '3')
tiprack_10 = labware.load('tiprack-10ul', '5')
# instruments setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack_300])

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_10])


def run_custom_protocols(
    tuberack_type: StringSelection(
        'opentrons-tuberack-2ml-eppendorf',
        'opentrons-tuberack-2ml-screwcap')='opentrons-tuberack-2ml-eppendorf'
        ):

    tuberack = labware.load(tuberack_type, '1')

    # distribute master mix A1
    p300.distribute(
        90,
        tuberack.wells('A1'),
        output_plate.cols('1', '4'),
        disposal_vol=0
        )

    # distribute master mix B1
    p300.distribute(
        90,
        tuberack.wells('B1'),
        output_plate.cols('7', '10'),
        disposal_vol=0
        )

    dests = [col for col in output_plate.cols('1', '4', '7', '10')]
    sources = [col for col in source_plate.cols('1', length=4)]
    for source, dest in zip(sources, dests):
        m10.pick_up_tip()
        m10.transfer(2, source, dest, new_tip='never')
        m10.mix(5, 10, dest)
        m10.blow_out(dest.top())
        m10.drop_tip()

    sources = [col for col in output_plate.cols('1', '4', '7', '10')]
    dests = [output_plate.cols(index, length=2) for index in range(1, 12, 3)]
    for source, dest in zip(sources, dests):
        m10.transfer(10, source, dest)
