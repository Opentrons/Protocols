from opentrons import containers, instruments

#list of talens
talens = ['AAACCCAAACCCAAA', 'AAACCCAAACCCAAATT', 'AAAAAAAAAAAAAAA']  # change here
#list of vectors
vectors = ['pT3TS 1', 'pT3TS 2', 'pKT3 1']  # change here

vol1 = 6.25  # reagent 1 volume
vol2 = 5  # reagent 2 volume
vol3 = 3.75  # reagent 3 volume
nuc_vol = 5  # nucleotide volume
vector_vol = 5  # vector volume

# open file with absolute path (will be different depending on operating system)
# file paths on Windows look more like 'C:\\path\\to\\your\\csv_file.csv' on Mac '/path/to/your/csv_file.csv'

#path = 'C:\\Users\\calel_000\\Libraries\\Documents\\Opentrons\\Protocols\\FusX Mayo Clinic\\FusX Plate Mapping input draft.csv'

# takes file path as input and returns list of the plate contents in proper order
# input intended to be same format as in the FusX plate map Excel sheet

def generate_content_list(filepath):
    with open(filepath) as my_file:

        # save well contents from CSV file into a list
        plate_contents = []
    
        # store lines temporarily to reverse order of lines
        temp_lines = []

        # loop through each line (row of plate)
        for row in my_file.read().splitlines():
            temp_lines.append(row)

        # go through lines (rows of plate) in reverse of input file
        for row in reversed(temp_lines):
            # loop through each comma-separated value (each row's contents)
            for well in row.split(','):
                plate_contents.append(well.strip())
    
    return plate_contents;

# returns a list of the well objects containing each nucleotide triple
# and optional double in the appropriate plate locations
# input is a string 15 or 17 characters long of the TALEN triples + optional double

def generate_well_list(TALENstring):
    
    # list to hold wells for the entered nucleotides
    wells = []
    
    #first 5 nucleotide triplet locations
    for triple in range(0, 5):
        plate = source_plates[triple]
        nucleotides = TALENstring[(3*triple):(3*triple + 3)]
        wells.append(plate.wells(plate_dict[nucleotides]))
        
    # optional last 2 nucleotides' location
    if len(TALENstring) == 17:
        nucleotides = TALENstring[15:17]
        wells.append(plate5.wells(plate_dict[nucleotides]))
        
    return wells;

# returns a list of the well objects containing each vector
# input is a list of vector strings

def generate_vector_locations(vectors):
    wells = []
    for vector in vectors:
        wells.append(plate5.wells(plate_dict[vector]))  # get location 
    return wells;

# executes protocol taking in a list of TALENs and vectors

def executeProtocol(talens, vectors):
    
    vector_wells = generate_vector_locations(vectors)
    
    for talen in range(0, len(talens)):
        # Transfer 6.25ul from 1.7 microcentrifuge tube A1 to pcr strip well
        p10single.transfer(vol1, reagent1, PCRstrip[talen])
        # Transfer 5ul from the appropriate well in each input plate to pcr strip well
        p10single.transfer(nuc_vol, generate_well_list(talens[talen]), PCRstrip[talen], new_tip='always')
        # Transfer 5ul of vector (input plate 5) to pcr strip well
        p10single.transfer(vector_vol, vector_wells[talen], PCRstrip[talen])
        # Transfer 5ul from 1.7 microcentrifuge tube A2 to pcr strip well
        p10single.transfer(vol2, reagent2, PCRstrip[talen])
        # Tranfer 3.75ul from 1.7 microcentrifuge tube A3 to pcr strip well
        p10single.transfer(vol3, reagent3, PCRstrip[talen])
    

# the contents of each well on the plate (triple, duple, primer)
# can easily be populated from a csv, order will match up to well number order below 
# (following API order, starting at well A1, then B1, C1.....A2, B2, C2.... etc along rows)

# plate_contents = generate_content_list(path)  # populate from csv

# optional hard-code

plate_contents = ['AAA', 'AAC', 'AAG', 'AAT', 'ACA', 'ACC', 'ACG', 'ACT',  # A1 to H1
                   'AGA', 'AGC', 'AGG', 'AGT', 'ATA', 'ATC', 'ATG', 'ATT',  # A2 to H2
                   'CAA', 'CAC', 'CAG', 'CAT', 'CCA', 'CCC', 'CCG', 'CCT',
                   'CGA', 'CGC', 'CGG', 'CGT', 'CTA', 'CTC', 'CTG', 'CTT',
                   'GAA', 'GAC', 'GAG', 'GAT', 'GCA', 'GCC', 'GCG', 'GCT',
                   'GGA', 'GGC', 'GGG', 'GGT', 'GTA', 'GTC', 'GTG', 'GTT',
                   'TAA', 'TAC', 'TAG', 'TAT', 'TCA', 'TCC', 'TCG', 'TCT',
                   'TGA', 'TGC', 'TGG', 'TGT', 'TTA', 'TTC', 'TTG', 'TTT',
                   'AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT',
                   'GA', 'GC', 'GG', 'GT', 'TA', 'TC', 'TG', 'TT',
                   'pLR: A 1', 'pLR: C 1', 'pLR: G 1', 'pLR: T 1', 'pLR: A 2', 'pLR: C 2', 'pLR: G 2', 'pLR: T 2',
                   'pT3TS 1', 'pC 1', 'pKT3 1', 'pT3TS 2', 'pC 2', 'pKT3 2', 'x', 'x',  # A12 to H12
]

# wells of 96 well plate numbered 1 to 96, not really subject to change

plate_locations = list(range(0, 96))

# creates dictionary to map the triple or duple or primer to the location on the plate
plate_dict = dict(zip(plate_contents, plate_locations))

#destination PCR strip
PCRstrip = containers.load('PCR-strip-tall', 'A1')

#plates with the talen pieces
plate1 = containers.load('96-PCR-flat', 'B1')
plate2 = containers.load('96-PCR-flat', 'C1')
plate3 = containers.load('96-PCR-flat', 'D1')
plate4 = containers.load('96-PCR-flat', 'B2')
plate5 = containers.load('96-PCR-flat', 'C2')

#tube racks on cooling deck
reagents = containers.load('tube-rack-2ml', 'D2')
#tip rack for p10
tip10_rack = containers.load('tiprack-10ul', 'A2')
#trash container
trash = containers.load('point', 'A3')

#p10 (1 - 10 uL) (single)
p10single = instruments.Pipette(
    axis='a',
    name='p10single',
    max_volume=10,
    min_volume=1,
    channels=1,
    trash_container=trash,
    tip_racks=[tip10_rack])

#list of source plates
source_plates = [plate1, plate2, plate3, plate4, plate5]

#reagents
reagent1 = reagents['A1']
reagent2 = reagents['A2']
reagent3 = reagents['A3']

# function call to run protocol

executeProtocol(talens, vectors)
