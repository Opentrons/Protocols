from opentrons import instruments, labware, robot
from otcustomizers import FileInput

example_csv = """
Source labware label,Source position,Dest labware label,Dest position,Volume
C10-T7 - 03,289,Plate 11,10,160ul
C10-T7 - 03,178,Plate 11,11,160ul
C10-T7 - 03,210,Plate 11,12,160ul
C10-T7 - 03,306,Plate 11,13,160ul
C10-T7 - 03,211,Plate 11,14,160ul
C10-T7 - 03,355,Plate 11,15,160ul
C10-T7 - 03,4,Plate 11,18,160ul
C10-T7 - 03,84,Plate 11,19,160ul
C10-T7 - 03,196,Plate 11,20,160ul
C10-T7 - 03,212,Plate 11,21,160ul
C10-T7 - 03,276,Plate 11,22,160ul
C10-T7 - 03,308,Plate 11,23,160ul
C10-T7 - 03,53,Plate 11,26,160ul
C10-T7 - 03,69,Plate 11,27,160ul
C10-T7 - 03,101,Plate 11,28,160ul
C10-T7 - 03,181,Plate 11,29,160ul
C10-T7 - 03,197,Plate 11,30,160ul
C10-T7 - 03,153,Plate 11,31,160ul
C10-T7 - 03,265,Plate 11,34,160ul
C10-T7 - 03,154,Plate 11,35,160ul
C10-T7 - 03,346,Plate 11,36,160ul
C10-T7 - 03,59,Plate 11,37,160ul
C10-T7 - 03,171,Plate 11,38,160ul
C10-T7 - 03,283,Plate 11,39,160ul
C10-T7 - 02,369,Plate 11,42,160ul
C10-T7 - 02,146,Plate 11,43,160ul
C10-T7 - 02,162,Plate 11,44,160ul
C10-T7 - 02,51,Plate 11,45,160ul
C10-T7 - 02,195,Plate 11,46,160ul
C10-T7 - 02,323,Plate 11,47,160ul
C10-T7 - 02,68,Plate 11,50,160ul
C10-T7 - 02,100,Plate 11,51,160ul
C10-T7 - 02,197,Plate 11,52,160ul
C10-T7 - 02,102,Plate 11,53,160ul
C10-T7 - 02,200,Plate 11,54,160ul
C10-T7 - 02,280,Plate 11,55,160ul
C10-T7 - 02,121,Plate 11,58,160ul
C10-T7 - 02,185,Plate 11,59,160ul
C10-T7 - 02,313,Plate 11,60,160ul
C10-T7 - 02,314,Plate 11,61,160ul
C10-T7 - 02,140,Plate 11,62,160ul
C10-T7 - 02,156,Plate 11,63,160ul
C10-T7 - 02,236,Plate 11,66,160ul
C10-T7 - 02,221,Plate 11,67,160ul
C10-T7 - 02,80,Plate 11,68,160ul
C10-T7 - 01,34,Plate 11,69,160ul
C10-T7 - 01,275,Plate 11,70,160ul
C10-T7 - 01,132,Plate 11,71,160ul
C10-T7 - 01,164,Plate 11,74,160ul
C10-T7 - 01,180,Plate 11,75,160ul
C10-T7 - 01,197,Plate 11,76,160ul
C10-T7 - 01,182,Plate 11,77,160ul
C10-T7 - 01,215,Plate 11,78,160ul
C10-T7 - 01,247,Plate 11,79,160ul
C10-T7 - 01,136,Plate 11,82,160ul
C10-T7 - 01,216,Plate 11,83,160ul
C10-T7 - 01,248,Plate 11,84,160ul
C10-T7 - 01,361,Plate 11,85,160ul
C10-T7 - 01,170,Plate 11,86,160ul
C10-T7 - 01,202,Plate 11,87,160ul
C10-T7 - 01,266,Plate 12,10,160ul
C10-T7 - 01,330,Plate 12,11,160ul
C10-T7 - 01,11,Plate 12,12,160ul
C10-T7 - 01,27,Plate 12,13,160ul
C10-T7 - 01,59,Plate 12,14,160ul
C10-T7 - 01,75,Plate 12,15,160ul
C10-T7 - 01,171,Plate 12,18,160ul
C10-T7 - 01,203,Plate 12,19,160ul
C10-T7 - 01,44,Plate 12,20,160ul
C10-T7 - 01,76,Plate 12,21,160ul
C10-T7 - 01,236,Plate 12,22,160ul
C10-T7 - 01,332,Plate 12,23,160ul
C10-T7 - 01,61,Plate 12,26,160ul
C10-T7 - 01,158,Plate 12,27,160ul
C10-T7 - 01,318,Plate 12,28,160ul
C10-T7 - 01,334,Plate 12,29,160ul
C10-T7 - 01,366,Plate 12,30,160ul
C10-T7 - 01,382,Plate 12,31,160ul
C10-T7 - 01,63,Plate 12,34,160ul
C10-T7 - 01,79,Plate 12,35,160ul
C10-T7 - 01,111,Plate 12,36,160ul
C10-T7 - 01,383,Plate 12,37,160ul

"""


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


