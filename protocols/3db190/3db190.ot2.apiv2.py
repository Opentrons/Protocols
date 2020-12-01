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
    tipracks_20ul = [protocol.load_labware('opentrons_96_filtertiprack_20ul',
                                           slot) for slot in ['7', '8']]
    tipracks_1000ul = [protocol.load_labware(
        'opentrons_96_filtertiprack_1000ul', slot) for slot in ['4', '5']]

    # Load Plates
    # 1 mL Deepwell Microtiter Plate
    deepwell_plate = protocol.load_labware('eppendorf_96_deepwell_1000ul', 2)
    # PCR Plate resting on top of the thermal block
    pcr_plate = protocol.load_labware('enduraplate_96_wellplate_200ul', 3)

    # Load Instruments
    p20 = protocol.load_instrument('p20_single_gen2', p20_mount,
                                   tip_racks=tipracks_20ul)
    p1000 = protocol.load_instrument('p1000_single_gen2', p1000_mount,
                                     tip_racks=tipracks_1000ul)

    # Proccess Buffer (A1)
    buffer = protocol.load_labware(
        'opentrons_6_tuberack_falcon_50ml_conical', 1)['A1']

    deep_samples = deepwell_plate.wells()[:total_samples]
    pcr_samples = pcr_plate.wells()[:total_samples]

    # Protocol Steps

    # Add 400 uL of Process Buffer to Required Wells in Deep Well Block
    protocol.comment(f'Adding 400 uL of process buffer \
                     sequentially to {total_samples} wells...')
    p1000.pick_up_tip()
    for well in deep_samples:
        p1000.transfer(400, buffer, well,
                       new_tip='never')
    p1000.drop_tip()

    # PAUSE PROTOCOL #
    protocol.pause('Pausing protocol for further specimen processing and \
                   addition of 15uL of master mix to the PCR plate. Click \
                   Resume when ready...')

    # Mix and Add 5 uL from Deep Well Block to PCR Plate
    # Mix 5x with P1000 set at 150 uL, (Uses new tip each time)
    # then transfer with P20 at 5 uL (Uses new tip each time)
    protocol.comment('Starting the mixing and transfer of specimen process...')
    for source, dest in zip(deep_samples, pcr_samples):
        p1000.pick_up_tip()
        p1000.mix(5, 150, source)
        p1000.drop_tip()
        p20.transfer(5, source,
                     dest, new_tip='always')
