from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'CSV Tip Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

example_csv = """1# 5 lines of header where we store,,
# info for documentation.,,
#,,
#,,
#,,
SourceBox,SourcePos,RemoveTip(yes/no)
1,A1,1
1,A2,0
1,A3,0
1,A4,0
1,A5,0
1,A6,0
1,A7,1
1,A8,1
1,A9,1
"""


def run_custom_protocol(
        tip_cherrypick_CSV: FileInput = example_csv,
        mount_side: StringSelection('right', 'left') = 'right'
        ):

    # pipette
    p10 = instruments.P10_Single(mount=mount_side)

    # pop top 6 lines of CSV that do not contain transfer info
    transfer_info = [line.split(',')
                     for line in tip_cherrypick_CSV.splitlines() if line]
    for _ in range(6):
        transfer_info.pop(0)

    # determine number of tip racks, including new racks
    num_start_racks = max([int(line[0]) for line in transfer_info])
    count = sum([int(line[2]) for line in transfer_info])
    num_fresh_racks = (count // 96) + 1

    start_racks = [labware.load('tiprack-10ul', str(slot), 'filled')
                   for slot in range(1, num_start_racks + 1)]
    fresh_racks = [labware.load('tiprack-10ul', str(slot), 'fresh')
                   for slot in range(num_start_racks + 1,
                                     num_start_racks + 1 + num_fresh_racks)]
    tip_dests = [well for rack in fresh_racks for well in rack]

    # perform necessary tip transfers
    tip_counter = 0
    for row in transfer_info:
        # parse row info
        rack_ind = int(row[0]) - 1
        pos = row[1]
        switch = int(row[2])

        if switch == 1:
            rack = start_racks[rack_ind]
            p10.pick_up_tip(rack.wells(pos))
            p10.drop_tip(tip_dests[tip_counter])
            tip_counter += 1
