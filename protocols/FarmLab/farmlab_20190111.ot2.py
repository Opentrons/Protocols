from opentrons import labware, instruments

trough_name = 'trough-1row-deep'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=10,
        depth=40)

# Labware setup
plate = labware.load('96-flat', '2')
trough_12 = labware.load('trough-12row', '1')
trough_1 = labware.load(trough_name, '3')
liquid_trash = labware.load('trough-1row-25ml', '4').wells('A1')
tiprack = labware.load('tiprack-200ul', '6')

dilution_buffer = trough_12.wells('A1')
conjugate = trough_12.wells('A2')
substrate = trough_12.wells('A3')
stop_solution = trough_12.wells('A4')

# Pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
        strip_number: int=10,
        dilution_buffer_volume: float=90,
        first_incubation_time: float=45,
        wash_cycle_number: int=5,
        second_incubation_time: float=30,
        third_incubation_time: float=15,
        stop_solution_volume: float=100
        ):

    targets = [well for well in plate.rows(0)[:strip_number]]
    target_dispense_loc = [well.top() for well in targets]
    target_aspirate_loc = [well.bottom(-0.5) for well in targets]

    # Transfer dilution buffer
    m300.transfer(
        dilution_buffer_volume,
        dilution_buffer,
        target_dispense_loc,
        blow_out=True)

    m300.delay(minutes=first_incubation_time)

    # Empty wells
    m300.transfer(
        dilution_buffer_volume + 20,
        target_aspirate_loc,
        liquid_trash.top(),
        blow_out=True)

    # Wash wells with wash buffer 5 times
    m300.pick_up_tip()
    for mix_repetition in range(wash_cycle_number):
        m300.transfer(
            180,
            trough_1.wells('A1'),
            target_dispense_loc,
            new_tip='never',
            blow_out=True)
        m300.transfer(200, target_aspirate_loc, liquid_trash.top(),
                      new_tip='never', blow_out=True)
    m300.drop_tip()

    # Transfer conjugate
    m300.transfer(
        100, conjugate, target_dispense_loc, blow_out=True)

    m300.delay(minutes=second_incubation_time)

    # Empty wells
    m300.transfer(120, target_aspirate_loc, liquid_trash.top(), blow_out=True)

    # Wash wells with wash buffer 5 times
    m300.pick_up_tip()
    for mix_repetition in range(wash_cycle_number):
        m300.transfer(
            180,
            trough_1.wells('A1'),
            target_dispense_loc,
            new_tip='never',
            blow_out=True)
        m300.transfer(200, target_aspirate_loc, liquid_trash.top(),
                      new_tip='never', blow_out=True)
    m300.drop_tip()

    # Transfer substrate
    m300.transfer(
        100, substrate, target_dispense_loc, blow_out=True)

    m300.delay(minutes=third_incubation_time)

    # Transfer stop solution
    m300.transfer(
        stop_solution_volume,
        stop_solution,
        target_dispense_loc,
        blow_out=True)


run_custom_protocol(
        **{'strip_number': 10,
        'dilution_buffer_volume': 90,
        'first_incubation_time': 45,
        'wash_cycle_number': 5,
        'second_incubation_time': 30,
        'third_incubation_time': 15,
        'stop_solution_volume': 100}
        )
