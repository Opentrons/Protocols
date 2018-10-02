from opentrons import instruments, labware, robot
from otcustomizers import FileInput

# labware setup
trough = labware.load('trough-12row', '2')
plates_384 = [labware.load('384-plate', slot)
              for slot in ['5', '8', '11']]
plates_96 = [labware.load('96-PCR-flat', slot)
             for slot in ['3', '4']]
tipracks = [labware.load('tiprack-200ul', slot)
            for slot in ['1', '6', '9', '7', '10']]

# instrument setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=tipracks)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)


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
    info_list = [cell for line in example_csv.splitlines() if line
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
        media_volume, trough.wells('A1'), dest_loc, new_tip='once')

    p300.start_at_tip(tipracks[0].wells('A2'))

    # transfer sample to destination
    for source, dest, vol in zip(sources, dests, volumes):
        p300.transfer(vol, source, dest, mix_after=(3, vol/2))
