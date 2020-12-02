metadata = {
    'protocolName': 'CSV Input Reagent Dispensing',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol):

    # [p1000_tips, p300_tips, p1000_mount, p300_mount, reservoir_type] = get_values(  # noqa: F821
    #     "total_samples", "p20_mount", "p1000_mount")

    # Load Tip Racks
    p1000_tiprack = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 1)
    p300_tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 2)

    # Load Pipettes
    p1000 = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[p1000_tiprack])
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300_tiprack])

    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 3)
    reaction_plate = protocol.load_labware('nest_96_wellplate_2ml_deep', 6) # Temporary, might be multiple tube racks of 96 vials

    print(reservoir.wells()[0])


# P1000 GEN2
# P300 GEN2
# NEST 12-Well Reservoir 15 ml

# Pipette mounts
# Use text input to get tip rack names (Step 1)
# CSV for uploading custom reaction vessel racks with vials or well plates (Step 2)
# CSV for stock solution reservoirs (Step 3)
# Import CSV for High-Throughput Synthesis (Step 4)

# Example: 

# Choose pipette and pickup tip (if statement with volume)
# Reservoir 1: 270 uL in A1
# Reservoir 1: 27 uL in A2
# etc...