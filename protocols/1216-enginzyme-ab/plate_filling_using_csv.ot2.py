from opentrons import labware, instruments, robot
from otcustomizers import FileInput

example_reagent = """
Support,Buffer,Buffer Volume,NaCl,Additive,CFE,Water,Activity
None,Tris_7.5,100,0,0,50,350,
Opal,Tris_7.5,100,0,0,50,350,
Coral,Tris_7.5,100,0,0,50,350,
Amber,Tris_7.5,100,0,0,50,350,
None,Tris_8.5,100,0,0,50,350,
Opal,Tris_8.5,100,0,0,50,350,
Coral,Tris_8.5,100,0,0,50,350,
Amber,Tris_8.5,100,0,0,50,350,
None,Na-P_7.5,100,0,0,50,350,
Opal,Na-P_7.5,100,0,0,50,350,
Coral,Na-P_7.5,100,0,0,50,350,
"""

example_location = """
Reagent,Container,Slot,Well
Tris_7.5,opentrons-tuberack-2ml-eppendorf,1,A1
Tris_8.5,opentrons-tuberack-2ml-eppendorf,4,B1
Na-P_7.5,opentrons-tuberack-2ml-eppendorf,1,C1
NaCl,opentrons-tuberack-15ml,3,A1
Additive,opentrons-tuberack-15ml,3,B1
CFE,opentrons-tuberack-15ml,3,C1
Water,opentrons-tuberack-15ml,3,A2
"""


def load_locations(csv_string):
    """
    (1) Parse through location csv
    (2) Identify and load unique labware
    (3) Define reagent locations in reagent containers dictionary
    (4) Return reagent containers dictionary
    """
    info_list = [line.split(',')
                 for line in csv_string.splitlines() if line]
    reagent_containers = {}
    for line in info_list[1:]:
        name = line[0].lower()
        container = line[1]
        slot = line[2]
        loc = line[3]
        if not robot.deck[slot].has_children():
            labware.load(container, slot)
        reagent_containers[name] = \
            robot.deck[slot].get_children_list()[0].wells(loc)
    return reagent_containers


def get_reagent_lists(csv_string, reagent_containers):
    """
    (1) Parse through reagent csv
    (2) Match each well to the appropriate reagent and link the destination
        well and volume to the reagent
    (3) Return info dictionary
    """
    info = {name: {'vol': [], 'dest': []}
            for name in reagent_containers.keys()}
    info_list = [line.split(',')
                 for line in csv_string.splitlines() if line]
    headers = [cell.lower() for cell in info_list[0]]
    for index, line in enumerate(info_list[1:]):
        reagent = None
        for cell, header in zip(line, headers):
            if header in info:
                if float(cell):
                    info[header]['vol'].append(float(cell))
                    info[header]['dest'].append(index)
            elif header == 'buffer':
                reagent = cell.lower()
            elif header == 'buffer volume':
                info[reagent]['vol'].append(float(cell))
                info[reagent]['dest'].append(index)
    return info


def run_custom_protocol(
        location_csv: FileInput=example_location,
        reagent_csv: FileInput=example_reagent):

    # labware setup
    plate = labware.load('96-flat', '2')
    tipracks = labware.load('opentrons-tiprack-300ul', '6')

    # instrument setup
    p300 = instruments.P300_Single(
        mount='left',
        tip_racks=[tipracks])

    reagent_containers = load_locations(location_csv)

    reagent_lists = get_reagent_lists(reagent_csv, reagent_containers)

    for reagent in reagent_lists:
        if reagent_lists[reagent]['vol']:
            p300.distribute(
                reagent_lists[reagent]['vol'],
                reagent_containers[reagent],
                plate.wells(reagent_lists[reagent]['dest']))
