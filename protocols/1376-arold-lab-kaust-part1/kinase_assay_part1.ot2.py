from opentrons import labware, instruments, modules, robot
from otcustomizers import FileInput

# labware setup
temp_deck = modules.load('tempdeck', '2')
target = labware.load('96-flat', '2', share=True)
tiprack = labware.load('tiprack-10ul', '11')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack])


assay_example = """
Target Well,Water,Substrate A+,Substrate A,Substrate B+,Substrate B,Enzyme 1,\
Enzyme 2,Enzyme 3,Enzyme 4
A2,2.5,2.5,,,,,,,
B2,2.5,,2.5,,,,,,
C2,2.5,,,2.5,,,,,
D2,2.5,,,,2.5,,,,
E2,,,2.5,,,2.5,,,
F2,,,2.5,,,,2.5,,
G2,,,,,2.5,,,2.5,
H2,,,,,2.5,,,,2.5
"""

reagent_example = """
Reagent,Tube Rack,Slot,Well
Water,opentrons-tuberack-2ml-eppendorf,3,A1
Substrate A,opentrons-tuberack-2ml-eppendorf,3,B1
Substrate A+,opentrons-tuberack-2ml-eppendorf,3,C1
Substrate B,opentrons-tuberack-2ml-eppendorf,3,D1
Substrate B+,opentrons-tuberack-2ml-eppendorf,3,A2
Enzyme 1,opentrons-tuberack-2ml-eppendorf,4,B2
Enzyme 2,opentrons-tuberack-2ml-eppendorf,4,C2
Enzyme 3,opentrons-tuberack-2ml-eppendorf,4,D2
Enzyme 4,opentrons-tuberack-2ml-eppendorf,4,A3
"""


def load_reagents(csv_string):
    info_list = [line.split(',')
                 for line in csv_string.splitlines() if line]
    reagent_dict = {}
    for line in info_list[1:]:
        name = line[0].lower().replace(" ", "")
        container = line[1]
        slot = line[2]
        loc = line[3]
        if not robot.deck[slot].has_children():
            labware.load(container, slot)
        reagent_dict[name] = \
            robot.deck[slot].get_children_list()[0].wells(loc)
    return reagent_dict


def transfer_reagent_to_well(csv_string, reagent_info):
    """
    (1) Parse through reagent csv
    (2) Match each well to the appropriate reagent and link the destination
        well and volume to the reagent
    (3) Return info dictionary
    """
    info_list = [line.split(',')
                 for line in csv_string.splitlines() if line]
    headers = [cell.lower().replace(" ", "") for cell in info_list[0]]
    for index, header in enumerate(headers[1:], 1):
        dest = []
        vol = []
        for line in info_list[1:]:
            if line[index] and header in reagent_info.keys():
                vol.append(float(line[index]))
                source = reagent_info[header]
                dest.append(target.wells(line[0]))
        p10.distribute(vol, source, dest)


def run_custom_protocol(
        tempdeck_temperature: float=4.0,
        reagent_location_csv: FileInput=reagent_example,
        assay_setup_csv: FileInput=assay_example):

    temp_deck.set_temperature(tempdeck_temperature)
    temp_deck.wait_for_temp()

    reagents = load_reagents(reagent_location_csv)

    transfer_reagent_to_well(assay_setup_csv, reagents)
