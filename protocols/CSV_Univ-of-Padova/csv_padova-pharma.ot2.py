from opentrons import instruments, labware
from otcustomizers import FileInput, StringSelection


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


def well_csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list, re-ordering to match
    Opentrons well order convention (A1, B1, C1, ..., A2, B2, B2, ...)
    """
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    destinations = []
    volumes = []
    for line in info_list[2:]:
        destinations.append(line[1])
        volumes.append(float(line[2]))
    return destinations, volumes


def run_custom_protocol(
        volumes_csv: FileInput=example_csv,
        mix_after_transfer: StringSelection('True', 'False')='True'):

    destinations, volumes = well_csv_to_list(volumes_csv)

    min_volume = min(volumes)

    # instrument setup
    if min_volume <= 30:
        pip = instruments.P50_Single(
            mount='right',
            tip_racks=[tips])
    elif min_volume <= 300:
        pip = instruments.P300_Single(
            mount='right',
            tip_racks=[tips])
    else:
        pip = instruments.P1000_Single(
            mount='right',
            tip_racks=[tips])

    for vol, dest in zip(volumes, destinations):
        pip.pick_up_tip()
        pip.transfer(
            vol, solvent.wells('A1'), plate.wells(dest), new_tip='never')
        if mix_after_transfer == 'True':
            if vol > pip.max_volume:
                vol = pip.max_volume
            pip.mix(3, vol, plate.wells(dest))
        pip.drop_tip()
