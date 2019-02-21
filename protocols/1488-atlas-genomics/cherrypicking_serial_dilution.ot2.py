from opentrons import labware, instruments
from otcustomizers import FileInput
import math

metadata = {
    'protocolName': 'Serial Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
sample_plates = [labware.load('96-flat', str(slot))
                 for slot in range(1, 6)]
trough = labware.load('trough-12row', '7')
bDNA_plate = labware.load('96-flat', '6')
tiprack_10 = labware.load('tiprack-10ul', '8')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '9')

# instruments
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=[tiprack_10])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])


dilution_csv_example = """
Buffer Volume,Sample Volume
45,5
45,5
45,5
90,10
"""


def csv_to_list(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    buffer_vols = []
    sample_vols = []
    for line in info_list[1:]:
        buffer_vols.append(float(line[0]))
        sample_vols.append(float(line[1]))
    return buffer_vols, sample_vols


def run_custom_protocol(
        number_of_samples: int=40,
        dilution_csv: FileInput=dilution_csv_example,
        starting_column: str='3',
        bDNA_buffer_volume: float=300,
        bDNA_sample_volume: float=40):

    buffer_vols, sample_vols = csv_to_list(dilution_csv)

    sample_col_num = math.ceil(number_of_samples / 8)
    dil_cols = len(buffer_vols) + 1
    groups_per_plate = 12 // dil_cols

    # define dilution groups
    dil_groups = [plate.cols(index * dil_cols, length=dil_cols)
                  for plate in sample_plates
                  for index in range(groups_per_plate)][:sample_col_num]

    # reagent setup
    diluent = trough.wells('A1')
    diluent_volume_tracker = diluent.max_volume()

    # distribute diluent
    buffer_volumes = buffer_vols * sample_col_num
    buffer_loc = [col for group in dil_groups for col in group[1:]]
    m300.pick_up_tip()
    m300.aspirate(300, diluent)
    for vol, col in zip(buffer_volumes, buffer_loc):
        if m300.current_volume <= vol:
            if diluent_volume_tracker < vol * 8:
                diluent = next(diluent)
                diluent_volume_tracker = diluent.max_volume()
            m300.aspirate(diluent)
            diluent_volume_tracker -= vol * 8
        m300.dispense(vol, col)
    m300.drop_tip()

    # serial dilute samples in groups
    for group in dil_groups:
        m10.pick_up_tip()
        for vol, source, dest in zip(sample_vols, group[:-1], group[1:]):
            m10.transfer(vol, source, dest, new_tip='never')
            m10.mix(5, 10, dest)
        m10.drop_tip()

    # transfer dilent to bDNA plate
    bDNA_dests = bDNA_plate.cols(starting_column, length=sample_col_num * 2)
    m300.pick_up_tip()
    for col in bDNA_dests:
        if m300.current_volume <= bDNA_buffer_volume:
            if diluent_volume_tracker < bDNA_buffer_volume * 8:
                diluent = next(diluent)
                diluent_volume_tracker = diluent.max_volume()
            m300.aspirate(diluent)
            diluent_volume_tracker -= bDNA_buffer_volume * 8
        m300.dispense(bDNA_buffer_volume, col)
    m300.drop_tip()

    # transfer sample to bDNA plate
    bDNA_sources = [group[-1] for group in dil_groups]
    bDNA_groups = [bDNA_dests[i:i+2] for i in range(len(dil_groups))]
    if bDNA_sample_volume > 10:
        pipette = m300
    else:
        pipette = m10
    for source, dests in zip(bDNA_sources, bDNA_groups):
        pipette.pick_up_tip()
        for dest in dests:
            pipette.transfer(bDNA_sample_volume, source, dest, new_tip='never')
            pipette.mix(5, bDNA_sample_volume, dest)
        pipette.drop_tip()
