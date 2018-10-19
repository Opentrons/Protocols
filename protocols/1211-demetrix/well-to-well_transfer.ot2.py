
from opentrons import labware, instruments, robot
from otcustomizers import FileInput

labware_csv_example = """
Slot,Plate Type,Well Height
1,384-pcr,15
2,96-echo,30
3,trough-12row,
4,96-flat,
5,384-plate,
"""

transfer_csv_example = """
Source Slot,Source Well,Dest Slot,Dest Well,Volume
1,A1,4,A11,1
2,B1,5,A5,3
3,A12,5,H12,7
"""


def load_labware(csv_string):
    container_info = [cell for line in csv_string.splitlines() if line
                      for cell in [line.split(',')]]
    containers = {}
    for line in container_info[1:]:
        if line[1] not in labware.list():
            if '96' in line[1]:
                labware.create(
                    line[1],
                    grid=(12, 8),
                    spacing=(9, 9),
                    diameter=4.2,
                    depth=round(float(line[2])))
            elif '384' in line[1]:
                labware.create(
                    line[1],
                    grid=(24, 16),
                    spacing=(4.5, 4.5),
                    diameter=3.1,
                    depth=round(float(line[2])))
        containers[line[0]] = labware.load(line[1], line[0])
    return containers


def update_tip_count(tip_count, tip_limit, pipette):
    tip_count += 1
    if tip_count == tip_limit:
        robot.pause("You have run out of tips. Resume after tipracks are \
        replaced.")
        pipette.reset_tip_tracking()
        tip_count = 0
    return tip_count


def run_custom_protocol(
        labware_csv: FileInput=labware_csv_example,
        transfer_csv: FileInput=transfer_csv_example):

    containers = load_labware(labware_csv)
    # print(containers)
    tipracks = [labware.load('tiprack-10ul', str(slot+1))
                for slot in range(len(containers), 11)]

    tip_limit = 96 * len(tipracks)
    tip_count = 0

    p10 = instruments.P10_Single(
        mount='left',
        tip_racks=tipracks)

    transfer_info = [cell for line in transfer_csv.splitlines() if line
                     for cell in [line.split(',')]]

    for line in transfer_info[1:]:
        vol = float(line[4])
        source = containers[line[0]].wells(line[1])
        dest = containers[line[2]].wells(line[3])
        tip_count = update_tip_count(tip_count, tip_limit, p10)
        p10.transfer(vol, source, dest, blow_out=True)
