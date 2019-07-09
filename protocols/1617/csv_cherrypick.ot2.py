from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'CSV Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

example_csv = """source deck,Source well,volume,Destination deck,Destination \
well,mixing volume,mixing cycle
4,A1,20,1,A1,20, 1
5,D7,40,1,D12,40, 2
6,F12,70,2,G8,10, 3
"""


def run_custom_protocol(
        transfer_cherrypick_CSV: FileInput = example_csv,
        source_plate_type: StringSelection(
            'Bio-Rad Hardshell 96-well plate',
            'Opentrons 4x6 tube rack') = 'Bio-Rad Hardshell 96-well plate',
        destination_plate_type: StringSelection(
            'Bio-Rad Hardshell 96-well plate',
            'Opentrons 4x6 tube rack') = 'Bio-Rad Hardshell 96-well plate',
        pipette_selection: StringSelection('P10 and P50', 'P50 and P300',
                                           'P10 and P300') = 'P50 and P300',
):

    if source_plate_type == 'Bio-Rad Hardshell 96-well plate':
        source_name = 'biorad-hardshell-96-PCR'
    else:
        source_name = 'opentrons-tuberack-2ml-eppendorf'

    if destination_plate_type == 'Bio-Rad Hardshell 96-well plate':
        dest_name = 'biorad-hardshell-96-PCR'
    else:
        dest_name = 'opentrons-tuberack-2ml-eppendorf'

    # pop top 6 lines of CSV that do not contain transfer info
    transfer_info = [line.split(',')
                     for line in transfer_cherrypick_CSV.splitlines() if line]
    transfer_info.pop(0)
    source_plate_slots = []
    source_wells = []
    target_plate_slots = []
    target_wells = []
    volumes = []
    mix_vols = []
    mix_cycles = []

    # parse for transfer information
    for line in transfer_info:
        source_plate_slots.append(line[0].strip())
        source_wells.append(line[1].strip())
        volumes.append(float(line[2].strip()))
        target_plate_slots.append(line[3].strip())
        target_wells.append(line[4].strip())
        mix_vols.append(float(line[5].strip()))
        mix_cycles.append(int(line[6].strip()))

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
    source_plates = [labware.load(source_name, key, 'source ' + key)
                     for key in unique_source_slots]
    destination_plates = [labware.load(dest_name, key, 'destination ' + key)
                          for key in unique_target_slots]

    # pipette and tiprack setup depending on pipette selection
    if pipette_selection.split(' ')[0] == 'P10':
        tips10 = [labware.load('tiprack-10ul', slot) for slot in ['10', '11']]
        tips300 = [labware.load('opentrons-tiprack-300ul', slot)
                   for slot in ['7', '8', '9']]
        tips10_max = 96*2
        tips300_max = 96*3
        all_tips_10 = [well for rack in tips10 for well in rack.wells()]
        p10 = instruments.P10_Single(mount='right')
        if pipette_selection.split(' ')[2] == 'P50':
            p50 = instruments.P50_Single(mount='left')
        else:
            p300 = instruments.P300_Single(mount='left')
        tip10_count = 0
    else:
        tips300 = [labware.load('opentrons-tiprack-300ul', slot)
                   for slot in ['7', '8', '9', '10', '11']]
        tips300_max = 96*5
        p50 = instruments.P50_Single(mount='right')
        p300 = instruments.P300_Single(mount='left')
    all_tips_300 = [well for rack in tips300 for well in rack.wells()]
    tip300_count = 0

    # perform transfers
    for s_slot, s_well, t_slot, t_well, vol, mix_vol, mix_n in zip(
            source_plate_slots,
            source_wells,
            target_plate_slots,
            target_wells,
            volumes,
            mix_vols,
            mix_cycles):

        if pipette_selection.split(' ')[0] == 'P10':
            if tip10_count == tips10_max:
                robot.pause('Replace tipracks before resuming.')
                p10.reset()
                tip10_count = 0
        if tip300_count == tips300_max:
            robot.pause('Replace tipracks before resuming.')
            p50.reset()
            p300.reset()
            tip300_count = 0

        if vol > 0:
            s_plate_ind = unique_source_slots[s_slot]
            s_plate = source_plates[s_plate_ind]
            t_plate_ind = unique_target_slots[t_slot]
            t_plate = destination_plates[t_plate_ind]

            source = s_plate.wells(s_well)
            target = t_plate.wells(t_well)

            if pipette_selection == 'P10 and P50':
                if vol <= 10:
                    pipette = p10
                    tip10_count += 1
                    pipette.pick_up_tip(all_tips_10[tip10_count])
                else:
                    pipette = p50
                    tip300_count += 1
                    pipette.pick_up_tip(all_tips_300[tip300_count])
            elif pipette_selection == 'P10 and P300':
                if vol <= 30:
                    pipette = p10
                    tip10_count += 1
                    pipette.pick_up_tip(all_tips_10[tip10_count])
                else:
                    pipette = p300
                    tip300_count += 1
                    pipette.pick_up_tip(all_tips_300[tip300_count])
            else:
                if vol <= 50:
                    pipette = p50
                else:
                    pipette = p300
                tip300_count += 1
                pipette.pick_up_tip(all_tips_300[tip300_count])

            pipette.transfer(
                vol,
                source,
                target,
                blow_out=True,
                new_tip='never'
                )
            pipette.mix(mix_n, mix_vol)
            pipette.blow_out(target.top())
            pipette.drop_tip()
