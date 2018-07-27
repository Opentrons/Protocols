from opentrons import labware, instruments

# customization
""" Part 1 """
protein_dilution_factor = 10
protein_dilution_vol = 20

""" Part 2 """
c_ligand_dilution_vol = 20

""" Part 3 """
protein_to_add = 20
f_ligand_to_add = 140
protein_mix_vol = 2000


# Labware setup
target = labware.load('384-plate', 1)
reagent_rack = labware.load('tube-rack-2ml', 2)
tiprack1_10 = labware.load('tiprack-10ul', 3)
tiprack2_10 = labware.load('tiprack-10ul', 4)
tiprack3_10 = labware.load('tiprack-10ul', 5)


# Protein dilution setup
protein_well = reagent_rack.wells('C1')
buffer_well = reagent_rack.wells('C2')
new_protein_well = reagent_rack.wells('C3')

# Serial dilutions of competitor ligand setup
c_ligand_1500 = reagent_rack.wells('A1')
c_ligand_300 = reagent_rack.wells('B1')
DMSO_well = reagent_rack.wells('D1')

# Protein and fluorescent ligand mix setup
f_ligand_well = reagent_rack.wells('C5')
protein_mix_well = reagent_rack.wells('C6')

# Pipette setup
tipracks = [tiprack1_10, tiprack2_10, tiprack3_10]
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=tipracks)


# Part 1: Dilute protein in buffer
protein_vol = protein_dilution_vol / protein_dilution_factor
buffer_vol = protein_dilution_vol - protein_vol

# p10.transfer(buffer_vol, buffer_well, new_protein_well)
# p10.transfer(protein_vol, protein_well, new_protein_well)


# Part 2: Make two sets of serial dilution of competitor ligand
cl_vol = c_ligand_dilution_vol / 10
DMSO_vol = c_ligand_dilution_vol - cl_vol

p10.pick_up_tip()
p10.transfer(DMSO_vol, DMSO_well, reagent_rack.rows['A'][1:5], new_tip='never')
p10.transfer(DMSO_vol, DMSO_well, reagent_rack.rows['B'][1:5], new_tip='never')
p10.drop_tip()

p10.pick_up_tip()
for tube1, tube2 in zip(reagent_rack.rows['A'][0:4],
                        reagent_rack.rows['A'][1:5]):
    p10.transfer(cl_vol, tube1, tube2, mix_after=(3, 10), new_tip='never')
p10.drop_tip()

p10.pick_up_tip()
for tube1, tube2 in zip(reagent_rack.rows['B'][0:4],
                        reagent_rack.rows['B'][1:5]):
    p10.transfer(cl_vol, tube1, tube2, mix_after=(3, 10), new_tip='never')
p10.drop_tip()


# Part 3: Make protein and fluorescent ligand mix
buffer_vol = protein_mix_vol - protein_to_add - f_ligand_to_add
p10.transfer(buffer_vol, buffer_well, protein_mix_well)

p10.transfer(protein_to_add, new_protein_well, protein_mix_well)
p10.transfer(f_ligand_to_add, f_ligand_well, protein_mix_well)


# Part 4: Add competitor ligand to target plate
p10.transfer(2, DMSO_well, target.rows(0))

serial_dilutions = reagent_rack.rows['A'][0:5] + reagent_rack.rows['B'][0:5]
for row_index, concentration in enumerate(serial_dilutions):
    p10.transfer(2, concentration, target.rows(row_index+1))

# Part 5: Add protein/fluorescent ligand mix to target plate
for row in target.rows['A':'K']:
    for well in row:
        p10.pick_up_tip()
        p10.transfer(28, protein_mix_well, well, new_tip='never')
        p10.mix(3, 10)
        p10.drop_tip()
