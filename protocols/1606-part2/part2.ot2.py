from opentrons import labware, instruments, robot
from otcustomizers import FileInput

metadata = {
    'protocolName': 'Cell Culture Assay Part 2: OD Calculation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
culture_plate_24_name = 'Costar-culture-plate-24'
if culture_plate_24_name not in labware.list():
    labware.create(
        culture_plate_24_name,
        grid=(6, 4),
        spacing=(19.3, 19.3),
        diameter=16.26,
        depth=17.4,
        volume=3400
    )

microtiter_clear_name = 'Corning-microtiter-96'
if microtiter_clear_name not in labware.list():
    labware.create(
        microtiter_clear_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.86,
        depth=10.67,
        volume=360
    )

reservoir_name = 'Axygen-290ml-reservoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=8,
        depth=37,
        volume=290000
    )

# load labware
source_plate = labware.load(culture_plate_24_name, '1', 'source plate')
media_res = labware.load(reservoir_name, '2', 'media')
pbs_res = labware.load(reservoir_name, '3', 'PBS')
rep_plate = labware.load(
                microtiter_clear_name,
                '4',
                'clear microtiter plate'
            )
tips1000 = labware.load('tiprack-1000ul', '5')
tips10 = labware.load('tiprack-10ul', '6')

# instruments
p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips1000])
p10 = instruments.P10_Single(mount='left', tip_racks=[tips10])

# reagent setup
media = media_res.wells('A1')
pbs = pbs_res.wells('A1')

# csv defaults
example1 = """,1,2,3,4
A,ycEW000_b3_ct in SC-URA,ycEW000_b4_ct in SC-URA,ycEW000_b3_rt in SC-URA,ycEW\
000_b4_rt in SC-URA
B,ycEW163_b3_ct in SC-URA,ycEW163_b4_ct in SC-URA,ycEW163_b3_rt in SC-URA,ycEW\
163_b4_rt in SC-URA
C,ycEW081_b3_ct in SC-URA,ycEW081_b4_ct in SC-URA,ycEW081_b3_rt in SC-URA,ycEW\
081_b4_rt in SC-URA
D,media,,,
,,,,
,,,,
,,,,
,,,,
,,,,
"""
example2 = """,1,2,3,4,5,6,7,8,9,10,11,12,,,,,
A,,,null in SC-URA,null in SC-URA,null in SC-URA,null in SC-URA,null in SC-URA\
,null in SC-URA,null in SC-URA,null in SC-URA,,,,,,,
B,,,ycEW000_b3_ct in SC-URA,ycEW000_b3_ct in SC-URA,ycEW000_b3_ct in SC-URA,yc\
EW000_b3_ct in SC-URA,ycEW000_b3_rt in SC-URA,ycEW000_b3_rt in SC-URA,ycEW000_\
b3_rt in SC-URA,ycEW000_b3_rt in SC-URA,,,,,,,
C,,,ycEW000_b4_ct in SC-URA,ycEW000_b4_ct in SC-URA,ycEW000_b4_ct in SC-URA,yc\
EW000_b4_ct in SC-URA,ycEW000_b4_rt in SC-URA,ycEW000_b4_rt in SC-URA,ycEW000_\
b4_rt in SC-URA,ycEW000_b4_rt in SC-URA,,,,,,,
D,,,ycEW163_b3_ct in SC-URA,ycEW163_b3_ct in SC-URA,ycEW163_b3_ct in SC-URA,yc\
EW163_b3_ct in SC-URA,ycEW163_b3_rt in SC-URA,ycEW163_b3_rt in SC-URA,ycEW163_\
b3_rt in SC-URA,ycEW163_b3_rt in SC-URA,,,,,,,
E,,,ycEW163_b4_ct in SC-URA,ycEW163_b4_ct in SC-URA,ycEW163_b4_ct in SC-URA,yc\
EW163_b4_ct in SC-URA,ycEW163_b4_rt in SC-URA,ycEW163_b4_rt in SC-URA,ycEW163_\
b4_rt in SC-URA,ycEW163_b4_rt in SC-URA,,,,,,,
F,,,ycEW081_b3_ct in SC-URA,ycEW081_b3_ct in SC-URA,ycEW081_b3_ct in SC-URA,yc\
EW081_b3_ct in SC-URA,ycEW081_b3_rt in SC-URA,ycEW081_b3_rt in SC-URA,ycEW081_\
b3_rt in SC-URA,ycEW081_b3_rt in SC-URA,,,,,,,
G,,,ycEW081_b4_ct in SC-URA,ycEW081_b4_ct in SC-URA,ycEW081_b4_ct in SC-URA,yc\
EW081_b4_ct in SC-URA,ycEW081_b4_rt in SC-URA,ycEW081_b4_rt in SC-URA,ycEW081_\
b4_rt in SC-URA,ycEW081_b4_rt in SC-URA,,,,,,,
H,,,null in SC-URA,null in SC-URA,null in SC-URA,null in SC-URA,null in SC-URA\
,null in SC-URA,null in SC-URA,null in SC-URA,,,,,,,
"""


