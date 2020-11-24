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
    buffer_reservoir = protocol.load_labware('nest_1_reservoir_195ml', 4)

    # Load 7 Tube Racks with Samples in 30 mL Tubes
    for slot in range(1,12):
        if not slot in protocol.loaded_labwares:
            protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', slot)
    
    pool_size = 5
    all_wells = [protocol.loaded_labwares[i].wells()[j] for i in range(5,12) for j in range(6)]
    sample_wells = [all_wells[i:i + pool_size] for i in range(0, len(all_wells), pool_size)]
    dest_wells = deepwell_plate.wells()[0:len(sample_wells)]

    # for i in range(len(sample_wells)):
    #     p300_single.transfer(40, sample_wells[i], dest_wells[i], new_tip='always')

    # print(deepwell_plate.wells()[0:len(dest_wells)])

    columns = (len(dest_wells) - (len(dest_wells) % 8)) / 8
    print(int(columns))

# Custom Labware Description (if applicable): 
# 1.5 mL tubes (cat. no. 16466-058 VWR)
# Caplugs (cat. no. 2223530G80) 30 mL tubes
# NEST 96 DWP 2mL (cat. no. 503162) (SAME AS BELOW?)(https://www.fishersci.com/shop/products/nunc-1-3-2-0ml-deepwell-plates-shared-wall-technology/12565606?searchHijack=true&searchTerm=12565606&searchType=RAPID&crossRef=max9620&matchedCatNo=12565606)
# Thermofisher Nunc 96-well deep well plate (cat. no. 278743) (https://assets.thermofisher.com/TFS-Assets/LSG/manuals/D03027.pdf)
# NEST 1 well Reservoir 195 mL (cat. no. 360103)