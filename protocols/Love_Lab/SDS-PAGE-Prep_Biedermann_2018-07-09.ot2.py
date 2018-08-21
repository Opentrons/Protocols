from opentrons import instruments, labware
from otcustomizers import FileInput

# customization
tris_buff_loc = 'A1'  # location of trisG buffer in trough
tricine_buff_loc = 'A3'  # location of tricine buffer in trough
reducing_agent_loc = 'A5'  # location of reducing agent in trough
mq_water_loc = 'A7'  # location of mQ water in trough


# labware setup
tips_p10 = labware.load('tiprack-10ul', '1')
sample = labware.load('96-PCR-flat', '2')
output_n = labware.load('96-PCR-flat', '3')
tips_p50 = labware.load('tiprack-200ul', '4')
trough = labware.load('trough-12row', '5')
output_r = labware.load('96-PCR-flat', '6')

reducing_csv = """
,1,2,3,4,5,6,7,8,9,10,11,12
A,TrisG-R,TrisG-N,Tricine-R,Tricine-N,TrisG-Blank,Tricine-Blank,,,,,,
B,Tricine-Blank,TrisG-R,TrisG-N,Tricine-R,Tricine-N,TrisG-Blank,,,,,,
C,TrisG-Blank,Tricine-Blank,TrisG-R,TrisG-N,Tricine-R,Tricine-N,,,,,,
D,Tricine-N,TrisG-Blank,Tricine-Blank,TrisG-R,TrisG-N,Tricine-R,,,,,,
E,,,,,,,,,,,,
F,,,,,,,,,,,,
G,,,,,,,,,,,,
H,,,,,,,,,,,,
"""
non_csv = """
,1,2,3,4,5,6,7,8,9,10,11,12
A,TrisG-R,TrisG-N,Tricine-R,Tricine-N,TrisG-Blank,Tricine-Blank,,,,,,
B,Tricine-Blank,TrisG-R,TrisG-N,Tricine-R,Tricine-N,TrisG-Blank,,,,,,
C,TrisG-Blank,Tricine-Blank,TrisG-R,TrisG-N,Tricine-R,Tricine-N,,,,,,
D,Tricine-N,TrisG-Blank,Tricine-Blank,TrisG-R,TrisG-N,Tricine-R,,,,,,
E,,,,,,,,,,,,
F,,,,,,,,,,,,
G,,,,,,,,,,,,
H,,,,,,,,,,,,
"""

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tips_p10]
)

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tips_p50]
)

# variables and reagents setup
tris_buff = trough.wells(tris_buff_loc)
tricine_buff = trough.wells(tricine_buff_loc)
reducing_agent = trough.wells(reducing_agent_loc)
mq_water = trough.wells(mq_water_loc)


def transpose_matrix(m):
    return [[r[i] for r in reversed(m)] for i in range(len(m[0]))]


def flatten_matrix(m):
    return [cell for row in m for cell in row]


def well_csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list, re-ordering to match
    Opentrons well order convention (A1, B1, C1, ..., A2, B2, B2, ...)
    """
    data = [
        line.split(',')
        for line in reversed(csv_string.split('\n')) if line.strip()
        if line
    ]
    return flatten_matrix(transpose_matrix(data))
    return flatten_matrix(data)


def wells_only(csv_string):
    list_of_wells = [str(cell) for cell in well_csv_to_list(csv_string)]

    list_of_wells = list_of_wells[9:]
    list_of_wells = [x for i, x in enumerate(list_of_wells) if i % 9 != 0]
    return list_of_wells


def prepare_wells(plate_layout, output_plate, reducing_loc):
    tris_blank = []
    tris_test = []
    tricine_blank = []
    tricine_test = []

    well_count = 0

    for item in plate_layout:
        item = item.lower()
        if item.startswith('tris'):
            if item.endswith('blank'):
                tris_blank.append(well_count)
            else:
                tris_test.append(well_count)
        elif item.lower().startswith('tric'):
            if item.endswith('blank'):
                tricine_blank.append(well_count)
            else:
                tricine_test.append(well_count)

        well_count = well_count + 1

    # transfer buffers
    volumes = [15, 10, 10, 7.5]
    locations = [tris_buff, tricine_buff, tris_buff, tricine_buff]
    destinations = [tris_test, tricine_test, tris_blank, tricine_blank]
    pipettes = [p50, p10, p10, p10]

    for vol, loc, dest, pip in zip(volumes, locations, destinations, pipettes):
        pip.pick_up_tip()
        pip.transfer(vol, loc, output_plate.wells(dest), new_tip='never')
        pip.drop_tip()

    # transfer water or reducing agent
    volumes = [3, 2, 10, 7.5]
    locations = [reducing_loc, reducing_loc, mq_water, mq_water]

    for vol, loc, dest in zip(volumes, locations, destinations):
        p10.pick_up_tip()
        p10.transfer(vol, loc, output_plate.wells(dest), new_tip='never')
        p10.drop_tip()

    # transfer sample
    p50.pick_up_tip()
    p50.transfer(12, sample.wells(tris_test), output_plate.wells(tris_test),
                 new_tip='never')
    p50.drop_tip()

    p10.pick_up_tip()
    p10.transfer(8, sample.wells(tricine_test),
                 output_plate.wells(tricine_test), new_tip='never')
    p10.drop_tip()


def run_custom_protocol(reducing_csv: FileInput=reducing_csv,
                        non_csv: FileInput= non_csv):

    reducing = wells_only(reducing_csv)
    non = wells_only(non_csv)

    prepare_wells(reducing, output_r, reducing_agent)
    prepare_wells(non, output_n, mq_water)
