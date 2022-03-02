input_file = """Number of Redo
28
pos TB_RCK_1,pos MTP_1,VolumeInPlate,VolumeFromTube
RPL220225NR,9094087_6_AAB_4_4_1
1,6,93,120
2,55,93,120
3,78,93,120
4,108,93,120
5,121,93,120
6,178,93,120
7,217,93,120
8,227,93,120
9,228,93,120
10,237,93,120
11,245,93,120
12,248,93,120
13,255,93,120
14,257,93,120
15,261,93,120
16,265,93,120
17,266,93,120
18,267,93,120
19,271,93,120
20,283,93,120
21,284,93,120
22,301,93,120
23,316,93,120
24,330,93,120
25,331,93,120
26,332,93,120
27,338,93,120
28,348,93,120
"""

input_file2 = ""

plate_scan = '9094087_6_AAB_4_4_1____'

plate_scan2 = ''

tuberack_scan = 'RPL220225NR____'

tuberack_scan2 = ''

default_disposal_vol = 200
default_transfer_vol = 200

import os
import json
import math

# metadata
metadata = {
    'protocolName': 'Redo Replacement Picking (Greiner Masterblock 384 Well \
Plate 225 µL)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    tip_track = True
    p300_mount = 'left'

    # load labware
    rack = ctx.load_labware('eurofins_96x2ml_tuberack', '2', 'tuberack')

    plates = [ctx.load_labware('greinermasterblock_384_wellplate_225ul', '4')]

    if input_file2:
        plates.append(
         ctx.load_labware('greinermasterblock_384_wellplate_225ul', '1'))

    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['11']]

    # pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tips300)

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}

    folder_path = '/data/tip_track'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def _pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log[pip]['tips'][tip_log[pip]['count']])
            tip_log[pip]['count'] += 1

    # check barcode scans (tube, plate)
    tuberack_bar, plate_bar = input_file.splitlines()[3].split(',')[:2]
    if not tuberack_scan[:len(tuberack_scan)-4] == tuberack_bar.strip():
        print(tuberack_scan[:len(tuberack_scan)-4])
        raise Exception(f'Tuberack scans do not match ({tuberack_bar}, \
{tuberack_scan})')
    if not plate_scan[:len(plate_scan)-4] == plate_bar.strip():
        raise Exception(f'Plate scans do not match ({plate_bar}, {plate_bar})')

    if input_file2:
        tuberack_bar2, plate_bar2 = input_file2.splitlines()[3].split(',')[:2]
        if not tuberack_scan2[:len(tuberack_scan2)-4] == tuberack_bar2.strip():
            print(tuberack_scan2[:len(tuberack_scan2)-4])
            raise Exception(f'Tuberack2 scans do not match ({tuberack_bar2}, \
    {tuberack_scan2})')
        if not plate_scan2[:len(plate_scan2)-4] == plate_bar2.strip():
            raise Exception(
             f'Plate2 scans do not match ({plate_bar2}, {plate_bar2})')

    # parse
    inputdata = [[
        [val.strip() for val in line.split(',')]
        for line in input_file.splitlines()[4:]
        if line and line.split(',')[0].strip()]]

    tubelist = [[
        well for col in rack.columns()
        for well in col[:8]]]

    if input_file2:

        inputdata.append([
            [val.strip() for val in line.split(',')]
            for line in input_file2.splitlines()[4:]
            if line and line.split(',')[0].strip()])

        tubelist.append([
            well for col in rack.columns()
            for well in col[8:]])

    for data, plate, tubes_ordered in zip(inputdata, plates, tubelist):
        for line in data:
            tube = tubes_ordered[int(line[0])-1]
            well = plate.wells()[int(line[1])-1]
            if len(line) >= 3 and line[2]:
                disposal_vol = float(line[2])
            else:
                disposal_vol = default_disposal_vol
            if len(line) >= 4 and line[3]:
                transfer_vol = float(line[3])
            else:
                transfer_vol = default_transfer_vol

            # remove contents of well
            _pick_up(p300)

            ctx.max_speeds['A'] = 100  # slow descent
            ctx.max_speeds['Z'] = 100  # slow descent

            # effective tip capacity 280 with 20 uL air gap
            reps = math.ceil(disposal_vol / 280)

            vol = disposal_vol / reps

            for rep in range(reps):
                p300.move_to(well.top())
                p300.air_gap(20)
                p300.aspirate(vol, well.bottom(1))
                p300.dispense(
                 vol+20, ctx.fixed_trash.wells()[0].top(-5), rate=1.5)
                ctx.delay(seconds=1)

            # to improve completeness of removal
            for clearance in [0.7, 0.4, 0.2, 0]:
                p300.aspirate(20, well.bottom(clearance))

            del ctx.max_speeds['A']  # reset to default
            del ctx.max_speeds['Z']  # reset to default

            p300.drop_tip()

            # transfer tube to well
            _pick_up(p300)

            # effective tip capacity 280 with 20 uL air gap
            reps = math.ceil(transfer_vol / 280)

            vol = transfer_vol / reps

            for rep in range(reps):
                p300.move_to(tube.top())
                p300.air_gap(20)
                p300.aspirate(vol, tube.bottom(0.2))
                p300.dispense(vol+20, well.top(-2), rate=1.5)
                ctx.delay(seconds=1)

            p300.drop_tip()

    # track final used tip
    if not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
