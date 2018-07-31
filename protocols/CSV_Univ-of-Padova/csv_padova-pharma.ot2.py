from opentrons import instruments, labware

# customization
mix = 1  # if you want to mix, mix = 1; no mix, mix = 0
max_volume = 43  # adjust based on largest volume in CSV

# labware setup
tips = labware.load('tiprack-200ul', '1')
solvent = labware.load('tube-rack-15_50ml', '2')
plate = labware.load('96-PCR-flat', '3')

example_csv = """
#COMMENT LINE,,
# CMPD-ID,PLATE-POSITION,volume_to_be_added_to_the_weel (uL)
1000,A5,25
1001,A6,32
1004,B4,43

"""

# instrument setup
if max_volume <= 50:
    pip = instruments.P50_Single(
        mount='right',
        tip_racks=[tips])
elif max_volume <= 300:
    pip = instruments.P300_Single(
        mount='right',
        tip_racks=[tips])
else:
    pip = instruments.P1000_Single(
        mount='right',
        tip_racks=[tips])


# variables and reagents setup
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


def run_custom_protocol(
        volumes_csv: 'FileInput'=example_csv):
    script = [str(cell) for cell in well_csv_to_list(volumes_csv)]

    well_loc = script[script.index('PLATE-POSITION')+1:script.index(
            'volume_to_be_added_to_the_weel (uL)')]
    volumes = script[script.index('volume_to_be_added_to_the_weel (uL)')+1:]

    ind = 0
    for vol in volumes:
        volumes[ind] = int(vol)
        ind = ind + 1

    ind = 0
    for vol in volumes:
        pip.pick_up_tip()
        pip.transfer(vol, solvent.wells('A1'), plate.wells(well_loc[ind]),
                     new_tip='never')
        if mix == 1:
            pip.mix(3, vol, plate.wells(well_loc[ind]))
        pip.drop_tip()
        ind = ind+1


run_custom_protocol(**{'volumes_csv': example_csv})
