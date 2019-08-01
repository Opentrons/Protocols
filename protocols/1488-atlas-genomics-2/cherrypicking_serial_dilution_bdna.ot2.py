from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection
import math

metadata = {
    'protocolName': 'Serial Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# tiprack-custom-200ul
tiprack_200_name = 'tiprack-custom-200ul'
if tiprack_200_name not in labware.list():
    labware.create(
        tiprack_200_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=52,
        volume=200)

# tiprack-custom-10ul
tiprack_10_name = 'tiprack-custom-10ul'
if tiprack_10_name not in labware.list():
    labware.create(
        tiprack_10_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=4.2,
        depth=44,
        volume=10)

# bDNA plate
bDNA_plate_name = 'bDNA plate'
if bDNA_plate_name not in labware.list():
    labware.create(
        bDNA_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=11,
        volume=300)

# trough_300ul
trough_name = 'trough_300ul'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=0,
        depth=41,
        volume=300000)


# plate_200ul_noskirt
plate_name = 'plate_200ul_noskirt'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=21,
        volume=200)

# deep well plate
deep_plate_name = 'deep_well_plate'
if deep_plate_name not in labware.list():
    labware.create(
        deep_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=22,
        volume=500)

# labware setup
sample_plates = [labware.load(plate_name, str(slot))
                 for slot in range(1, 6)]
trough = labware.load(trough_name, '7')
trough_2 = labware.load(deep_plate_name, '9')
tiprack_10 = labware.load(tiprack_10_name, '8')
tiprack_300 = labware.load(tiprack_200_name, '11')

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


def transform_volumes(volume):
    if volume <= 200:
        return [volume]
    else:
        if volume % 200 >= 30 and volume % 200 <= 200:
            return [200] * int(volume // 200) + [volume % 200]
        else:
            volume_list = [200] * int(volume // 200) + [volume % 200]
            new_vol = (volume_list.pop(-2) + volume_list.pop(-1)) / 2
            [volume_list.append(new_vol) for _ in range(2)]
            return volume_list


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
        bDNA_sample_volume: float=40,
        output_plate_type: StringSelection(
            'plate_200ul_noskirt', 'bDNA plate')='bDNA plate'):

    output_plate = labware.load(output_plate_type, '6')

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
    for vol, col in zip(buffer_volumes, buffer_loc):
        for new_vol in transform_volumes(vol):
            if m300.current_volume <= new_vol:
                if diluent_volume_tracker < new_vol * 8:
                    diluent = next(diluent)
                    diluent_volume_tracker = diluent.max_volume()
                m300.blow_out(diluent.top())
                m300.aspirate(200, diluent)
                diluent_volume_tracker -= new_vol * 8
            m300.dispense(new_vol, col)
    m300.drop_tip()

    # serial dilute samples in groups
    for group in dil_groups:
        m10.pick_up_tip()
        for vol, source, dest in zip(sample_vols, group[:-1], group[1:]):
            m10.set_flow_rate(aspirate=5, dispense=10)
            m10.transfer(vol, source, dest, new_tip='never')
            m10.set_flow_rate(aspirate=10, dispense=60)
            m10.mix(5, 10, dest)
        m10.drop_tip()

    m10.set_flow_rate(aspirate=5, dispense=10)

    # reagent setup
    diluent_s = trough_2.wells('A1')
    diluent_s_volume_tracker = diluent_s.max_volume()

    # transfer dilent to bDNA plate
    m300.pick_up_tip()
    m300.aspirate(200, diluent_s)
    for col in output_plate.cols():
        for new_vol in transform_volumes(bDNA_buffer_volume):
            if m300.current_volume <= bDNA_buffer_volume:
                if diluent_s_volume_tracker < bDNA_buffer_volume * 8:
                    diluent_s = next(diluent_s)
                    diluent_s_volume_tracker = diluent_s.max_volume()
                m300.blow_out(diluent_s.top())
                m300.aspirate(200, diluent_s)
                diluent_s_volume_tracker -= bDNA_buffer_volume * 8
            m300.dispense(new_vol, col)
    m300.dispense(diluent_s.top())
    m300.drop_tip()

    # transfer sample to bDNA plate
    bDNA_dests = [col for col in output_plate.cols(starting_column, to='12')]
    if len(bDNA_dests) % 2 == 1:
        bDNA_dests.pop(-1)
    bDNA_sources = [group[-1] for group in dil_groups]
    bDNA_groups = [bDNA_dests[i*2:i*2+2] for i in range(len(dil_groups))]
    if bDNA_sample_volume > 10:
        pipette = m300
    else:
        pipette = m10
    for source, dests in zip(bDNA_sources, bDNA_groups):
        for dest in dests:
            pipette.transfer(bDNA_sample_volume, source, dest)
