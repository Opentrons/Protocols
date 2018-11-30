from opentrons import labware, instruments
from otcustomizers import StringSelection

# labware setup
plate = labware.load('96-flat', '2')
trough = labware.load('trough-12row', '1')

tiprack_10 = labware.load('tiprack-10ul', '4')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

# reagent setup
cells = trough.wells('A1')

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])

layout = """
,,1,1,1,2,2,2,3,3,3,1
4,4,4,5,5,5,6,6,6,7,7,7
8,8,8,9,9,9,10,10,10,1,1,1
1,1,1,11,11,11,12,12,12,13,13,13
2,2,2,3,3,3,4,4,4,5,5,5
6,6,6,7,7,7,1,1,1,8,8,8
9,9,9,10,10,10,11,11,11,12,12,12
13,13,13,14,14,14,15,15,15,1,1,1
"""


def run_custom_protocol(
    tube_rack_type: StringSelection(
        "opentrons-tuberack-2ml-eppendorf",
        "opentrons-tuberack-2ml-screwcap")="opentrons-tuberack-2ml-eppendorf"):

    tuberack = labware.load(tube_rack_type, '3')

    # transfer medium
    m300.pick_up_tip(tiprack_300.wells('B1'))  # pick up 7 tips
    for col_num in range(2):
        m300.mix(5, 300, cells)
        m300.transfer(190, cells, plate.cols(col_num)[1], new_tip='never')
    m300.return_tip()

    m300.pick_up_tip()
    for col_num in range(2, 12):
        m300.mix(5, 300, cells)
        m300.transfer(190, cells, plate.cols(col_num), new_tip='never')
    m300.drop_tip()

    # transfer sample
    layout_list = [cell for line in layout.splitlines() if line
                   for cell in line.split(',')]
    master_list = [[] for _ in range(15)]
    for index, cell in enumerate(layout_list):
        if cell:
            master_list[int(cell)-1].append(index)

    well_loc = [well for row in plate.rows() for well in row]
    tubes = [well for row in tuberack.rows() for well in row]

    # using same tip for tube 1-4
    p10.pick_up_tip()
    for tube_num in range(4):
        for dest in master_list[tube_num]:
            p10.mix(3, 10, tubes[tube_num])
            p10.transfer(
                10, tubes[tube_num], well_loc[dest], new_tip='never')
    p10.drop_tip()

    # using same tip for tube 5-7
    p10.pick_up_tip()
    for tube_num in range(4, 7):
        for dest in master_list[tube_num]:
            p10.mix(3, 10, tubes[tube_num])
            p10.transfer(
                10, tubes[tube_num], well_loc[dest], new_tip='never')
    p10.drop_tip()

    # using same tip for tube 8-10
    p10.pick_up_tip()
    for tube_num in range(7, 10):
        for dest in master_list[tube_num]:
            p10.mix(3, 10, tubes[tube_num])
            p10.transfer(
                10, tubes[tube_num], well_loc[dest], new_tip='never')
    p10.drop_tip()

    # using same tip for tube 11-13
    p10.pick_up_tip()
    for tube_num in range(10, 13):
        for dest in master_list[tube_num]:
            p10.mix(3, 10, tubes[tube_num])
            p10.transfer(
                10, tubes[tube_num], well_loc[dest], new_tip='never')
    p10.drop_tip()

    # using same tip for tube 14-15
    p10.pick_up_tip()
    for tube_num in range(13, 15):
        print(tube_num)
        for dest in master_list[tube_num]:
            p10.mix(3, 10, tubes[tube_num])
            p10.transfer(
                10, tubes[tube_num], well_loc[dest], new_tip='never')
    p10.drop_tip()
