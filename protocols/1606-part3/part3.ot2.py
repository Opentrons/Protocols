from opentrons import labware, instruments
from otcustomizers import FileInput

metadata = {
    'protocolName': 'Cell Culture Assay Part 3: Fluorescence Preparation',
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

microtiter_black_name = 'Greiner-microtiter-96'
if microtiter_black_name not in labware.list():
    labware.create(
        microtiter_black_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.96,
        depth=10.9,
        volume=390
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
new_plate = labware.load(culture_plate_24_name, '1', 'new plate')
source_plate = labware.load(culture_plate_24_name, '2', 'source plate')
tips1000 = labware.load('tiprack-1000ul', '3')
rep_plate = labware.load(
                microtiter_black_name,
                '4',
                'black microtiter plate'
            )
media_res = labware.load(reservoir_name, '5', 'media')

# instruments
p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips1000])

# reagent setup
media = media_res.wells('A1')

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
example3 = """,volume to transfer,,,
,1,2,3,4
A,0.692041682919592,0.249687903440589,-1.38121542799499,-1.10314393700325
B,0.121065381994554,0.191387575309833,8.58369280527018,0.687285301638352
C,0.22075056488891,0.147928989074222,0.24630542038257,1.62601686531012
D,,,,
"""


def run_custom_protocol(
        overnight_contents_in_24_well_plate_csv: FileInput = example1,
        destinations_for_96_well_plate_csv: FileInput = example2,
        dilution_volume_csv: FileInput = example3
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
                well = new_plate.wells(well_name)
                all_data[culture.strip()] = [well]

    # parse 96-well destinations CSV
    dest_data = [line.split(',')[1:13]
                 for line in destinations_for_96_well_plate_csv.splitlines()
                 if line][1:9]
    all_data['null'] = [media, []]  # initialize well receiving only media
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

    # transfer proper volume of culture to corresponding well
    volume_data = [line.split(',')[1:]
                   for line in dilution_volume_csv.splitlines() if line][2:]
    for r_ind, row in enumerate(volume_data):
        for c_ind, vol in enumerate(row):
            if vol:
                vol = float(vol)
                if vol > 0:
                    well_name = row_names[r_ind] + str(c_ind+1)
                    source = source_plate.wells(well_name)
                    dest = new_plate.wells(well_name)
                    p1000.pick_up_tip()
                    p1000.transfer(
                        1000,
                        media,
                        dest,
                        blow_out=True,
                        new_tip='never'
                    )
                    p1000.transfer(
                        vol*1000,
                        source,
                        dest,
                        blow_out=True,
                        new_tip='never'
                    )
                    p1000.drop_tip()

    # distribute overnight culture and media from 24- to 96-well plate
    for key in all_data:
        dests = all_data[key][1]
        if key != 'null':
            source = all_data[key][0]
            p1000.distribute(
                200,
                source,
                dests,
                disposal_vol=0
            )
        else:
            p1000.distribute(
                200,
                media,
                dests,
                disposal_vol=0
            )
