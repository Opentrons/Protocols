from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': 'DNA Normalization and Pooling from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
buffer = labware.load('usascientific_12_reservoir_22ml', '1').wells()[0]
dest_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '2', 'destination plate')
source_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '3', 'source plate')
tipracks10 = [
    labware.load('opentrons_96_tiprack_10ul', slot, '10ul tiprack')
    for slot in ['4', '5']
]
pool = labware.load(
    'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
    '6',
    'pool tube rack').wells()[0]

example_csv = """source well,destination well,vol sample (ul),vol buffer (ul),\
pool vol (ul, 0 if no pooling)
A1,A1,5,5,8
C1,B1,2,8,4
"""


def run_custom_protocol(
        p10_mount: StringSelection('right', 'left') = 'right',
        input_csv: FileInput = example_csv
):
    # pipette
    p10 = instruments.P10_Single(mount=p10_mount, tip_racks=tipracks10)

    # parse
    trans_data = [
        [val.strip() for val in line.split(',')]
        for line in input_csv.splitlines()[1:] if line
    ]

    # cherrypick and normalize
    for line in trans_data:
        s, d, v_sample, v_buffer, v_pool = [
            source_plate.wells(line[0]), dest_plate.wells(line[1]),
            float(line[2]), float(line[3]), float(line[4])
        ]
        if v_sample + v_buffer > 10:
            p50_mount = 'left' if p10_mount == 'right' else 'right'
            tipracks50 = [
                labware.load(
                    'opentrons_96_tiprack_300ul', slot, '300ul tiprack')
                for slot in ['7', '8']
            ]
            p50 = instruments.P50_Single(mount=p50_mount, tip_racks=tipracks50)
            pip = p50
        else:
            pip = p10

        # transfer sample
        pip.pick_up_tip()
        pip.aspirate(v_buffer, buffer)
        pip.aspirate(v_sample, s)
        pip.dispense(v_buffer + v_sample, d.bottom(2))
        pip.drop_tip()

    # pool
    for line in trans_data:
        s, d, v_sample, v_buffer, v_pool = [
            source_plate.wells(line[0]), dest_plate.wells(line[1]),
            float(line[2]), float(line[3]), float(line[4])
        ]
        if v_pool > 10:
            pip = p50
        else:
            pip = p10

        # transfer to pool
        pip.pick_up_tip()
        pip.transfer(v_pool, d, pool.bottom(5), new_tip='never')
        pip.blow_out()
        pip.drop_tip()
