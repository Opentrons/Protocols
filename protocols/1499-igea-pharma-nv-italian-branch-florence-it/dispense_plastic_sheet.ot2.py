from opentrons import labware, instruments

metadata = {
    'protocolName': 'Custom Sheet Dispense',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom sheet
sheet_name = 'A4-plastic-sheet'
if sheet_name not in labware.list():
    custom_plate = labware.create(sheet_name,
                                  grid=(4, 20),
                                  spacing=(12.7, 38.1),
                                  diameter=6.5,
                                  depth=0.5)

# load labware
trough = labware.load('trough-12row', '6')
sheet = labware.load(sheet_name, '10')

# establish saline resorvoir
saline = trough.wells('A1')


def run_custom_protocol(transfer_volume: float = 10.0):
    # select proper pipette and tip rack
    if transfer_volume < 5:
        tips = labware.load('tiprack-10ul', '3')
        pipette = instruments.P10_Single(mount='left', tip_racks=[tips])
    else:
        tips = labware.load('opentrons-tiprack-300ul', '3')
        pipette = instruments.P50_Single(mount='right', tip_racks=[tips])

    # distribute saline to all spots on paper
    pipette.distribute(transfer_volume,
                       saline,
                       [well.top(2) for well in sheet.wells()])
