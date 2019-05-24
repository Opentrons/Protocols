from opentrons import labware, instruments, robot
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'CSV Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom plate
plate_name = 'Axygen-96-Vwell'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.4,
        depth=11.8,
        volume=480
    )

example_csv = """# 5 lines of header where we store,,,,
# info for documentation.,,,,
#,,,,
#,,,,
#,,,,
SourcePlate,SourceWell,TargetPlate,TargetWell,Volume (µl)
1,A1,2,A1,4
1,A2,2,A1,1
1,A3,2,A1,0
1,A4,2,A1,1
1,A5,2,A1,1
1,A6,2,A1,1
1,A7,2,A1,5
1,A8,2,A1,2
1,A9,2,A1,0
"""


def run_custom_protocol(
        transfer_cherrypick_CSV: FileInput = example_csv,
        mount_side: StringSelection('right', 'left') = 'right'
        ):

    # pop top 6 lines of CSV that do not contain transfer info
    transfer_info = [line.split(',')
                     for line in transfer_cherrypick_CSV.splitlines() if line]
    for _ in range(6):
        transfer_info.pop(0)
    source_plate_slots = []
    source_wells = []
    target_plate_slots = []
    target_wells = []
    volumes = []

    # parse for transfer information
    for line in transfer_info:
        source_plate_slots.append(line[0].strip())
        source_wells.append(line[1].strip())
        target_plate_slots.append(line[2].strip())
        target_wells.append(line[3].strip())
        volumes.append(float(line[4].strip()))

    unique_source_slots = {}
    source_plate_inds = 0
    for slot in source_plate_slots:
        if slot not in unique_source_slots:
            unique_source_slots.update({slot: source_plate_inds})
            source_plate_inds += 1

    unique_target_slots = {}
    target_plate_inds = 0
    for slot in target_plate_slots:
        if slot not in unique_target_slots:
            unique_target_slots.update({slot: target_plate_inds})
            target_plate_inds += 1

    # load proper labware
    source_plates = [labware.load(plate_name, key, 'source ' + key)
                     for key in unique_source_slots]
    target_plates = [labware.load(plate_name, key, 'target ' + key)
                     for key in unique_target_slots]
    num_tip_slots = 11 - (len(source_plates) + len(target_plates))
    tips10 = [labware.load('tiprack-10ul', str(slot))
              for slot in range(12-num_tip_slots, 12)]
    tip_max = 96*num_tip_slots
    tip_count = 0

    # pipette with defined tipracks
    p10 = instruments.P10_Single(mount=mount_side, tip_racks=tips10)

    # perform transfers
    for s_slot, s_well, t_slot, t_well, vol in zip(source_plate_slots,
                                                   source_wells,
                                                   target_plate_slots,
                                                   target_wells,
                                                   volumes):
        if tip_count == tip_max:
            robot.pause('Replace tipracks before resuming.')

        if vol > 0:
            s_plate_ind = unique_source_slots[s_slot]
            s_plate = source_plates[s_plate_ind]
            t_plate_ind = unique_target_slots[t_slot]
            t_plate = target_plates[t_plate_ind]

            source = s_plate.wells(s_well)
            target = t_plate.wells(t_well)
            p10.transfer(vol, source, target, blow_out=True)
            tip_count += 1
