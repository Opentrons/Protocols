metadata = {
    'protocolName': 'High-Throughput Synthesis',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(protocol):

    [p1000_tips, p300_tips, p1000_mount, p300_mount, reservoir_type,
     vial_map, htp_csv] = get_values(  # noqa: F821
        "p1000_tips", "p300_tips", "p1000_mount", "p300_mount",
        "reservoir_type", "vial_map", "htp_csv")

    # Load Tip Racks
    p1000_tiprack = protocol.load_labware(p1000_tips, 1)
    p300_tiprack = protocol.load_labware(p300_tips, 2)

    # Load Pipettes
    p1000 = protocol.load_instrument('p1000_single_gen2',
                                     p1000_mount, tip_racks=[p1000_tiprack])
    p300 = protocol.load_instrument('p300_single_gen2',
                                    p300_mount, tip_racks=[p300_tiprack])

    reservoir = protocol.load_labware(reservoir_type, 3)

    # Load Reaction Vessel Labware
    vial_info = [[val.strip() for val in line.split(',')]
                 for line in vial_map.splitlines()
                 if line.split(',')[0].strip()][1:]

    for line in vial_info:
        s_lw, s_slot = line[1:3]
        for slot, lw in zip([s_slot], [s_lw]):
            if int(slot) not in protocol.loaded_labwares:
                protocol.load_labware(lw.lower(), slot)

    # Get all sample reaction vials
    sample_tubes = []
    for line in vial_info:
        lw, slot, well = line[1:4]
        sample_tubes.append(protocol.loaded_labwares[
                            int(slot)].wells_by_name()[well])

    # Parse High-Throughput CSV
    htp_info = [[val.strip().lower() for val in line.split(',')]
                for line in htp_csv.splitlines()
                if line.split(',')[0].strip()][2:]

    # Get all dispense volumes in each row
    dispense_vols = [i[1:13] for i in htp_info]

    # Group dispense volumes per column
    # Each list contains volumes per reservoir
    dispense_vols_serialized = [[vol[i] for vol in
                                dispense_vols] for i in range(12)]

    # Creates data structure with correct reservoir,
    # wells, and corresponding volumes
    raw_samples_data = {i: {well: vol for well, vol in
                        enumerate(volumes) if vol != ''}
                        for i, volumes in enumerate(dispense_vols_serialized)}

    # Remove columns with empty values
    samples_data = {i: v for i, v in raw_samples_data.items() if v}

    for res in samples_data:
        for i, vol in enumerate(samples_data[res]):
            well, volume = i, int(samples_data[res][i])
            pip = p300 if volume < 300 else p1000
            if not pip.has_tip:
                pip.pick_up_tip()
            pip.transfer(volume, reservoir.wells()[res],
                         sample_tubes[well], new_tip='never')
        for pipette in [p300, p1000]:
            if pipette.has_tip:
                pipette.drop_tip()