def run_custom_protocol(
        overnight_contents_in_24_well_plate_csv: FileInput = example1,
        destinations_for_96_well_plate_csv: FileInput = example2,
):

    # initialize data storage dictionary
    all_data = {}
    row_names = 'ABCDEFGH'

    """              start CSV parsing               """

    # parse overnight contents CSV
    overnight_data = [line.split(',')[1:]
                      for line in
                      overnight_contents_in_24_well_plate_csv.splitlines()
                      if line][1:]
    for r_ind, row in enumerate(overnight_data):
        for c_ind, culture in enumerate(row):
            if culture and culture != 'media':
                well_name = row_names[r_ind] + str(c_ind+1)
                well = source_plate.wells(well_name)
                all_data[culture.strip()] = [well]

    # parse 96-well destinations CSV
    dest_data = [line.split(',')[1:13]
                 for line in destinations_for_96_well_plate_csv.splitlines()
                 if line][1:9]
    # initialize well receiving only media
    all_data['null'] = [media, []]
    for r_ind, row in enumerate(dest_data):
        for c_ind, culture in enumerate(row):
            if (culture.strip() in all_data and
                    culture.strip().split(' ')[0] != 'null'):
                well_name = row_names[r_ind] + str(c_ind+1)
                well = rep_plate.wells(well_name)
                if len(all_data[culture.strip()]) == 1:
                    all_data[culture.strip()].append([well])
                else:
                    all_data[culture.strip()][1].append(well)
            elif culture.strip().split(' ')[0] == 'null':
                well_name = row_names[r_ind] + str(c_ind+1)
                well = rep_plate.wells(well_name)
                all_data['null'][1].append(well)

    """              end CSV parsing                 """

    robot.home()
    robot.pause('Pellet the cells in the 24 well plate using a table top centr\
ifuge (3000 rpm for 3 min). Quickly replace the plate in slot 1 and resume to \
ensure cells do not dislodge from the pellet.')

    # remove media
    for key in all_data:
        if key != 'null':
            p1000.transfer(
                1000,
                all_data[key][0],
                p1000.trash_container.top(),
                blow_out=True,
                new_tip='always'
            )

    # distribute PBS on the side of the wells
    p1000.pick_up_tip()
    for key in all_data:
        if key != 'null':
            well = all_data[key][0]
            offset = well.from_center(r=0.95, h=1.0, theta=0)
            dest = (well, offset)
            p1000.transfer(
                1000,
                pbs,
                dest,
                blow_out=True,
                new_tip='never'
            )
    p1000.drop_tip()

    robot.pause('Resuspend the cells by putting it back on the shaker set at \
180 rpm for a few seconds. Pellet the cells in the 24 well plate using a table\
top centrifuge (3000 rpm for 3 min). Quickly replace the plate in slot 1 and \
resume to ensure cells do not dislodge from the pellet.')

    # remove PBS
    for key in all_data:
        if key != 'null':
            p1000.transfer(
                1000,
                all_data[key][0],
                p1000.trash_container.top(),
                blow_out=True,
                new_tip='always'
            )

    # distribute media on the side of the wells
    p1000.pick_up_tip()
    for key in all_data:
        if key != 'null':
            well = all_data[key][0]
            offset = well.from_center(r=0.95, h=1.0, theta=0)
            dest = (well, offset)
            p1000.transfer(
                1000,
                media,
                dest,
                blow_out=True,
                new_tip='never'
            )
    p1000.drop_tip()

    robot.pause('Resuspend the cells by putting it back on the shaker set at \
180 rpm for a few seconds.')

    # distribute overnight culture and media from 24- to 96-well plate
    for key in all_data:
        dests = all_data[key][1]
        if key != 'null':
            source = all_data[key][0]
            p10.transfer(20, source, dests)
            media_vol = 180
        else:
            media_vol = 200
        p1000.distribute(
            media_vol,
            media,
            dests,
            disposal_vol=0
        )

    robot.comment('Take the clear microtiter plate to the Tecan reader. Resume \
to finish.')
