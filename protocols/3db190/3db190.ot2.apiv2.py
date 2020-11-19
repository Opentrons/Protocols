from opentrons import protocol_api

def get_values(*names):
    import json
    _all_values = json.loads("""{"total_samples":"10","p20_mount":"left","p1000_mount":"right"}""")
    return [_all_values[n] for n in names]

metadata = {
    'protocolName': 'PCR/qPCR prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.7'
}

def run(protocol):

    [total_samples, p20_mount, p1000_mount] = get_values(  # noqa: F821
    "total_samples", "p20_mount", "p1000_mount")

    total_samples = int(total_samples)

    # Load Tip Racks
    tiprack1 = protocol.load_labware('opentrons_96_tiprack_20ul', 5)
    tiprack2 = protocol.load_labware('opentrons_96_tiprack_20ul', 8)
    tiprack3 = protocol.load_labware('opentrons_96_tiprack_1000ul', 4)
    tiprack4 = protocol.load_labware('opentrons_96_tiprack_1000ul', 7)

    # Load Plates
    multiwell_plate = protocol.load_labware('eppendorf_96_deepwell_1000ul', '2')  # 1 mL Deepwell Microtiter Plate
    pcr_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 3)   # PCR Plate

    # Load Instruments
    P20_single = protocol.load_instrument('p20_single_gen2', p20_mount, tip_racks=[tiprack1, tiprack2])
    P1000_single = protocol.load_instrument('p1000_single_gen2', p1000_mount, tip_racks=[tiprack3, tiprack4])

    # Reagents
    reagents = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 1) # Proccess Buffer (A1), Master Mix (B1)

    ### Protocol Steps ###

    # Add 400 uL of Process Buffer to Required Wells in Deep Well Block (Uses one tip)
    protocol.comment(f'Adding 400 uL of process buffer sequentially to {total_samples} wells...')
    P1000_single.pick_up_tip()
    for well in range(total_samples):
        P1000_single.transfer(400, reagents.wells_by_name()['A1'], multiwell_plate.wells()[well], new_tip='never')
    P1000_single.drop_tip()

    ## PAUSE PROTOCOL ###
    protocol.pause('Pausing protocol for further specimen processing. Please prepare for the RT-PCR-Setup Procedure and click Resume when ready...')

    # Add 15 uL of Master Mix to the Deep Well Block
    protocol.comment(f'Adding 15 uL of Master Mix to {total_samples} wells on the PCR Plate...')
    P20_single.pick_up_tip()
    for well in range(total_samples):
        P20_single.transfer(15, reagents.wells_by_name()['B1'], pcr_plate.wells()[well], new_tip='never')
    P20_single.drop_tip()

    # Mix and Add 5 uL from Deep Well Block to PCR Plate 
    # Mix 3x with P300 set at 150 uL, (Uses new tip each time)
    # then transfer with P20 at 5 uL (Uses new tip each time)
    protocol.comment('Starting the mixing and transfer of specimen process...')
    for well in range(total_samples):
        P1000_single.pick_up_tip()
        P1000_single.mix(5, 150, multiwell_plate.wells()[well])
        P1000_single.drop_tip()
        P20_single.transfer(5, multiwell_plate.wells()[well], pcr_plate.wells()[well], new_tip='always')