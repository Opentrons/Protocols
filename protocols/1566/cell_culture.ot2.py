from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput
import csv
import math
import datetime

metadata = {
    'protocolName': 'Cell Culture Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom plate and tips
plate_name = 'Corning-96-flat'
if plate_name not in labware.list():
    labware.create(plate_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=6.86,
                   depth=10.67,
                   volume=200)

tiprack_100_name = 'tipone-tiprack-100ul'
tiprack_300_name = 'tipone-tiprack-300ul'
for name in [tiprack_100_name, tiprack_300_name]:
    if name not in labware.list():
        labware.create(
            name,
            grid=(12, 8),
            spacing=(9, 9),
            diameter=5,
            depth=60)

# labware
source_plate = labware.load(plate_name, '1')
dest_plate = labware.load(plate_name, '2')
tips300 = [labware.load(tiprack_300_name, slot)
           for slot in ['4', '7', '10']]
tips50 = [labware.load(tiprack_100_name, slot)
          for slot in ['5', '8', '11']]
tubes = labware.load('opentrons-tuberack-50ml', '6')

# pipettes
p300 = instruments.P300_Single(mount='left', tip_racks=tips300)
p50 = instruments.P50_Single(mount='right', tip_racks=tips50)

# reagent setup
media = tubes.wells('A1')
PBS = tubes.wells('A2')
trypsin = tubes.wells('A3')
discharge = tubes.wells('B1')
liquid_trash = tubes.wells('B2')

csv_0 = """1 120 120,0 0 0,0 0 0,1 0 0,1 75 75,0 0 0,0 0 0,1 135 135,0 0 0,1 0\
 0,1 75 75,0 0 0
0 0 0,1 120 120,1 120 120,1 0 0,1 0 0,0 0 0,1 75 75,1 135 135,1 75 75,1 120 \
120,1 120 120,1 0 0
0 0 0,1 120 120,0 0 0,0 0 0,0 0 0,1 120 120,1 75 75,0 0 0,1 0 0,0 0 0,0 0 0,1 \
120 120
1 135 135,0 0 0,1 135 135,0 0 0,0 0 0,1 120 120,0 0 0,0 0 0,0 0 0,0 0 0,0 0\
 0,0 0 0
0 0 0,0 0 0,1 0 0,1 75 75,0 0 0,1 120 120,0 0 0,1 75 75,0 0 0,1 135 135,0 0\
 0,0 0 0
1 75 75,1 75 75,0 0 0,0 0 0,0 0 0,1 120 120,1 0 0,0 0 0,1 120 120,0 0 0,0 0\
 0,1 75 75
1 75 75,0 0 0,0 0 0,1 120 120,1 135 135,0 0 0,0 0 0,1 0 0,0 0 0,1 75 75,1 120\
 120,0 0 0
0 0 0,1 0 0,1 75 75,1 120 120,1 135 135,0 0 0,1 135 135,1 120 120,1 120 120,1\
 75 75,1 135 135,1 135 135"""

csv_1 = """1 120 30,0 0 0,0 0 0,1 0 150,1 75 75,0 0 0,0 0 0,1 135 15,0 0 0,1\
 0 150,1 75 75,0 0 0
0 0 0,1 120 30,1 120 30,1 0 150,1 0 150,0 0 0,1 75 75,1 135 15,1 75 75,1 120\
 30,1 120 30,1 0 150
0 0 0,1 120 30,0 0 0,0 0 0,0 0 0,1 120 30,1 75 75,0 0 0,1 0 150,0 0 0,0 0 0,1\
 120 30
1 135 15,0 0 0,1 135 15,0 0 0,0 0 0,1 120 30,0 0 0,0 0 0,0 0 0,0 0 0,0 0 0,0\
 0 0
0 0 0,0 0 0,1 0 150,1 75 75,0 0 0,1 120 30,0 0 0,1 75 75,0 0 0,1 135 15,0 0\
 0,0 0 0
1 75 75,1 75 75,0 0 0,0 0 0,0 0 0,1 120 30,1 0 150,0 0 0,1 120 30,0 0 0,0\
 0 0,1 75 75
1 75 75,0 0 0,0 0 0,1 120 30,1 135 15,0 0 0,0 0 0,1 0 150,0 0 0,1 75 75,1\
 120 30,0 0 0
0 0 0,1 0 150,1 75 75,1 120 30,1 135 15,0 0 0,1 135 15,1 120 30,1 120 30,1 75\
 75,1 135 15,1 135 15"""


def run_custom_protocol(CSV_for_XYZ: FileInput = csv_0,
                        P: StringSelection('yes', 'no') = 'no',
                        T: int = 10):

    # setup source and destination wells in row order
    all_source = [well for row in source_plate.rows() for well in row]
    all_dest = [well for row in dest_plate.rows() for well in row]

    # initialize lists for X, Y, and Z
    X = []
    Y = []
    Z = []

    # initialize height trackers for PBS, media, and trypsin
    h_track = {'PBS': -11,
               'media': -11,
               'trypsin': -11}
    r_cyl = 13.5
    pi = math.pi

    # function to track the heights of each of the 3 reagent tubes to ensure
    # the pipette does not submerge into the liquid
    def height_tracker(vol, tube):
        nonlocal h_track
        dh = vol/(pi*(r_cyl**2))
        h_track[tube] -= dh

    # function to fill X, Y, and Z with 96 values each, moving across rows then
    # down columns
    def CSV_parser(file):
        nonlocal X
        nonlocal Y
        nonlocal Z
        for row in file.splitlines():
            for well in row.split(','):
                vals = well.split()
                X.append(int(vals[0]))
                Y.append(float(vals[1]))
                Z.append(float(vals[2]))

    # function to discharge 100ul from specified wells
    def discharge_supernatant():
        nonlocal X
        nonlocal all_source

        # discharge 100ul from specified wells
        p300.pick_up_tip()
        counter = 0
        for switch, well in zip(X, all_source):
            if switch == 1:
                # go almost to side of well, about 1mm from bottom
                offset = well.from_center(r=0.9, theta=0, h=-0.8)
                edge = (well, offset)
                p300.aspirate(100, edge)
                counter += 1
                if counter == 3:
                    p300.dispense(300, discharge)
                    p300.blow_out(discharge)
                    counter = 0
        if counter > 0:
            p300.blow_out(discharge)
        p300.drop_tip()

    # choose correct CSV depending on case of P
    if P == 'yes':
        CSV_for_XYZ = csv_0
    else:
        CSV_for_XYZ = csv_1
    CSV_parser(CSV_for_XYZ)

    # discharge 100ul from specified wells
    discharge_supernatant()

    # set dispense speed to 1/4 default
    p300.set_flow_rate(dispense=75)

    # dispense 100ul PBS to specified wells
    p300.pick_up_tip()
    counter = 0
    height_tracker(300, 'PBS')
    p300.aspirate(300, PBS.top(h_track['PBS']))
    for switch, well in zip(X, all_source):
        if switch == 1:
            # go to the side of the well, nearly at the top
            offset = well.from_center(r=1, theta=0, h=0.9)
            dest = (well, offset)
            p300.dispense(100, dest)
            counter += 1
            if counter == 3:
                p300.blow_out(PBS.top())
                height_tracker(300, 'PBS')
                p300.aspirate(300, PBS.top(h_track['PBS']))
                counter = 0
    if counter > 0:
        p300.blow_out(PBS)
    p300.drop_tip()

    # reset dispense speed to default
    p300.set_flow_rate(dispense=300)

    # discharge 100ul PBS from specified wells
    discharge_supernatant()

    # dispense 30ul trypsin to specified wells
    p300.pick_up_tip()
    counter = 0
    height_tracker(300, 'trypsin')
    p300.aspirate(300, trypsin.top(h_track['trypsin']))
    for switch, well in zip(X, all_source):
        if switch == 1:
            p300.dispense(30, well.top())
            counter += 1
            if counter == 10:
                p300.blow_out(trypsin.top())
                height_tracker(300, 'trypsin')
                p300.aspirate(300, trypsin.top(h_track['trypsin']))
                counter = 0
    if counter > 0:
        p300.blow_out(trypsin)
    p300.drop_tip()

    # incubate T minutes
    p300.delay(minutes=T)

    # dispense 120ul media to specified wells
    p300.pick_up_tip()
    counter = 0
    height_tracker(240, 'media')
    p300.aspirate(240, media)
    for switch, well in zip(X, all_source):
        if switch == 1:
            p300.dispense(120, well.top(2))
            counter += 1
            if counter == 2:
                p300.blow_out(media.top())
                height_tracker(240, 'media')
                p300.aspirate(240, media.top(h_track['media']))
                counter = 0
    if counter > 0:
        p300.blow_out(media)
    p300.drop_tip()

    if P == 'yes':
        for switch, vol, well in zip(X, Z, all_source):
            if switch == 1 and vol > 0:
                p300.pick_up_tip()
                p300.mix(15, 100, well)
                p300.transfer(vol, well, liquid_trash, new_tip='never')
                p300.drop_tip()

        p300.pick_up_tip()
        for switch, vol, well in zip(X, Y, all_source):
            if switch == 1 and vol > 0:
                height_tracker(vol, 'media')
                p300.transfer(vol,
                              media.top(h_track['media']),
                              well.top(2),
                              new_tip='never')
        p300.drop_tip()

    else:
        counter = 0
        p300.pick_up_tip()
        for switch, vol in zip(X, Y):
            if switch == 1:
                if vol > 0:
                    height_tracker(vol, 'media')
                    dest = all_dest[counter]
                    p300.transfer(vol,
                                  media.top(h_track['media']),
                                  dest.top(2),
                                  new_tip='never')
                counter += 1
        p300.drop_tip()

        # initialize list for Z positions that will be printed to a file
        Z_temp = []
        counter = 0
        for switch, vol, source in zip(X, Z, all_source):
            if switch == 1:
                if vol <= 50:
                    pipette = p50
                    mix_vol = 50
                else:
                    pipette = p300
                    mix_vol = 100
                pipette.pick_up_tip()
                pipette.mix(15, mix_vol, source)
                dest = all_dest[counter]
                pipette.transfer(vol, source, dest, new_tip='never')
                pipette.drop_tip()
                counter += 1
                # Z_temp.append(dest.get_name())
                Z_temp.append(vol)

        Z_positions = []
        list = []
        counter = 0
        for pos in Z_temp:
            if counter < 12:
                counter += 1
                list.append(pos)
            else:
                Z_positions.append(list)
                list = [pos]
                counter = 1
        if len(list) != 0:
            Z_positions.append(list)

        now = datetime.datetime.now()
        new_file_name = 'LIST_' + now.strftime("%Y-%m-%d") + '.csv'
        whole_dir = '/data/user_storage/' + new_file_name
        if not robot.is_simulating():
            with open(whole_dir, mode='w') as z_file:
                z_writer = csv.writer(z_file,
                                      delimiter=',',
                                      quotechar='"',
                                      quoting=csv.QUOTE_MINIMAL)
                for row in Z_positions:
                    z_writer.writerow(row)

        # prompt user to retrieve the written CSV from the robot
        robot.comment('Retrieve your file: ' + new_file_name)
