from opentrons import labware, instruments
from otcustomizers import StringSelection, FileInput
import math

# labware setup
source_racks = [labware.load('opentrons-tuberack-2ml-eppendorf', slot)
                for slot in ['1', '2', '3']]

dest_racks = [labware.load('opentrons-tuberack-2ml-screwcap', slot)
              for slot in ['4', '5', '6']]
for rack in dest_racks:
    for well in rack:
        well.properties['height'] = 24

diluent = labware.load('opentrons-tuberack-50ml', '7').wells('A1')

tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                for slot in ['8', '9']]
tipracks_10 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['10', '11']]

# instruments setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tipracks_300)

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=tipracks_10)
pipettes = [p300, p50]


csv_example = """
Sample (uL),Buffer (uL)
70,80
70,80
79,80
100,95
100,95
"""


def csv_to_list(csv_string):
    """
    returns two ordered lists:
        sample volumes, diluent volumes
    each value in the list represents the volume to be transferred to each well
    """
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    sample_vol, diluent_vol = [], []
    for line in (info_list[1:]):
        if line[0] == "":
            line[0] = 0
        sample_vol.append(float(line[0]))
        if line[1] == "":
            line[1] = 0
        diluent_vol.append(float(line[1]))
    return sample_vol, diluent_vol


def run_custom_protocol(
        dilution_csv: FileInput=csv_example,
        total_diluent_volume: float=50,
        mix_after_each_transfer: StringSelection("True", "False")="True"):

    sample_volumes, diluent_volumes = csv_to_list(csv_example)
    diluent_height = 20 + \
        (50-total_diluent_volume) * 1000 / (math.pi * (15 ** 2))

    if mix_after_each_transfer == "True":
        mix_num = 3
    else:
        mix_num = 0

    sources = [well for rack in source_racks for well in rack]
    dests = [well for rack in dest_racks for well in rack]

    for index, vol in enumerate(diluent_volumes):
        diluent_height += vol / (math.pi * (15 ** 2))
        if vol >= 50:
            if not p300.tip_attached:
                p300.pick_up_tip()
            p300.transfer(
                vol,
                diluent.top(-diluent_height),
                dests[index],
                new_tip='never')
        else:
            if not p50.tip_attached:
                p50.pick_up_tip()
            p50.transfer(
                vol,
                diluent.top(-diluent_height),
                dests[index],
                new_tip='never')
    for pipette in pipettes:
        if pipette.tip_attached:
            pipette.drop_tip()

    for index, vol in enumerate(sample_volumes):
        if vol >= 50:
            p300.transfer(
                vol, sources[index], dests[index], mix_after=(mix_num, 50))
        else:
            p50.transfer(
                vol, sources[index], dests[index], mix_after=(mix_num, 20))
