# def get_values(*names):
#     import json
#     _all_values = json.loads("""{"vial_map":""}""")
#     return [_all_values[n] for n in names]

metadata = {
    'protocolName': 'CSV Input Reagent Dispensing',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol):

    # [p1000_tips, p300_tips, p1000_mount, p300_mount, reservoir_type, vial_map, htp_csv] = get_values(  # noqa: F821
    #     "total_samples", "p20_mount", "p1000_mount")

    vial_map = """Well Number,Labware,Slot,Well Position
1,opentrons_24_tuberack_nest_2ml_screwcap,4,A1
2,opentrons_24_tuberack_nest_2ml_screwcap,4,A2
3,opentrons_24_tuberack_nest_2ml_screwcap,4,A3"""

    htp_csv = """*Note numbering starts from top left to top right,Reservoir 1,Reservoir 2,Reservoir 3,Reservoir 4,Reservoir 5,Reservoir 6,Reservoir 7,Reservoir 8,Reservoir 9,Reservoir 10,Reservoir 11,Reservoir 12,
Well Number,Metal Salt Stock Soln 1 (1 M) (uL),Metal Salt Stock Soln 2 (1 M) (uL),Metal Salt Stock Soln 3 (1 M) (uL),Metal Salt Stock Soln 4 (1 M) (uL),Organic Linker Stock Soln 1 (1 M) (uL),Organic Linker Stock Soln 2 (1 M) (uL),Organic Linker Stock Soln 3 (1 M) (uL),Organic Linker Stock Soln 4 (1M) (uL),Extra Solvent 1 (uL),Extra Solvent 2 (uL),Extra Solvent 3 (uL),Extra Solvent 4 (uL),Total Volume (uL)
51,270,325,325,,150,,,,71,107,,,1248
52,270,375,375,,150,,,,78,117,,,1365
53,270,425,425,,150,,,,,,,,1270"""


    # Load Tip Racks
    p1000_tiprack = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 1)
    p300_tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 2)

    # Load Pipettes
    p1000 = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[p1000_tiprack])
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300_tiprack])

    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 3)

    # Load Reaction Vessel Labware
    vial_info = [[val.strip() for val in line.split(',')] for line in vial_map.splitlines()
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
        sample_tubes.append(protocol.loaded_labwares[int(slot)].wells_by_name()[well])


    # Parse High-Throughput CSV
    htp_info = [[val.strip().lower() for val in line.split(',')] for line in htp_csv.splitlines()
                    if line.split(',')[0].strip()][2:]

    # Get all dispense volumes in each row
    dispense_vols = [htp_info[i][1:13] for i in range(len(htp_info))]

    # Group dispense volumes per column (Each list contains volumes per reservoir)
    dispense_vols_serialized = [[vol[i] for vol in dispense_vols] for i in range(len(dispense_vols[0]))]

    # Dispenses volumes from each reservoir to corresponding wells
    # Note: empty columns result in tips being wasted. Fix?
    for res in range(len(dispense_vols_serialized)):
        p300.pick_up_tip()
        p1000.pick_up_tip()
        for vial, vol in zip(sample_tubes, dispense_vols_serialized[res]):
            if vol:
                if int(vol) < 300:
                    # print(f'P300: {vol} uL from {reservoir.wells()[res]} in {vial}')
                    p300.transfer(int(vol), reservoir.wells()[res], vial, new_tip='never')
                else:
                    # print(f'P1000: {vol} uL from {reservoir.wells()[res]} in {vial}')
                    p1000.transfer(int(vol), reservoir.wells()[res], vial, new_tip='never')
            else:
                continue
        p300.drop_tip()
        p1000.drop_tip()




# Pipette mounts
# Use drop down input to get tip rack names (Step 1)
# CSV for uploading custom reaction vessel racks with vials or well plates (Step 2)
# CSV for stock solution reservoirs (Step 3)
# Import CSV for High-Throughput Synthesis (Step 4)

# Example: 

# Choose pipette and pickup tip (if statement with volume)
# Reservoir 1: 270 uL in A1
# Reservoir 1: 27 uL in A2
# etc...