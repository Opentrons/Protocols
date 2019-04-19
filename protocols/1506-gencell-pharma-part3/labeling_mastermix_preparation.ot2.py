from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Labeling Master Mix Preparation',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        sample_num: int=8,
        control_num: int=8):

    # labware setup
    mix_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '4')
    labware.load('tempdeck', '10')
    temp_rack = labware.load('opentrons-aluminum-block-2ml-eppendorf', '10',
                             share=True)
    samples_control_plate = labware.load('PCR-strip-tall', '1')

    tiprack_300 = labware.load('opentrons-tiprack-300ul', '5')

    # instruments setup
    m50 = instruments.P50_Multi(
        mount='right',
        tip_racks=[tiprack_300])

    water = temp_rack.wells('A1')
    RE_buffer = temp_rack.wells('A2')
    dntps = temp_rack.wells('A3')
    cy3 = temp_rack.wells('A4')
    cy5 = temp_rack.wells('A5')
    exo = temp_rack.wells('A6')

    mixcy3 = mix_rack.wells('A1')
    mixcy5 = mix_rack.wells('A3')
    samples = samples_control_plate.wells('A1', length=sample_num)
    controls = samples_control_plate.wells('A6', length=control_num)

    if sample_num <= 8:
        sample_cols = [samples_control_plate.cols('1')]
    else:
        sample_cols = [col for col in samples_control_plate.cols(
            '1', length=math.ceil(sample_num/8))]
    if control_num <= 8:
        control_cols = [samples_control_plate.cols('6')]
    else:
        control_cols = [col for col in samples_control_plate.cols(
            '6', length=math.ceil(control_num/8))]

    # Transfer reagents to mastermixes
    s_factor = sample_num + 0.5
    c_factor = control_num + 0.5

    m50.distribute(
        [s_factor * 2, c_factor * 2],
        water,
        [mixcy3, mixcy5],
        disposal_vol=5
        )

    m50.transfer(
        [s_factor * 10, c_factor * 10],
        RE_buffer,
        [mixcy3.top(), mixcy5.top()],
        blow_out=True
        )

    m50.transfer(
        [s_factor * 5, c_factor * 5],
        dntps,
        [mixcy3.top(), mixcy5.top()],
        blow_out=True
        )

    for source, vol, dest in zip(
            [cy3, cy5], [s_factor * 3, c_factor * 3], [mixcy3, mixcy5]):
        m50.pick_up_tip()
        m50.mix(5, 30, source)
        m50.transfer(vol, source, dest, new_tip='never')
        m50.mix(5, 50, dest)
        m50.drop_tip()

    for vol, dest in zip([s_factor * 1, c_factor * 1], [mixcy3, mixcy5]):
        m50.pick_up_tip()
        if dest == mixcy3:
            m50.mix(5, 10, exo)
        m50.transfer(vol, exo, dest, new_tip='never')
        m50.mix(5, 10, dest)
        m50.drop_tip()

    # Distribute mastermixes in samples and controls
    for source, dests in zip([mixcy3, mixcy5], [samples, controls]):
        dest_wells = [well for well in dests]
        m50.pick_up_tip()
        m50.mix(5, 50, source)
        m50.distribute(21, source, dest_wells, disposal_vol=5, new_tip='never')
        m50.drop_tip()

    for col in sample_cols + control_cols:
        m50.pick_up_tip()
        m50.mix(5, 30, col)
        m50.blow_out(col[0].top())
        m50.drop_tip()
