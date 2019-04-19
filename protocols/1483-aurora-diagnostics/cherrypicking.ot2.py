from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

csv_example = """
CMPD-ID,PLATE-POSITION,volume_to_be_added_to_the_well
1000,A1,25
1001,A2,25
1002,A3,25
1003,A4,25
1004,A5,25
"""

plate_name = 'optical-96-well'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9.025, 9.025),
        diameter=5.494,
        depth=23.24)


def csv_to_list(csv_string):
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    dests, vols = [], []
    for line in info_list[1:]:
        well_name = line[1]
        volume = float(line[2])
        dests.append(well_name)
        vols.append(volume)
    return dests, vols


def run_custom_protocol(
        volume_csv: FileInput=csv_example,
        dna_volume: float=2):

    # labware setup
    tuberack = labware.load('trough-12row', '2')
    plate = labware.load('optical-96-well', '3', 'Output Plate')
    dna = labware.load('optical-96-well', '6', 'DNA Plate')

    tiprack_10 = labware.load('tiprack-10ul', '5')
    tiprack_300 = labware.load('opentrons-tiprack-300ul', '1')

    # instruments setup
    p300 = instruments.P300_Single(
        mount='left',
        tip_racks=[tiprack_300])

    m10 = instruments.P10_Multi(
        mount='right',
        tip_racks=[tiprack_10])

    # reagent setup
    buff = tuberack.wells('A1')

    dest_wells, volumes = csv_to_list(volume_csv)

    # transfer buffer
    buff_volume_tracker = buff.max_volume()
    p300.pick_up_tip()
    for dest, vol in zip(dest_wells, volumes):
        if buff_volume_tracker < p300.max_volume:
            buff = next(buff)
            buff_volume_tracker = buff.max_volume()
        if p300.current_volume < vol:
            p300.blow_out(buff.top())
            p300.transfer(vol, buff, plate.wells(dest), air_gap=10,
                          new_tip='never')
            buff_volume_tracker -= vol
    p300.drop_tip()

    # transfer samples
    for source, dest in zip(dna.cols(), plate.cols()):
        m10.transfer(dna_volume, source, dest, mix_after=(3, 10))
