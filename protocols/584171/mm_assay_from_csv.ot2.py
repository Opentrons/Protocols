from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': 'PCR Mastermix Assay from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
tuberack = labware.load(
    'opentrons_15_tuberack_falcon_15ml_conical', '1', 'PCR assay mix tubes')

example_csv = """Source,Destination Well,Transfer Amount,# of Tranfers,
tube 1,A3,240 ul,2,
tube 1,B3,240 ul,2,
tube 1,G9,240 ul,2,
tube 1,H9,240 ul,2,
tube 2,A4,240 ul,2,
tube 2,B4,240 ul,2,
tube 2,G8,240 ul,2,
tube 2,H8,240 ul,2,
tube 2,C6,240 ul,2,
tube 2,D6,240 ul,2,
tube 3,A5,240 ul,2,
tube 3,B5,240 ul,2,
tube 3,G7,240 ul,2,
tube 3,H7,240 ul,2,
tube 3,C7,240 ul,2,
tube 3,D7,240 ul,2,
tube 4,A6,240 ul,2,
tube 4,B6,240 ul,2,
tube 4,G6,240 ul,2,
tube 4,H6,240 ul,2,
tube 4,C8,240 ul,2,
tube 4,D8,240 ul,2,
tube 5,A7,240 ul,2,
"""


def run_custom_protocol(
        p1000_mount: StringSelection('right', 'left') = 'right',
        input_csv_file: FileInput = example_csv,
        number_of_target_plates: int = 3
):
    # load destination plates
    plate = labware.load(
        'usascientific_96_wellplate_2.4ml_deep', '2', 'assay plate')
    max_racks = math.ceil(15*number_of_target_plates/96)
    tips = [
        labware.load('opentrons_96_tiprack_1000ul', str(slot))
        for slot in range(3, 3+max_racks)
    ]

    # pipette
    p1000 = instruments.P1000_Single(mount=p1000_mount, tip_racks=tips)

    # parse
    trans_data = [
        [val.strip() for val in line.split(',')]
        for line in input_csv_file.splitlines()[1:]
        if line and line.split(',')[0]
    ]
    sources = [
        tuberack.wells()[int(tube.split('tube')[-1])-1]
        for tube in [line[0] for line in trans_data]
    ]
    dests = [plate.wells(line[1].upper()) for line in trans_data]
    vols = [float(line[2].split('ul')[0]) for line in trans_data]
    num_trans = [int(line[3]) for line in trans_data]

    for n in range(number_of_target_plates):
        p1000.pick_up_tip()
        s_prev = sources[0]
        for v, s, d, t in zip(vols, sources, dests, num_trans):
            if s != s_prev:
                s_prev = s
                p1000.drop_tip()
                p1000.pick_up_tip()
            for _ in range(t):
                p1000.aspirate(v, s.bottom(5))
                p1000.aspirate(50, s.top(5))
                p1000.dispense(v+50, d.top(-2))
                p1000.blow_out(d.top(-2))
            p1000.mix(3, v, d.bottom(5))
            p1000.blow_out(d.top(-2))
        p1000.drop_tip()
        if n < number_of_target_plates - 1:
            robot.pause('Replace the assay plate in slot 2 with the next plate \
and refill source tubes if necessary before resuming.')
        else:
            robot.comment('Protocol fully executed.')
