import math

metadata = {
    'protocolName': 'Lyra Direct SARS-CoV Assay Sample Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):

    [total_samples, p20_mount, p300_mount] = get_values(  # noqa: F821
        "total_samples", "p20_mount", "p300_mount")

    total_samples = int(total_samples)
    cols = math.ceil(total_samples/8)

    # Load Tip Racks
    tipracks_20ul = [protocol.load_labware('opentrons_96_filtertiprack_20ul',
                                           slot) for slot in ['7', '8']]
    tipracks_200ul = [protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', slot) for slot in ['4', '5']]

    # Load Plates
    # 1 mL Deepwell Microtiter Plate
    deepwell_plate = protocol.load_labware('eppendorf_96_deepwell_1000ul', 2)
    # PCR Plate resting on top of the thermal block
    pcr_plate = protocol.load_labware('enduraplate_96_wellplate_200ul', 3)

    # Load Instruments
    p20 = protocol.load_instrument('p20_multi_gen2', p20_mount,
                                   tip_racks=tipracks_20ul)
    p300 = protocol.load_instrument('p300_multi_gen2', p300_mount,
                                    tip_racks=tipracks_200ul)

    p300.flow_rate.aspirate = 300
    p300.flow_rate.dispense = 300
    p20.flow_rate.aspirate = 12
    p20.flow_rate.dispense = 12

    # Proccess Buffer (A1)
    # 10 mL per channel, enough for 3 columns of sample
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 1)
    buffer_wells = [well for well in reservoir.rows()[0][:cols]
                    for i in range(3)]

    # Sample Wells
    deep_samples = deepwell_plate.rows()[0][:cols]
    pcr_samples = pcr_plate.rows()[0][:cols]

    # Protocol Steps

    # Add 400 uL of Process Buffer to Required Wells in Deep Well Block
    protocol.comment(f'Adding 400 uL of process buffer \
                     sequentially to {total_samples} wells...')
    p300.pick_up_tip()
    for well, buffer in zip(deep_samples, buffer_wells):
        p300.transfer(400, buffer, well,
                      new_tip='never')
    p300.drop_tip()

    # PAUSE PROTOCOL #
    protocol.pause('Pausing protocol for further specimen processing and \
                   addition of 15uL of master mix to the PCR plate. Click \
                   Resume when ready...')

    # Mix and Add 5 uL from Deep Well Block to PCR Plate
    # Mix 5x with P300 set at 150 uL, (Uses new tip each time)
    # then transfer with P20 at 5 uL (Uses new tip each time)
    protocol.comment('Starting the mixing and transfer of specimen process...')
    for source, dest in zip(deep_samples, pcr_samples):
        p300.pick_up_tip()
        p300.mix(5, 150, source)
        p300.drop_tip()
        p20.transfer(5, source,
                     dest, new_tip='always')
