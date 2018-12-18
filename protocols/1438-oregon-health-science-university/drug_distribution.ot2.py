from opentrons import labware, instruments

metadata = {
    'protocolName': 'Drug Distribution in Triplicate',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
plate = labware.load('96-flat', '2')
tiprack = labware.load('opentrons-tiprack-300ul', '4')

# instruments setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack])

drugs = [well for row in tuberack.rows() for well in row]

dests = [row(index, length=3)
         for row in plate.rows() for index in range(0, 7, 3)]


def run_custom_protocol(transfer_volume: float=20):
    for source, dest in zip(drugs, dests):
        p50.distribute(20, source, dest, blow_out=source)