def split_cols(script_csv: 'FileInput'=example_csv):
    script = [str(cell) for cell in well_csv_to_list(script_csv)]

    source_plate = script[1:script.index('Source position')]
    source_well = script[script.index('Source position') +
                         1:script.index('Dest labware label')]
    dest_plate = script[script.index('Dest labware label') +
                        1:script.index('Dest position')]
    dest_well = script[script.index('Dest position') +
                       1:script.index('Volume')]
    sample_vol = script[script.index('Volume')+1:]

    source_well_2 = []
    dest_well_2 = []
    sample_vol_2 = []

    for swell, dwell, volume in zip(source_well, dest_well, sample_vol):
        source_well_2.append(int(swell))
        dest_well_2.append(int(dwell))
        sample_vol_2.append(int(volume[:-2]))

    return source_plate, source_well_2, dest_plate, dest_well_2, sample_vol_2


def identify_unique_plate(source_plate, dest_plate):
    unique_source = []
    for item in source_plate:
        if item not in unique_source:
            unique_source.append(item)

    unique_dest = []
    for item in dest_plate:
        if item not in unique_dest:
            unique_dest.append(item)

    return unique_source, unique_dest


def run_custom_protocol(
    script_csv: FileInput=example_csv
        ):

    # VARIABLES AND REAGENTS SETUP
    source_plate, source_well, dest_plate, dest_well, sample_vol = split_cols(
        script_csv)
    source_names, dest_names = identify_unique_plate(source_plate, dest_plate)

    total_samples = len(sample_vol) + 8
    # counts total number for pipette tips needed for protocol

    # LABWARE SETUP
    # trough
    trough = labware.load('trough-12row', '2')

    # tipracks
    tips = labware.load('tiprack-200ul', '1')
    total_samples = total_samples - 96

    ind = 0
    tip_names = ['tips2', 'tips3', 'tips4']
    # adds more tipracks if necessary based on number of samples
    while total_samples > 96:
        tip_names[ind] = labware.load('tiprack-200ul', str(2*(2+ind)))
        total_samples = total_samples - 96
        ind = ind + 1

    # source 384-well plates
    slot_num = 5
    for plate in source_names:  # loads each unique source plate
        vars()[plate] = labware.load('384-plate', str(slot_num))
        slot_num = slot_num + 3

    # destination 96-well plates
    empty_slots = [slot.get_name()
                   for slot in robot.deck if len(slot.children_by_name) == 0]
    slot_ind = 0
    for plate in dest_names:  # loads each unique destination plate
        vars()[plate] = labware.load('96-PCR-flat', empty_slots[slot_ind])
        slot_ind = slot_ind + 1

    # INSTRUMENT SETUP
    single = instruments.P300_Single(
        mount='left',
        tip_racks=[tips]
    )

    multi = instruments.P300_Multi(
        mount='right',
        tip_racks=[tips]
    )

    # BEGIN PROTOCOL
    # fill troughs with media
    multi.pick_up_tip()
    # tip_start_loc = multi.current_tip()
    for plate in dest_names:
        multi.transfer(160, trough.wells('A1'), vars()[plate].rows('A'),
                       new_tip='never')
    multi.drop_tip()

    single.start_at_tip(tips.wells('A2'))
    # transfer sample to destination
    for s_plate, s_well, d_plate, d_well, vol in zip(
            source_plate, source_well, dest_plate, dest_well, sample_vol):
        single.pick_up_tip()
        single.mix(3, vol/2, vars()[s_plate].well(s_well))
        single.transfer(vol, vars()[s_plate].well(s_well),
                        vars()[d_plate].well(d_well), new_tip='never')
        single.drop_tip()
