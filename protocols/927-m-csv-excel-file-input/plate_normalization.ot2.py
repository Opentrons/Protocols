from opentrons import labware, instruments
from otcustomizers import FileInput

# labware setup
plate_a = labware.load('96-deep-well', '1')
plate_b = labware.load('96-deep-well', '2')
diluent = labware.load('trough-12row', '5').wells('A1')
tuberack = labware.load('tube-rack-2ml', '6')
mixtube = tuberack.wells('A1')

tiprack1 = labware.load('tiprack-200ul', '3')
tiprack2 = labware.load('tiprack-200ul', '4')

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack1, tiprack2])

norm_example_csv = """
WELL,Oligo Name,Product no.,Conc (µM),Volume (ml),Amount (nmol)
A1,Oligo1,18FT-1,25,1,25
A2,Oligo2,18FT-2,22,1,22
A3,Oligo3,18FT-3,23,1,23
A4,Oligo4,18FT-4,13,1,13
A5,Oligo5,18FT-5,48,1,48
A6,Oligo6,18FT-6,22,1,22
A7,Oligo7,18FT-7,20,1,20
A8,Oligo8,18FT-8,24,1,24
A9,Oligo9,18FT-9,28,1,28
A10,Oligo10,18FT-10,16,1,16
A11,Oligo11,18FT-11,29,1,29
A12,Oligo12,18FT-12,28,1,28
"""

cons_example_csv = """
66,43,58,61,24,111,139,185,28,106,56,90
60,16,101,71,128,25,48,96,143,198,197,168
164,156,121,109,106,84,111,60,185,45,147,187
129,175,5,84,88,12,68,105,17,6,139,13
106,190,122,85,124,63,179,143,199,46,74,70
7,41,88,62,65,31,126,151,155,113,61,189
198,78,27,89,133,34,59,18,78,111,44,196
195,8,59,168,26,8,172,102,93,33,157,93
"""


def csv_to_dict(csv_string):
    """
    Transform normalization csv into a dictionary
    Keys: well, oligo, product, conc, volume, amount
    """
    lines = [line for line in csv_string.split('\n') if line]
    headers = lines[0].split(',')
    headers = [header.split(' ')[0].lower() for header in headers]
    info_dict = {header: [] for header in headers}
    for line in lines[1:]:
        new_line = line.split(',')
        for key, value in zip(headers, new_line):
            if (key == 'conc') or (key == 'amount'):
                value = int(value)
            elif (key == 'volume'):
                value = int(value)*1000
            info_dict[key].append(value)
    return info_dict


def calculate_volumes(info_dict):
    """
    Find lowest concentration and calculate volume of DNA and buffer to add to
    each well in order to normalize the whole plate to the lowest concentration
    """
    final_conc = min(info_dict['conc'])
    info_dict['dna_vol'] = []
    info_dict['diluent_vol'] = []
    for conc, vol in zip(info_dict['conc'], info_dict['volume']):
        dna_vol = round(final_conc*vol/conc)
        diluent_vol = vol-dna_vol
        info_dict['dna_vol'].append(dna_vol)
        info_dict['diluent_vol'].append(diluent_vol)
    return info_dict


def normalization_of_conc(pipette, info_dict, diluent, source, dest):
    """
    Depend on the calculations, transfer DNA and buffer to each well of plate B
    """
    dna_vol = info_dict['dna_vol']
    diluent_vol = info_dict['diluent_vol']
    loc = info_dict['well']
    source_wells = source.wells(loc)
    dest_wells = dest.wells(loc)
    for vol, source, dest in zip(dna_vol, source_wells, dest_wells):
        pipette.transfer(vol, source, dest)
    pipette.pick_up_tip()
    for vol, dest in zip(diluent_vol, dest_wells):
        if vol:
            pipette.transfer(vol, diluent, dest, new_tip='never')
    pipette.drop_tip()


def volume_to_list(csv_string):
    """
    Takes a csv string of volumes and flattens it to a list
    """
    return [
        int(cell)
        for line in (csv_string.split('\n')) if line.strip()
        for cell in line.split(',') if cell
    ]


def consolidate(pipette, volume_list, source_plate, dest):
    """
    Depending on the list of volumes, transfer the appropriate volume from each
    well to the same destintation
    """
    plate_loc = [well for row in source_plate.rows() for well in row]
    for vol, source in zip(volume_list, plate_loc):
        pipette.transfer(vol, source, dest)


def run_custom_protocol(
    normalization_csv: FileInput=norm_example_csv,
    consolidation_csv: FileInput=cons_example_csv,
    number_of_aliquots: int=10,
    aliquot_volume: int=32
        ):

    """
    Normalization of concentration
    """
    info = csv_to_dict(normalization_csv)
    info = calculate_volumes(info)
    normalization_of_conc(p50, info, diluent, plate_a, plate_b)

    """
    Consolidation to tube
    """
    vols = volume_to_list(consolidation_csv)
    consolidate(p50, vols, plate_b, mixtube)

    """
    Aliquots
    """
    aliquot_loc = tuberack.wells(1, length=number_of_aliquots)
    p50.transfer(aliquot_volume, mixtube, aliquot_loc, new_tip='once')
