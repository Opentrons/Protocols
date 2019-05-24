from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Mass Spec Sample Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create labware
plate_name = 'Falcon-96-round'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.35,
        depth=10.59,
        volume=320
    )

# load labware and modules
tempdeck = modules.load('tempdeck', '1')
plate2 = labware.load(plate_name, '1', share=True)
plate1 = labware.load(plate_name, '2', 'plate 1')
plate3 = labware.load(plate_name, '3', 'plate 3')
trough = labware.load('trough-12row', '4')
tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
tips = [labware.load('tiprack-10ul', slot) for slot in ['6', '7']]

# pipettes
p10 = instruments.P10_Single(mount='right', tip_racks=tips)

# setup wells
plate1_wells = [well for row in plate1.rows() for well in row]
plate2_wells = [well for row in plate2.rows() for well in row]
plate3_wells = [well for row in plate3.rows() for well in row]
tube = tuberack.wells('A1')
solution = trough.wells('A1')


def run_custom_protocol(start_temperature_in_Celsius: int = 25,
                        stop_temperature_in_Celsius: int = 95):

    # check input temperatures for too great of a range
    if abs(start_temperature_in_Celsius-stop_temperature_in_Celsius) > 95:
        raise Exception("Please enter a range of temperatures 96˚C apart "
                        "or fewer.")

    # determine whether to increment or decrement temperature
    if start_temperature_in_Celsius > stop_temperature_in_Celsius:
        s = -1
    elif start_temperature_in_Celsius < stop_temperature_in_Celsius:
        s = 1
    else:
        raise Exception("Please enter distinct start and stop temperatures.")

    # loop through temperatures and wells
    for temp, well1, well2, well3 in zip(range(start_temperature_in_Celsius,
                                               stop_temperature_in_Celsius+s,
                                               s),
                                         plate1_wells,
                                         plate2_wells,
                                         plate3_wells):
        if not robot.is_simulating():
            tempdeck.set_temperature(temp)
            tempdeck.wait_for_temp()

        # step 1
        p10.transfer(10, tube, well1, blow_out=True)

        # step 2
        p10.pick_up_tip()
        p10.transfer(90, solution, well1.top(), new_tip='never', blow_out=True)
        p10.mix(10, 10, well1)

        # step 3
        p10.transfer(100, well1, well2.top(), new_tip='never', blow_out=True)
        for _ in range(2):
            p10.delay(minutes=2)
            p10.mix(5, 10, well2)
        p10.transfer(100, well2, well3, new_tip='never')
        p10.drop_tip()
