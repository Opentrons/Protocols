from opentrons import instruments, labware, robot
from otcustomizers import FileInput

metadata = {
    'protocolName': 'Transfer samples from 384-well plate to 96-well plate',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'}

# importing Agenus castom labware defenitions:

# 384 corning square flat bottom
plate_name = '384_corning_FlatBottom'
if plate_name not in labware.list():
    custom_plate = labware.create(
        '384_corning_FlatBottom',  # name of your labware
        grid=(24, 16),   # specify amount of (columns, rows)
        spacing=(4.5, 4.5),  # distances (mm) between each (column, row)
        diameter=3.5,  # diameter (mm) of each well on the plate
        depth=11.8,  # depth (mm) of each well on the plate
        volume=100)

# Biotix trough (Biotix empty tip box without the green tip nest)
plate_name = 'Biotix_Trough'
if plate_name not in labware.list():
    custom_plate = labware.create(
        'Biotix_Trough',   # name of your labware
        grid=(12, 8),     # specify amount of (columns, rows)
        spacing=(9, 9),    # distances (mm) between each (column, row)
        diameter=7,     # diameter (mm) of each well on the plate
        depth=38,     # depth (mm) of each well on the plate
        volume=250000)

# 96 greiner cellstar round flat bottom
plate_name = '96_greiner_cellstar_FlatBottom'
if plate_name not in labware.list():
    custom_plate = labware.create(
        '96_greiner_cellstar_FlatBottom',  # name of you labware
        grid=(12, 8),  # specify amount of (columns, rows)
        spacing=(9, 9),  # distances (mm) between each (column, row)
        diameter=7,  # diameter (mm) of each well on the plate
        depth=11,  # depth (mm) of each well on the plate
        volume=350)

# labware setup
trough = labware.load('Biotix_Trough', '2')
plates_384 = [labware.load('384_corning_FlatBottom', slot)
              for slot in ['5', '8', '11']]
plates_96 = [labware.load('96_greiner_cellstar_FlatBottom', slot)
             for slot in ['3', '4']]
tipracks = [labware.load('tiprack-200ul', slot)
            for slot in ['1', '6', '9', '7', '10']]

# instrument setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tipracks)

# Changing the phead aspirate/dispense speeds
p300.set_flow_rate(aspirate=150, dispense=300)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)

# Changing the mhead aspirate/dispense speeds
m300.set_flow_rate(aspirate=50, dispense=100)


example_csv = """
Source Plate Location,Source Well,Dest Plate Location,Dest Well,Volume
11,0,3,95,160
11,1,3,94,160
11,2,3,93,160
8,3,3,92,160
8,4,4,91,160
8,5,4,90,160
5,6,4,89,160
5,7,4,88,160
5,8,4,87,160
"""


def well_csv_to_list(csv_string):
    """
    convert csv string into lists: sources, dests, volumes
    """
    sources = []
    volumes = []
    dests = []
    info_list = [cell for line in csv_string.splitlines() if line
                 for cell in [line.split(',')]]
    for line in info_list[1:]:
        for plate in plates_384:
            if plate.get_parent() == robot.deck.children_by_name[line[0]]:
                source = plate.wells(int(line[1]))
        for plate in plates_96:
            if plate.get_parent() == robot.deck.children_by_name[line[2]]:
                dest = plate.wells(int(line[3]))
        vol = int(line[4])
        sources.append(source)
        dests.append(dest)
        volumes.append(vol)

    return sources, dests, volumes


def run_custom_protocol(
        media_volume: float=160,
        script_csv: FileInput=example_csv):

    sources, dests, volumes = well_csv_to_list(script_csv)

    # fill 96-well plates with media
    dest_plate_list = []
    for dest in dests:
        if dest.get_parent() not in dest_plate_list:
            dest_plate_list.append(dest.get_parent())
    dest_loc = [col
                for plate in dest_plate_list for col in plate.cols()]
    m300.distribute(
        media_volume, trough.wells('A1'), dest_loc, blow_out=True,
        new_tip='once')

    p300.start_at_tip(tipracks[0].wells('A2'))

    # transfer sample to destination
    for source, dest, vol in zip(sources, dests, volumes):
        p300.pick_up_tip()
        p300.mix(5, 25, source)
        p300.transfer(vol, source, dest, new_tip='never')
        p300.mix(2, 160, dest)
        p300.drop_tip()
