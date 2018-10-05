from opentrons import labware, instruments, robot
from otcustomizers import FileInput

"""
Create Folding Mix
"""

# labware setup
pcr = labware.load('PCR-strip-tall', '2')
tiprack_10 = [labware.load('tiprack-10ul', slot)
              for slot in ['10', '7']]
tiprack_50 = [labware.load('tiprack-200ul', slot)
              for slot in ['11', '8']]
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')

# reagent setup
reagent = {'pool '+str(i+1): tuberack.wells(i) for i in range(11)}
reagent['biotinylated dna'] = tuberack.wells('A6')
reagent['folding buffer'] = tuberack.wells('B6')
reagent['h2o'] = tuberack.wells('C6')
reagent['scaffold'] = tuberack.wells('D6')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tiprack_10)

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=tiprack_50)


structure_scheme_example = """
Structure,Name,Scaffold,Pool 1,Pool 2,Pool 3,Pool 4,Pool 5,Pool 6,Pool 7,\
Pool 8,Pool 9,Pool 10,Pool 11,Biotinylated DNA,Folding Buffer,H2O,Total
1,20nm GRIDS 4x,4.00,52.48,19.20,0,0,0,0,0,0,0,0,0,12.80,16.00,55.52,160.00
2,10nm GRIDS 4x,4.00,0,0,42.88,67.20,0,0,0,0,0,0,0,12.80,16.00,17.12,160.00
3,RESI LOGO,1.00,0,0,0,0,8.64,21.76,0,0,0,0,0,3.20,4.00,1.40,40.00
4,RESI RECT,3.00,0,0,0,0,0,0,29.76,15.60,15.60,15.60,15.60,9.60,12.00,3.24,\
120.00
"""


def create_structures(csv_string):
    # transform csv string to list
    info_list = [line.split(',')
                 for line in csv_string.splitlines() if line]

    # define headers
    headers = [header.lower() for header in info_list[0]]

    # parse through list
    for index, line in enumerate(info_list[1:]):
        for cell, header in zip(line, headers):
            dest = pcr.wells(index)  # define destination well
            if header in reagent.keys():
                cell = float(cell)
                if cell:
                    if cell <= 10:
                        pipette = p10
                    else:
                        pipette = p50
                    # transfer reagent to destination well
                    pipette.transfer(cell, reagent[header], dest)
            elif header == 'name':
                # display structure name to OT-App
                robot.comment('Preparing structure: '+cell)
            elif header == 'total':
                cell = float(cell)
                if cell >= 50:
                    pipette = p50
                else:
                    pipette = p10
                # mix structure 10x before moving on to the next structure
                pipette.pick_up_tip()
                pipette.mix(10, pipette.max_volume, dest)
                pipette.drop_tip()


def run_custom_protocol(
        folding_mix_scheme_csv: FileInput=structure_scheme_example):

    create_structures(folding_mix_scheme_csv)
