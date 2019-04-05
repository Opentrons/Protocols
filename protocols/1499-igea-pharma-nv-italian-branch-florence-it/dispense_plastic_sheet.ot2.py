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
p10 = instruments.P10_Single(mount='left',
                             tip_racks=[tips10])


def run_custom_protocol(transfer_volume: float = 10.0):

    # transfer saline to all spots on paper
    p10.pick_up_tip()
    p10.transfer(10,
                 saline,
                 [well.top(2) for well in sheet.wells()],
                 blow_out=True,
                 new_tip='never')
    p10.drop_tip()
