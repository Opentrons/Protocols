metadata = {
    'protocolName': 'PCR/qPCR prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    # Load labware
    tipracks_20ul = []
    for slot in [7, 10, 11]:
        tipracks_20ul.append(ctx.load_labware('opentrons_96_tiprack_20ul', slot))
    
    tiprack_300ul = ctx.load_labware('opentrons_96_tiprack_300ul', 4)
    source_plate = ctx.load_labware('nest_12_reservoir_15ml', 1, 'Source Plate #1') # On top of ice tray

    temp_plates = []
    for i, slot in enumerate([8, 5, 2], 1):
        temp_plates.append(ctx.load_labware('thermofast_pcr_plate_96well_semiskirted', slot, f'Template Plate #{i}'))

    dest_plates = []
    for i, slot in enumerate([9, 6, 3], 1):
        dest_plates.append(ctx.load_labware('thermofast_pcr_plate_96well_semiskirted', slot, f'Destination Plate #{i}'))

    # Load pipettes
    m20 = ctx.load_instrument('p20_multi_gen2', 'left', tip_racks=tipracks_20ul)
    m300 = ctx.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_300ul])

    # Transfer 40 uL of master mix
    m300.pick_up_tip()
    for i in range(len(temp_plates)):
        m300.transfer(40, source_plate['A1'], temp_plates[i].rows()[0], new_tip='never')
    m300.drop_tip()

    # Transfer 10 uL of Template to Destination
    for i in range(len(temp_plates)):
        m20.transfer(10, temp_plates[i].rows()[0], dest_plates[i].rows()[0])