from opentrons import labware, instruments, modules
from otcustomizers import FileInput

"""
RNA dilution 96 samples
"""

# labware setup
temp_deck = modules.load('tempdeck', '4')
temp_plate = labware.load('96-flat', '4', 'Donor Plate', share=True)
temp_plate_2 = labware.load('96-flat', '7', 'Receptor Plate')
temp_plate_2.properties['height'] = 100
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
tiprack_10 = [labware.load('tiprack-10ul', slot)
              for slot in ['5', '6']]

# reagent
water = tuberack.wells('A1')

temp_deck.set_temperature(4)
temp_deck.wait_for_temp()

# pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tiprack_10)

vol_example = """
2,8,10,10,9,9,4,2,8,3,5,2
3,2,7,7,4,6,6,4,9,8,3,8
6,10,10,2,1,9,8,1,1,9,3,10
4,5,3,1,10,4,2,5,9,4,5,8
10,8,10,2,5,9,5,4,1,2,1,1
2,7,7,6,7,2,4,3,5,3,7,10
10,1,9,3,7,1,7,1,10,9,6,9
10,6,2,9,2,6,5,9,10,3,4,1
"""


def csv_to_list(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    vol_list = []
    for line in info_list:
        for cell in line:
            vol_list.append(float(cell))
    return vol_list


def run_custom_protocol(
        RNA_volume_CSV: FileInput=vol_example,
        water_volume_CSV: FileInput=vol_example):

    RNA_samples = [well for row in temp_plate.rows() for well in row]
    dests = [well for row in temp_plate_2.rows() for well in row]

    RNA_volume = csv_to_list(RNA_volume_CSV)
    water_vol = csv_to_list(water_volume_CSV)

    for vol, source, dest in zip(RNA_volume, RNA_samples, dests):
        p10.transfer(vol, source, dest, blow_out=True)

    p10.distribute(water_vol, water, [well.top() for well in dests])
