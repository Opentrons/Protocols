from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Cleanup with AMPure Magnetic Beads',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad_96_wellplate_200ul_pcr', '1', share=True)
output_plate = labware.load('biorad_96_wellplate_200ul_pcr', '2')
reagent_container = labware.load('usascientific_12_reservoir_22ml', '7')
liquid_waste = reagent_container.wells('A12')


def run_custom_protocol(
        pipette_type: StringSelection(
        'p50_Multi', 'p300_Multi', 'p50_Single', 'p300_Single') = 'p50_Multi',
        pipette_mount: StringSelection('right', 'left') = 'right',
        sample_number: int = 96,
        PCR_volume: float = 20,
        bead_ratio: float = 1.0,
        elution_buffer_volume: float = 32.5):

    incubation_time = 300
    settling_time = 120
    drying_time = 15
    total_tips = sample_number*8
    tiprack_num = total_tips//96 + (1 if total_tips % 96 > 0 else 0)
    slots = ['3', '5', '6', '8', '9', '10', '11'][:tiprack_num]
    tipracks = [labware.load('opentrons_96_tiprack_300ul', slot)
                for slot in slots]

    if pipette_type == 'p300_Single':
        pipette = instruments.P300_Single(
            mount=pipette_mount,
            tip_racks=tipracks)

    elif pipette_type == 'p50_Single':
        pipette = instruments.P50_Single(
            mount=pipette_mount,
            tip_racks=tipracks)

    elif pipette_type == 'p50_Multi':
        pipette = instruments.P50_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)

    elif pipette_type == 'p300_Multi':
        pipette = instruments.P300_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)

    mode = pipette_type.split('_')[1]
    if mode == 'Single':
        samples = [well for well in mag_plate.wells()[:sample_number]]
        samples_top = [well.top() for well in samples]
        output = [well for well in output_plate.wells()[:sample_number]]

    else:
        col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
        samples = [col for col in mag_plate.cols()[:col_num]]
        samples_top = [well.top() for well in mag_plate.rows(0)[:col_num]]
        output = [col for col in output_plate.cols()[:col_num]]

    # Define reagents and liquid waste
    beads = reagent_container.wells(0)
    elution_buffer = reagent_container.wells(3)

    # Define bead and mix volume to resuspend beads
    bead_volume = PCR_volume*bead_ratio
    if mode == 'Single':
        if bead_volume*sample_number > pipette.max_volume:
            mix_vol = pipette.max_volume
        else:
            mix_vol = bead_volume*sample_number
    else:
        if bead_volume*col_num > pipette.max_volume:
            mix_vol = pipette.max_volume
        else:
            mix_vol = bead_volume*col_num

    mix_voltarget = PCR_volume + 10

    # Disengage MagDeck
    mag_deck.disengage()

    # Mix Speed
    pipette.set_flow_rate(aspirate=180, dispense=180)
    pipette.set_flow_rate(aspirate=180, dispense=180)
    pipette.pick_up_tip()
    pipette.mix(25, mix_vol, beads)

    # Mix beads and PCR samples
    for target in samples:
        if not pipette.tip_attached:
            pipette.pick_up_tip()

        pipette.mix(2, mix_vol, beads)
        # Slow down head speed 0.5X for bead handling
        max_speed_per_axis = {
            'x': (50), 'y': (50), 'z': (50), 'a': (10), 'b': (10), 'c': (10)}
        robot.head_speed(
            combined_speed=max(max_speed_per_axis.values()),
            **max_speed_per_axis)
        pipette.set_flow_rate(aspirate=10, dispense=10)
        pipette.transfer(
            bead_volume, beads, target, air_gap=0, new_tip='never')
        pipette.set_flow_rate(aspirate=50, dispense=50)
        pipette.mix(25, mix_voltarget, target)
        pipette.blow_out()
        max_speed_per_axis = {
            'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),
            'c': (40)}
        robot.head_speed(
            combined_speed=max(max_speed_per_axis.values()),
            **max_speed_per_axis)

        pipette.drop_tip()

    # Return robot head speed to the defaults for all axes
        max_speed_per_axis = {
            'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),
            'c': (40)}
        robot.head_speed(
            combined_speed=max(max_speed_per_axis.values()),
            **max_speed_per_axis)

    # Incubate beads and PCR product at RT for 5 minutes
    robot.comment("Incubating the beads and PCR products at room temperature \
for 5 minutes. Protocol will resume automatically.")
    pipette.delay(seconds=incubation_time)

    # Engage MagDeck and Magnetize
    robot._driver.run_flag.wait()
    mag_deck.engage()
    robot.comment("Delaying for "+str(settling_time)+" seconds for beads to \
settle.")
    pipette.delay(seconds=settling_time)

    # Remove supernatant from magnetic beads
    pipette.set_flow_rate(aspirate=25, dispense=120)
    for target in samples:
        pipette.transfer(
            25, target.bottom(0.7), liquid_waste.top(), blow_out=True)

    # Wash beads twice with 70% ethanol

    air_vol = pipette.max_volume*0.1

    for cycle in range(1, 3):
        pipette.pick_up_tip()
        for target in samples_top:
            pipette.transfer(
                185, reagent_container.wells(cycle), target,
                air_gap=air_vol, new_tip='never')
        robot.comment("Delaying for 17 seconds.")
        pipette.delay(seconds=17)
        for target in samples:
            if not pipette.tip_attached:
                pipette.pick_up_tip()
            pipette.transfer(195, target.bottom(0.7),
                             reagent_container.wells(cycle+8).top(),
                             air_gap=air_vol, new_tip='never')
            pipette.drop_tip()
        robot.pause('Protocol paused. When ready, click RESUME.')

    # Dry at RT
    robot.comment("Drying the beads for "+str(drying_time)+" minutes. Protocol \
will resume automatically.")
    pipette.delay(minutes=drying_time)

    # Disengage MagDeck
    robot._driver.run_flag.wait()
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
        pipette.mix(25, mix_vol, target)
        pipette.blow_out(target.top())
        pipette.drop_tip()

    # Incubate at RT for 3 minutes
    robot.comment("Incubating at room temperature for 2 minutes. Protocol will \
resume automatically.")
    pipette.delay(minutes=2)

    # Engage MagDeck for 2 minutes and remain engaged for DNA elution
    robot._driver.run_flag.wait()
    mag_deck.engage()
    robot.comment("Delaying for "+str(settling_time)+" seconds for beads to \
settle.")
    pipette.delay(seconds=settling_time)

    # Transfer clean PCR product to a new well
    elution_bv = elution_buffer_volume - 2.5
    for target, dest in zip(samples, output):
        pipette.transfer(elution_bv, target.bottom(1), dest.top(),
                         blow_out=True)

    # Disengage MagDeck
    mag_deck.disengage()
