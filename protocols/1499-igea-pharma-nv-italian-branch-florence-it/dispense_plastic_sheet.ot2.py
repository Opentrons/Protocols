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

# labware
tips10 = labware.load('tiprack-10ul', '3')
trough = labware.load('trough-12row', '6')

# custom sheet
sheet = labware.load('A4-plastic-sheet', '10')

# establish saline resorvoir
saline = trough.wells('A1')

# pipettes
p50 = instruments.P50_Single(mount='left',
                             tip_racks=[tips10])

# transfer saline to all spots on paper
spots_ordered = [spot.top(2) for row in sheet.rows() for spot in row]
p50.distribute(10,
               saline,
               spots_ordered)
