from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Protein Quantification',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}

# define water location
water_layout = """
1,1,1,1,1,1,1,1,1,1,1,1
1,,,,,,,1,1,,,1
1,,,,,,1,1,1,,,1
1,,,,,,1,,1,,,1
1,1,1,1,1,1,1,,1,1,1,1
,,,,,,,,,,,
,,,,,,,,,,,
,,,,,,,,,,,
"""

# labware setup
plate = labware.load('96-flat', '2')
tuberack_15 = labware.load('opentrons-tuberack-15ml', '1')
tuberack_eppendorf = labware.load('opentrons-tuberack-2ml-eppendorf', '3')
tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['5', '6']]
tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['7', '8']]

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks_10)
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=tipracks_300)

# reagent setup
buffer = tuberack_15.wells('A1')
water = tuberack_15.wells('B1')
ThT = tuberack_eppendorf.wells('A1')


def run_custom_protocol(
    tuberack_type: StringSelection(
        'opentrons-tuberack-15ml', 'opentrons-tuberack-2ml-eppendorf'
        )='opentrons-tuberack-15ml'):

    if tuberack_type == 'opentrons-tuberack-15ml':
        protein = tuberack_15.wells('A2')
    else:
        protein = tuberack_eppendorf.wells('A2')

    # transfer protein
    for volume, row_alphabet in zip([99, 49, 24], ['B', 'C', 'D']):
        dests = plate.rows(row_alphabet)[1:6] + plate.rows(row_alphabet)[9:11]
        if volume > p300.min_volume:
            pipette = p300
        else:
            pipette = p10
        pipette.distribute(volume, protein, dests, blow_out=protein)

    # transfer buffer
    p300.pick_up_tip()
    for volume, row_alphabet in zip([49, 24], ['C', 'D']):
        dests_1 = [well.top() for well in plate.rows(row_alphabet)[1:6]]
        dests_2 = [well.top() for well in plate.rows(row_alphabet)[9:11]]
        vol_1 = 99 - volume
        vol_2 = 100 - volume
        p300.distribute(
            vol_1, buffer, dests_1, blow_out=buffer, new_tip='never')
        p300.distribute(
            vol_2, buffer, dests_2, blow_out=buffer, new_tip='never')
    p300.drop_tip()

    # transfer ThT
    p10.pick_up_tip()
    for row_alphabet in ['B', 'C', 'D']:
        dests = plate.rows(row_alphabet)[1:6]
        p10.transfer(1, ThT, [dest.top() for dest in dests],
                     blow_out=True, new_tip='never')
    p10.transfer(1, ThT, plate.wells('B7'), blow_out=True, new_tip='never')
    p10.drop_tip()

    # add buffer to B7
    p300.transfer(99, buffer, plate.wells('B7'))

    # add water to outermost wells
    water_dest = []
    water_list = [cell for line in water_layout.splitlines() if line
                  for cell in [line.split(',')]]
    for row, line in zip(plate.rows(), water_list):
        for well, vol in zip(row, line):
            if vol == '1':
                water_dest.append(well)
    p300.distribute(100, water, water_dest, disposal_vol=0)
