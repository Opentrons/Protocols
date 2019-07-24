from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Custom Omega Biotek Mag-Bind Protocol',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}


mag_deck = modules.load('magdeck', '10')
mag_plate = labware.load('usascientific_96_wellplate_2.4ml_deep',
                         '10', share=True)
reagent_container = labware.load('usascientific_12_reservoir_22ml', '7')


def run_custom_protocol(
    sample_number: int = 48,
    total_vol: float = 280,
    incubation_time_in_seconds: int = 30,
    settling_time_in_seconds: int = 120,
    ETR_Wash_Vol_in_ul: float = 50,
    wash_vol_in_ul: float = 400,
    bead_volume_in_ul: float = 145,
    ethanol_vol_in_ul: float = 182,
    pipette_type: StringSelection(
        'p300_Multi', 'p300_Single', 'p50_Multi',
        'p50_Single', 'p10_Single', 'p10_Multi',
        'p1000_Single') = 'p300_Single',
    pipette_axis: StringSelection('left', 'right') = 'left',
    start_vol_in_ul: float = 300,
    mix_vol_at_target_in_ul: float = 300,
    dry_time_in_minutes: int = 8,
    elution_buffer_volume_in_ul: float = 100,
    output_type: StringSelection('tube rack(s)',
                                 '96-well plate') = 'tube rack(s)'
):
    # checks
    if sample_number < 1 or sample_number > 96:
        raise Exception('Invalid sample number.')
    mode = pipette_type.split('_')[1]
    if mode == 'Multi' and output_type == 'tube rack(s)':
        raise Exception('Multi-channel pipette incompatible with tube racks.')

    # output setup
    if output_type == 'tube rack(s)':
        num_out_racks = 2 if sample_number > 48 else 1
        output_lw = [labware.load(
            'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', slot)
                     for slot in ['2', '3']][:num_out_racks]
    else:
        output_lw = [labware.load('biorad_96_wellplate_200ul_pcr')]

    # tipracks
    num_tip_racks = math.ceil(sample_number*4/96)
    slots = ['1', '6', '8', '11'][:num_tip_racks]

    capacity = pipette_type.split('_')[0]
    if capacity == 'p10':
        tiprack_name = 'opentrons_96_tiprack_10ul'
    elif capacity == 'p50' or capacity == 'p300':
        tiprack_name = 'opentrons_96_tiprack_300ul'
    else:
        tiprack_name = 'opentrons_96_tiprack_1000ul'

    if pipette_type == 'p1000_Single':
        tipracks = [labware.load('opentrons_96_tiprack_1000ul', slot)
                    for slot in slots]
        pipette = instruments.P1000_Single(
            mount=pipette_axis,
            tip_racks=tipracks)

    elif pipette_type == 'p300_Single':
        tipracks = [labware.load('opentrons_96_tiprack_300ul', slot)
                    for slot in slots]
        pipette = instruments.P300_Single(
            mount=pipette_axis,
            tip_racks=tipracks)

    elif pipette_type == 'p50_Single':
        tipracks = [labware.load('opentrons_96_tiprack_300ul', slot)
                    for slot in slots]
        pipette = instruments.P50_Single(
            mount=pipette_axis,
            tip_racks=tipracks)

    elif pipette_type == 'p10_Single':
        tipracks = [labware.load('opentrons_96_tiprack_10ul ', slot)
                    for slot in slots]
        pipette = instruments.P10_Single(
            mount=pipette_axis,
            tip_racks=tipracks)

    elif pipette_type == 'p10_Multi':
        tipracks = [labware.load('opentrons_96_tiprack_10ul ', slot)
                    for slot in slots]
        pipette = instruments.P10_Multi(
            mount=pipette_axis,
            tip_racks=tipracks)

    elif pipette_type == 'p50_Multi':
        tipracks = [labware.load('opentrons_96_tiprack_300ul', slot)
                    for slot in slots]
        pipette = instruments.P50_Multi(
            mount=pipette_axis,
            tip_racks=tipracks)

    elif pipette_type == 'p300_Multi':
        tipracks = [labware.load('opentrons_96_tiprack_300ul', slot)
                    for slot in slots]
        pipette = instruments.P300_Multi(
            mount=pipette_axis,
            tip_racks=tipracks)

    if mode == 'Single':
        samples = [well for well in mag_plate.wells()][:sample_number]
        output = [well for ol in output_lw
                  for well in ol.wells()][:sample_number]

    else:
        col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
        samples = [col for col in mag_plate.cols()][:col_num]
        output = [col for ol in output_lw
                  for col in ol.cols()][:col_num]

    # Define reagents and liquid waste
    beads = reagent_container.wells(0)
    ethanol = reagent_container.wells(1)
    SPMWash = reagent_container.wells(2)
    SPMWash2 = reagent_container.wells(3)
    elution_buffer = reagent_container.wells(4)
    liquid_waste = reagent_container.wells('A8', length=3)

    # Disengage MagDeck
    mix_vol_beads = 300
    mag_deck.disengage()

    # Mix beads and distribute
    for target in samples:
        pipette.set_flow_rate(aspirate=180, dispense=180)
        pipette.pick_up_tip()
        pipette.mix(9, mix_vol_beads, beads)
        pipette.transfer(
            bead_volume_in_ul,
            beads,
            target.top(),
            air_gap=0,
            new_tip='never')
        pipette.mix(4, 200, target)
        pipette.blow_out()
        pipette.drop_tip()

    # Add ethanol binding and mix
    binding_tiprack = labware.load(tiprack_name, '9')
    if mode == 'Multi':
        binding_tips = [tip for tip in binding_tiprack.rows('A')]
    else:
        binding_tips = [tip for tip in binding_tiprack.wells()]
    for tip, target in zip(binding_tips, samples):
        pipette.set_flow_rate(aspirate=180, dispense=180)
        pipette.pick_up_tip(tip)
        pipette.transfer(
            ethanol_vol_in_ul,
            ethanol,
            target.top(),
            air_gap=0,
            new_tip='never')
        pipette.mix(4, 200, target)
        pipette.blow_out()
        pipette.return_tip()

    # Incubate beads/product at RT
    pipette.delay(seconds=incubation_time_in_seconds)
    # Engage MagDeck and Magnetize
    mag_deck.engage(height=14)
    pipette.delay(seconds=settling_time_in_seconds)

    # Remove supernatant from magnetic beads
    pipette.set_flow_rate(aspirate=100, dispense=150)
    for tip, target in zip(binding_tips, samples):
        pipette.pick_up_tip(tip)
        pipette.transfer(
            total_vol,
            target.bottom(0.7),
            liquid_waste[0].top(),
            blow_out=True,
            new_tip='never')
        pipette.drop_tip()

    mag_deck.disengage()

    # Add first wash and mix
    first_wash_tiprack = labware.load(tiprack_name, '4')
    if mode == 'Multi':
        first_wash_tips = [tip for tip in first_wash_tiprack.rows('A')]
    else:
        first_wash_tips = [tip for tip in first_wash_tiprack.wells()]
    for tip, target in zip(first_wash_tips, samples):
        pipette.set_flow_rate(aspirate=180, dispense=180)
        pipette.pick_up_tip(tip)
        pipette.transfer(
            wash_vol_in_ul,
            SPMWash,
            target.top(),
            air_gap=0,
            new_tip='never')
        pipette.mix(5, mix_vol_beads, target)
        pipette.blow_out()
        pipette.return_tip()

    mag_deck.engage(height=14)
    pipette.delay(seconds=settling_time_in_seconds)
    # Remove supernatant from magnetic beads
    pipette.set_flow_rate(aspirate=100, dispense=100)
    for tip, target in zip(first_wash_tips, samples):
        pipette.pick_up_tip(tip)
        pipette.transfer(
            wash_vol_in_ul,
            target.bottom(),
            liquid_waste[1].top(),
            blow_out=True,
            new_tip='never')
        pipette.drop_tip()

    # Wash beads 2x
    mag_deck.disengage()

    second_wash_tiprack = labware.load(tiprack_name, '5')
    if mode == 'Multi':
        second_wash_tips = [tip for tip in second_wash_tiprack.rows('A')]
    else:
        second_wash_tips = [tip for tip in second_wash_tiprack.wells()]
    for tip, target in zip(second_wash_tips, samples):
        pipette.set_flow_rate(aspirate=180, dispense=180)
        pipette.pick_up_tip(tip)
        pipette.transfer(
            wash_vol_in_ul,
            SPMWash2,
            target.top(),
            air_gap=0,
            new_tip='never')
        pipette.mix(5, mix_vol_beads, target)
        pipette.blow_out()
        pipette.return_tip()

    mag_deck.engage(height=14)
    pipette.delay(seconds=settling_time_in_seconds)
    # Remove supernatant from magnetic beads
    pipette.set_flow_rate(aspirate=100, dispense=100)
    for tip, target in zip(second_wash_tips, samples):
        pipette.pick_up_tip()
        pipette.transfer(
            wash_vol_in_ul,
            target.bottom(),
            liquid_waste[2].top(),
            blow_out=True,
            new_tip='never')
        pipette.drop_tip()

    # Dry at RT
    pipette.delay(minutes=dry_time_in_minutes)
    # Disengage MagDeck
    mag_deck.disengage()

    # Mix beads with elution buffer
    elu_mix_vol = elution_buffer_volume_in_ul//2
    for target in samples:
        pipette.set_flow_rate(aspirate=180, dispense=180)
        pipette.pick_up_tip()
        pipette.transfer(
            elution_buffer_volume_in_ul,
            elution_buffer,
            target.top(),
            air_gap=0,
            new_tip='never')
        pipette.mix(10, elu_mix_vol, target)
        pipette.blow_out()
        pipette.drop_tip()

    # Incubate at RT for 2 minutes
    pipette.delay(seconds=settling_time_in_seconds)
    # Engage MagDeck for 1 minute and remain engaged for DNA elution
    mag_deck.engage(height=14)
    pipette.delay(seconds=settling_time_in_seconds)
    # Transfer clean PCR product to a new well
    for i, (target, dest) in enumerate(zip(samples, output)):
        pipette.transfer(
            elution_buffer_volume_in_ul,
            target.bottom(1),
            dest.top(),
            blow_out=True)
        if i == 47:
            robot.pause('Replace tubes in slots 2 and 3 before resuming.')

    # Disengage MagDeck
    mag_deck.disengage()
