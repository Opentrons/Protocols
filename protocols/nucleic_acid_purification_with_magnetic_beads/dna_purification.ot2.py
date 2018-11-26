from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
output_plate = labware.load('biorad-hardshell-96-PCR', '2')


def run_custom_protocol(
        pipette_type: StringSelection(
            'p300_Multi', 'p50_Single', 'p300_Single', 'p1000_Single',
            'p10_Multi', 'p50_Multi', 'p10_Single'
            )='p300_Multi',
        pipette_mount: StringSelection('left', 'right')='left',
        sample_number: int=24,
        sample_volume: float=20,
        bead_ratio: float=1.8,
        elution_buffer_volume: float=200,
        incubation_time: float=1,
        settling_time: float=1,
        drying_time: float=5):

    total_tips = sample_number*8
    tiprack_num = total_tips//96 + (1 if total_tips % 96 > 0 else 0)
    slots = ['3', '5', '6', '7', '8', '9', '10', '11'][:tiprack_num]
    if pipette_type == 'p1000_Single':
        tipracks = [labware.load('tiprack-1000ul', slot) for slot in slots]
        pipette = instruments.P1000_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p300_Single':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P300_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p50_Single':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P50_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p10_Single':
        tipracks = [labware.load('tiprack-10ul', slot) for slot in slots]
        pipette = instruments.P10_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p10_Multi':
        tipracks = [labware.load('tiprack-10ul', slot) for slot in slots]
        pipette = instruments.P10_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p50_Multi':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P50_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p300_Multi':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P300_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)

    mode = pipette_type.split('_')[1]

    if mode == 'Single':
        if sample_number <= 5:
            reagent_container = labware.load('tube-rack-2ml', '4')
            liquid_waste = labware.load('trough-12row', '5').wells('A12')
        else:
            reagent_container = labware.load('trough-12row', '4')
            liquid_waste = reagent_container.wells('A12')
        samples = [well for well in mag_plate.wells()[:sample_number]]
        output = [well for well in output_plate.wells()[:sample_number]]
    else:
        reagent_container = labware.load('trough-12row', '4')
        liquid_waste = reagent_container.wells('A12')
        col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
        samples = [col for col in mag_plate.cols()[:col_num]]
        output = [col for col in output_plate.cols()[:col_num]]

    # Define reagents and liquid waste
    beads = reagent_container.wells(0)
    ethanol = reagent_container.wells(1)
    elution_buffer = reagent_container.wells(2)

    # Define bead and mix volume
    bead_volume = sample_volume*bead_ratio
    if bead_volume/2 > pipette.max_volume:
        mix_vol = pipette.max_volume
    else:
        mix_vol = bead_volume/2
    total_vol = bead_volume + sample_volume + 5

    # Mix beads and PCR samples
    for target in samples:
        pipette.pick_up_tip()
        pipette.mix(5, mix_vol, beads)
        pipette.transfer(bead_volume, beads, target, new_tip='never')
        pipette.mix(10, mix_vol, target)
        pipette.blow_out()
        pipette.drop_tip()

    # Incubate beads and PCR product at RT for 5 minutes
    pipette.delay(minutes=incubation_time)

    # Engagae MagDeck and incubate
    mag_deck.engage()
    pipette.delay(minutes=settling_time)

    # Remove supernatant from magnetic beads
    pipette.set_flow_rate(aspirate=25, dispense=150)
    for target in samples:
        pipette.transfer(total_vol, target, liquid_waste, blow_out=True)

    # Wash beads twice with 70% ethanol
    air_vol = pipette.max_volume * 0.1
    for cycle in range(2):
        for target in samples:
            pipette.transfer(200, ethanol, target, air_gap=air_vol,
                             new_tip='once')
        pipette.delay(minutes=1)
        for target in samples:
            pipette.transfer(200, target, liquid_waste, air_gap=air_vol)

    # Dry at RT
    pipette.delay(minutes=drying_time)

    # Disengage MagDeck
    mag_deck.disengage()

    # Mix beads with elution buffer
    if elution_buffer_volume/2 > pipette.max_volume:
        mix_vol = pipette.max_volume
    else:
        mix_vol = elution_buffer_volume/2
    for target in samples:
        pipette.pick_up_tip()
        pipette.transfer(
            elution_buffer_volume, elution_buffer, target, new_tip='never')
        pipette.mix(20, mix_vol, target)
        pipette.drop_tip()

    # Incubate at RT for 3 minutes
    pipette.delay(minutes=5)

    # Engagae MagDeck for 1 minute and remain engaged for DNA elution
    mag_deck.engage()
    pipette.delay(minutes=settling_time)

    # Transfer clean PCR product to a new well
    for target, dest in zip(samples, output):
        pipette.transfer(elution_buffer_volume, target, dest, blow_out=True)
