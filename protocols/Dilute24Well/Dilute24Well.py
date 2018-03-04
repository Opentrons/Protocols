from otcustomizers import FileInput
from opentrons import containers, instruments

containers.create(
    'FluidX_24_9ml',                    # name of you container
    grid=(6, 8),                    # specify amount of (columns, rows)
    spacing=(18, 18),               # distances (mm) between each (column, row)
    diameter=13,                     # diameter (mm) of each well on the plate
    depth=83)                       # depth (mm) of each well on the plate

tiprack = containers.load("tiprack-1000ul", "B3")
destination = containers.load('FluidX_24_9ml', "B2", label="FluidX_24_9ml")
source = containers.load("trough-12row", "D2")
trash = containers.load("point", 'C3')

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
6
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
    header = example_csv.split("\n")[0].split(",")
    vol_to_add = []
    pos_to_add = []
    for line in example_csv.split("\n")[1:]:
        if not line:
            continue
        for i, col in header:
            if col == "DilutionVolume":
                vol_to_add.append(float(line.split(",")[i].rstrip()))
            if col == "LocationRack":
                pos_to_add.append(str(line.split(",")[i].rstrip()))
    p1000.transfer(
        vol_to_add, source.wells('A2'), [
            destination.wells(x) for x in pos_to_add.top(offset)])
