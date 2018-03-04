from otcustomizers import FileInput
from opentrons import containers, instruments, robot

tiprack = containers.load("tiprack-1000", "B3")
destination = containers.load("FluidX_24_9ml", "B2")
source = containers.load("trough-big", "D2")
trash = containers.load("point",'C3')
# Define the pipettes
p1000 = instruments.Pipette(
    name="eppendorf1000",
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=1000,
    min_volume=10,
    channels=1,
)

example_csv = """
    LocationRack,DilutionVolume
    A2,84.078
    D5,111.1194032
    A4,94.117
    C2,95.105
    A6,94.117
    B2,95.105
    B4,127.571
    B6,98.105
    """

def run_custom_protocol(input_csv: FileInput=example_csv):
    offset = -30
    input_lines = [x for x in example_csv.split("\n") if x.strip() != ""]
    header = [x.strip() for x in input_lines[0].split(",")]
    vol_to_add = []
    pos_to_add = []
    for line in input_lines[1:]:
        for i, col in enumerate(header):
            if col=="DilutionVolume":
                vol_to_add.append(float(line.split(",")[i].strip()))
            if col=="LocationRack":
                pos_to_add.append(str(line.split(",")[i].strip()))
    p1000.transfer(vol_to_add,
                   source.wells('A2'),
                   [destination.wells(x) for x in pos_to_add.top(offset)])