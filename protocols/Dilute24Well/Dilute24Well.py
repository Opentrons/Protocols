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

example_csv = """CPD ID,Structure,Original Name,Rack Type,Max volume in rack (4 mL),Rack Barcode,Vial Barcode,""" +\
              +"""LocationRack,Location 1536 XCHEM,Chemist,Salt,SMILES,weight (mg),MW (g.mol-1),Density,Volume of """ +\
              +"""reagent,DilutionVolume,Reaction Scale (mmol),Equivalent,Quant Reagent (mmol),Volume per reaction """ +\
              +"""(uL),nb reaction per plate,Volume needed (mL)
Amine1,C3H4N2O,isoxazol-3-amine,Fluidx 24 9mL,5,NA, FB04712992,A2,NA,TDI,N,NC1=NOC=C1,298.8,84.078,NA,NA,4442.303""" +\
              +"""575,0.08,1,0.08,100,12,1.2
Amine2,C6H6FN,2-fluoroaniline,Fluidx 24 6mL,4,NA, FB00049165,D5,NA,TDI,N,FC1=CC=CC=C1N,292,111.1194032,NA,NA,3284.7""" +\
              +"""54863,0.08,1,0.08,100,12,1.2
Amine3,C5H6N2,pyridin-3-amine,Fluidx 24 9mL,5,NA, FB04712980,A4,NA,TDI,N,NC1=CN=CC=C1,326.4,94.117,NA,NA,4335.02980""" +\
              +"""3,0.08,1,0.08,100,12,1.2
Amine4,C4H5N3,pyridazin-3-amine,Fluidx 24 9mL,5,NA, FB04712973,C2,NA,TDI,Y,NC1=NN=CC=C1,286.5,95.105,NA,NA,3765.574""" +\
              +"""891,0.08,1,0.08,100,12,1.2
Amine5,C5H6N2,pyridin-2-amine,Fluidx 24 9mL,5,NA, FB04713132,A6,NA,TDI,N,NC1=NC=CC=C1,312,94.117,NA,NA,4143.778488,""" +\
              +"""0.08,1,0.08,100,12,1.2
Amine6,C4H5N3,pyrimidin-2-amine,Fluidx 24 9mL,5,NA, FB04712981,B2,NA,TDI,N,NC1=NC=CC=N1,292.8,95.105,NA,NA,3848.378""" +\
              +"""108,0.08,1,0.08,100,12,1.2
Amine7,C6H6ClN,3-chloroaniline,Fluidx 24 9mL,5,NA, FB04712986,B4,NA,TDI,N,ClC1=CC=CC(N)=C1,290.6,127.571,NA,NA,28""" +\
              +"""47.433978,0.08,1,0.08,100,12,1.2
Amine8,C4H6N2O,5-methylisoxazol-3-amine,Fluidx 24 9mL,5,NA, FB04712990,B6,NA,TDI,N,CC1=CC(N)=NO1,336.5,98.105,NA,""" +\
              +"""NA,4287.498089,0.08,1,0.08,100,12,1.2
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
