from opentrons import labware, instruments

"""
Growing 96-well Bacterial Cultures
"""

trough_2row_name = 'trough-2row'
if trough_2row_name not in labware.list():
    labware.create(
        trough_2row_name,
        grid=(2, 1),
        spacing=(54, 0),
        diameter=53,
        depth=39.2)

# labware setup
deep_block = labware.load('96-deep-well', '2')
inoculants = labware.load('96-deep-well', '3')
trough_2row_1 = labware.load(trough_2row_name, '4')
tiprack = labware.load('tiprack-200ul', '7')
tiprack10 = labware.load('tiprack-10ul', '8')

# reagent setup
LB_medium = trough_2row_1.wells('A1')

# pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack10])


def run_custom_protocol(
        inoculant_volume: float=2):

    # transfer 750 uL lysis buffer to each well
    m300.transfer(
        750,
        LB_medium,
        [well.top() for well in deep_block.rows(0)],
        new_tip='once')

    # inoculate eacl well
    m10.transfer(
        inoculant_volume,
        [well.top() for well in inoculants.rows(0)],
        [well.top() for well in deep_block.rows(0)],
        new_tip='always')
