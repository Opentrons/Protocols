from opentrons import labware, instruments, modules
from otcustomizers import FileInput

"""
RT mix 96 samples
"""

# labware setup
temp_deck = modules.load('tempdeck', '4')
temp_plate = labware.load('96-flat', '4', 'Donor Plate', share=True)
temp_plate_2 = labware.load('96-flat', '7', 'Receptor Plate')
temp_plate_2.properties['height'] = 100
rt_plate = labware.load('96-flat', '8', 'Primer Plate')
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
tiprack_10 = [labware.load('tiprack-10ul', slot)
              for slot in ['5', '6']]
tiprack_10_m = labware.load('tiprack-10ul', '9')

# reagent
water = tuberack.wells('A1')

temp_deck.set_temperature(4)
temp_deck.wait_for_temp()

# pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tiprack_10)

m10 = instruments.p10_Multi(
    mount='right',
    tip_racks=[tiprack_10_m])

vol_example = """
5,1,2,2,1,5,1,4,4,1,3,3
4,1,5,1,2,1,1,3,3,1,5,3
4,2,1,5,4,3,2,2,2,2,2,2
5,3,3,4,1,4,3,4,2,1,5,4
3,2,5,5,3,3,4,5,2,1,3,5
3,1,4,1,1,5,4,3,1,3,1,1
4,3,4,5,4,5,1,4,4,4,2,1
5,1,2,5,1,4,2,1,3,2,5,1
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
        primer_volume: float=1,
        water_volume_CSV: FileInput=vol_example,
        RNA_volume_CSV: FileInput=vol_example):

    RNA_samples = [well for row in temp_plate.rows() for well in row]
    dests = [well for row in temp_plate_2.rows() for well in row]

    RNA_volume = csv_to_list(RNA_volume_CSV)
    water_vol = csv_to_list(water_volume_CSV)

    # transfer primer to plate
    m10.transfer(primer_volume, rt_plate.cols(), temp_plate_2.cols(),
                 blow_out=True, new_tip='always')

    # distribute water to plate
    p10.distribute(water_vol, water, [well.top() for well in dests])

    # transfer RNA sample to plate
    for vol, source, dest in zip(RNA_volume, RNA_samples, dests):
        p10.transfer(vol, source, dest, blow_out=True)
