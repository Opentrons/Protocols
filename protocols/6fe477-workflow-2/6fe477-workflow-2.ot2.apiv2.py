metadata = {
    'protocolName': 'Nucleic Acid Purification - Workflow 2',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(protocol):

    [total_samples, pool_size, p300_mount,
     p1000_mount] = get_values(  # noqa: F821
     "total_samples", "pool_size", "p300_mount", "p1000_mount")

    pool_size = int(pool_size)
    total_samples = int(total_samples)

    # Load Tip Racks
    tiprack_200ul_filter = protocol.load_labware(
        'opentrons_96_filtertiprack_200ul', 5)
    tiprack_1000ul = protocol.load_labware('opentrons_96_tiprack_1000ul', 6)

    # Load Pipettes
    p300 = protocol.load_instrument('p300_single_gen2', p300_mount,
                                    tip_racks=[tiprack_200ul_filter])
    p1000 = protocol.load_instrument('p1000_single_gen2', p1000_mount,
                                     tip_racks=[tiprack_1000ul])

    # 1.5mL Tube Rack
    tube_rack = protocol.load_labware('vwr_24_tuberack_1.5ml', 2)

    # Lysis Buffer Reservoir
    buffer_reservoir = protocol.load_labware('nest_1_reservoir_195ml', 3)['A1']

    # Load 7 Tube Racks with Samples in 30 mL Tubes
    for slot in range(1, 12):
        if slot not in protocol.loaded_labwares:
            protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical',
                                  slot)

    all_wells = [protocol.loaded_labwares[i].wells()[j] for i in [1, 4, 7, 8,
                 9, 10, 11] for j in range(6)]
    all_wells = all_wells[:total_samples]
    sample_wells = [all_wells[i:i + pool_size] for i in range(0,
                    len(all_wells), pool_size)]
    dest_wells = tube_rack.wells()[0:len(sample_wells)]

    protocol.comment(f'Adding 40 uL samples with a pool size of {pool_size}')
    for i in range(len(sample_wells)):
        p300.flow_rate.aspirate = 30
        p300.transfer(40, sample_wells[i], dest_wells[i], new_tip='always')

    # Transfer 560 uL of Lysis Buffer into samples in tube rack
    protocol.comment('Adding 560 uL of Lysis buffer into 1.5mL tubes on the \
                     tube rack')
    p1000.transfer(560, buffer_reservoir, dest_wells, new_tip='always')
