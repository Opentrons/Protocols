from opentrons import labware, instruments, robot
from otcustomizers import FileInput

metadata = {
    'protocolName': 'CSV Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# custom labware
plate_name = 'qPCR-384-tuberack'
if plate_name not in labware.list():
    labware.create(plate_name,
                   grid=(24, 16),
                   spacing=(4.5, 4.5),
                   depth=16.1,
                   diameter=4,
                   volume=100)

# labware
tips = labware.load('tiprack-10ul', '1')
tubes = labware.load('opentrons-aluminum-block-2ml-eppendorf', '2')
qPCR_rack = labware.load(plate_name, '3')

# pipettes
p10 = instruments.P10_Single(
    mount='right',
    tip_racks=[tips]
)

example_csv = """,Knockdown,Primer
1,KD1,KD1
2,KD1,KD1
3,KD1,KD1
4,KD1,GAPDH
5,KD1,GAPDH
6,KD1,GAPDH
7,KD2,KD2
8,KD2,KD2
9,KD2,KD2
10,KD2,GAPDH
11,KD2,GAPDH
12,KD2,GAPDH
13,KD3,KD3
14,KD3,KD3
15,KD3,KD3
16,KD3,GAPDH
17,KD3,GAPDH
18,KD3,GAPDH
19,Ctrl,KD1
20,Ctrl,KD1
21,Ctrl,KD1
22,Ctrl,KD2
23,Ctrl,KD2
24,Ctrl,KD2
25,Ctrl,KD3
26,Ctrl,KD3
27,Ctrl,KD3
28,Ctrl,GAPDH
29,Ctrl,GAPDH
30,Ctrl,GAPDH
31,H2O,KD1
32,H2O,KD2
33,H2O,KD3
34,H2O,GAPDH
35,,
36,,
37,,
"""

cDNA_tubes = {'kd1': tubes.wells('A1'),
              'kd2': tubes.wells('B1'),
              'kd3': tubes.wells('C1'),
              'ctrl': tubes.wells('D1'),
              'h2o': tubes.wells('A2')}

MM_tubes = {'kd1': tubes.wells('B2'),
            'kd2': tubes.wells('C2'),
            'kd3': tubes.wells('D2'),
            'gapdh': tubes.wells('A3')}


def run_custom_protocol(CSV_file: FileInput = example_csv):

    knockdowns = []
    primers = []

    def csv_parser(file_string):
        nonlocal knockdowns
        nonlocal primers

        # remove header column
        rows = file_string.splitlines()[1:]
        for row in rows:
            # check if empty line
            vals = row.split(',')
            if len(vals[1]) > 0:
                knockdowns.append(vals[1].lower())
                primers.append(vals[2].lower())

    csv_parser(CSV_file)

    # transfer primers
    for primer, dest in zip(primers, qPCR_rack.wells()):
        source = MM_tubes[primer]
        p10.pick_up_tip()
        p10.transfer(9, source, dest, new_tip='never')
        p10.blow_out(dest.top())
        p10.touch_tip(dest)
        p10.drop_tip()

    # transfer knockdowns
    for kd, dest in zip(knockdowns, qPCR_rack.wells()):
        source = cDNA_tubes[kd]
        p10.pick_up_tip()
        p10.transfer(1, source, dest, new_tip='never')
        p10.blow_out(dest.top())
        p10.touch_tip(dest)
        p10.drop_tip()
