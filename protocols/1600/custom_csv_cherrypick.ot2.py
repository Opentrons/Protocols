from opentrons import labware, instruments, robot
from otcustomizers import FileInput
import math

metadata = {
    'protocolName': 'CSV Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

example_csv = """s slot,Source well,volume,d slot,Destination,volume
4,A1,20,9,A1,20
5,D7,40,9,D12,40
6,F12,70,9,G8,70
"""


def run_custom_protocol(transfer_cherrypick_CSV: FileInput = example_csv):

    # pop top 6 lines of CSV that do not contain transfer info
    transfer_info = [line.split(',')
                     for line in transfer_cherrypick_CSV.splitlines() if line]
    transfer_info.pop(0)
    source_plate_slots = []
    source_wells = []
    target_plate_slots = []
    target_wells = []
    volumes = []
    num_transfers = len(transfer_info)

    # parse for transfer information
    for line in transfer_info:
        source_plate_slots.append(line[0].strip())
        source_wells.append(line[1].strip())
        volumes.append(float(line[2].strip()))
        target_plate_slots.append(line[3].strip())
        target_wells.append(line[4].strip())

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
    source_plates = [labware.load('biorad-hardshell-96-PCR',
                     key, 'source ' + key) for key in unique_source_slots]
    destination_plates = [labware.load('biorad-hardshell-96-PCR',
                          key, 'destination ' + key)
                          for key in unique_target_slots]

    tip_slots = [str(slot) for slot in range(1, 12)]
    for key in unique_source_slots:
        tip_slots.remove(key)
    for key in unique_target_slots:
        tip_slots.remove(key)

    if num_transfers >= 96*len(tip_slots):
        tip_slots_needed = len(tip_slots)
    else:
        tip_slots_needed = math.ceil(num_transfers / 96)

    tip_slots = tip_slots[0:tip_slots_needed]
    tipracks = [labware.load('opentrons-tiprack-300ul', str(slot))
                for slot in tip_slots]
    tip_max = 96*tip_slots_needed
    tip_count = 0
    tips = [tip for rack in tipracks for tip in rack.wells()]

    # pipette with defined tipracks
    p50 = instruments.P50_Single(mount='right')
    p300 = instruments.P300_Single(mount='left')

    # perform transfers
    for s_slot, s_well, t_slot, t_well, vol in zip(source_plate_slots,
                                                   source_wells,
                                                   target_plate_slots,
                                                   target_wells,
                                                   volumes):
        if tip_count == tip_max:
            robot.pause('Replace tipracks before resuming.')
            p50.reset()
            p300.reset()

        if vol > 0:
            s_plate_ind = unique_source_slots[s_slot]
            s_plate = source_plates[s_plate_ind]
            t_plate_ind = unique_target_slots[t_slot]
            t_plate = destination_plates[t_plate_ind]

            source = s_plate.wells(s_well)
            target = t_plate.wells(t_well)

            # choose proper pipette for volume
            pipette = p50 if vol <= 50 else p300
            pipette.pick_up_tip(tips[tip_count])
            pipette.transfer(
                vol,
                source,
                target,
                blow_out=True,
                new_tip='never'
                )
            pipette.drop_tip()
            tip_count += 1
