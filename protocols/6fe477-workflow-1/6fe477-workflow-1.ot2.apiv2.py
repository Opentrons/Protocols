import math

metadata = {
    'protocolName': 'Nucleic Acid Purification - Workflow 1',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol):

    # [total_samples, p20_mount, p1000_mount] = get_values(  # noqa: F821
    #     "total_samples", "p20_mount", "p1000_mount")

    # USER VARIABLES (pipette mounts, deep well plates, aspiration/dispensing speeds, sample pool size, total sample number)

    # Load Tip Racks
    tiprack_200ul_filter = protocol.load_labware('opentrons_96_filtertiprack_200ul', 1)
    tiprack_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', 2)

    # Load Pipettes
    p300_single = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack_200ul_filter])
    p300_multi = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_300ul])

    # Deep Well Plate (DWP)
    deepwell_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', 3) # Replace with 2 custom deep well plates

    # Lysis Buffer Reservoir
    buffer_reservoir = protocol.load_labware('nest_1_reservoir_195ml', 4)['A1']

    # Load 7 Tube Racks with Samples in 30 mL Tubes
    for slot in range(1,12):
        if not slot in protocol.loaded_labwares:
            protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', slot)
    
    pool_size = 5 # USER
    # total_samples = 12 # USER
    all_wells = [protocol.loaded_labwares[i].wells()[j] for i in range(5,12) for j in range(6)]
    sample_wells = [all_wells[i:i + pool_size] for i in range(0, len(all_wells), pool_size)]
    dest_wells = deepwell_plate.wells()[0:len(sample_wells)]

    # Transfer 40 uL samples into DWP
    protocol.comment(f'Adding 40 uL samples with a pool size of {pool_size}')
    for i in range(len(sample_wells)):
        p300_single.transfer(40, sample_wells[i], dest_wells[i], new_tip='always')

    # Transfer 240 uL of Lysis Buffer into variable wells using multichannel pipette
    buffer_wells = len(dest_wells)
    columns = math.floor(buffer_wells / 8)
    left_over_wells = buffer_wells % 8
    protocol.comment('Transferring 240 uL of Lysis buffer into DWP')
    for i in range(columns):
        p300_multi.pick_up_tip(tiprack_300ul.columns()[i][0])
        p300_multi.transfer(240, buffer_reservoir, deepwell_plate.columns()[i][0], new_tip='never')
        p300_multi.drop_tip()
    if left_over_wells > 0:
        p300_multi.pick_up_tip(tiprack_300ul.columns()[columns][8-left_over_wells])
        p300_multi.transfer(240, buffer_reservoir, deepwell_plate.columns()[columns][0], new_tip='never')
        p300_multi.drop_tip()
