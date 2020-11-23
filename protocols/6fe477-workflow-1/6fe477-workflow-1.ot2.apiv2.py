metadata = {
    'protocolName': 'Nucleic Acid Purification - Workflow 1',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol):

    # [total_samples, p20_mount, p1000_mount] = get_values(  # noqa: F821
    #     "total_samples", "p20_mount", "p1000_mount")

    # USER VARIABLES (pipette mounts, deep well plates, aspiration/dispensing speeds)

    tiprack_200ul_filter = protocol.load_labware('opentrons_96_filtertiprack_200ul', 1)
    tiprack_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', 2)

    p300_single = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack_200ul_filter])
    p300_multi = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_300ul])

    print(protocol.loaded_labwares)

# Custom Labware Description (if applicable): 
# 1.5 mL tubes (cat. no. 16466-058 VWR)
# Caplugs (cat. no. 2223530G80) 30 mL tubes
# NEST 96 DWP 2mL (cat. no. 503162)
# Thermofisher Nunc 96-well deep well plate (cat. no. 278743)
# NEST 1 well Reservoir 195 mL (cat. no. 360103)
