from opentrons import labware, instruments, modules
from otcustomizers import StringSelection


def run_custom_protocol(module_type: StringSelection(
                            'None', 'temp', 'magnet')='None',
                        number_of_runs: int=40):

    if module_type == 'temp':
        module = modules.load('tempdeck', '7')
        module.set_temperature(4)
    elif module_type == 'magnet':
        module = modules.load('magdeck', '7')

    tipracks = [
        labware.load('opentrons-tiprack-300ul', slot) for slot in ['3', '6']]

    plate = labware.load('96-flat', '2')
    plate_384 = labware.load('384-plate', '5')
    tuberack_2ml = labware.load('opentrons-tuberack-2ml-eppendorf', '1')

    p300 = instruments.P300_Single(mount='right', tip_racks=[tipracks[0]])
    m300 = instruments.P300_Multi(mount='left', tip_racks=[tipracks[1]])
    count = 0
    for _ in range(number_of_runs):
        # Serial Dilution
        m300.pick_up_tip()
        m300.transfer(
            30,
            plate.cols('1', to='11'),
            plate.cols('2', to='12'),
            new_tip='never')

        # Transfer to 384 plate with multichannel
        alternating_wells = []
        for col in plate_384.cols('1', to='6'):
            alternating_wells.append(col[0].top())
            alternating_wells.append(col[1].top())
        m300.transfer(
            30,
            plate.cols('1', to='12'),
            alternating_wells,
            new_tip='never')
        m300.return_tip()

        # transfer to tuberacks
        p300.pick_up_tip()
        p300.distribute(
            30,
            tuberack_2ml.wells('A2'),
            tuberack_2ml.wells('A1', to='D1'),
            new_tip='never')

        if module_type == 'temp':
            module.set_temperature(20)
            module.wait_for_temp()
        if module_type == 'magnet':
            module.engage()

        # Mix at different heights
        value = 3
        for well in tuberack_2ml.wells('A1', to='D1'):
            p300.mix(5, 50, well.top(-value))
            value = value + 5
            # p300.move_to(well.top(-15))
            p300.touch_tip(-10)
        p300.return_tip()

        if module_type == 'temp':
            module.deactivate()
        elif module_type == 'magnet':
            module.disengage()

        count = count + 1
        if count == 12:
            m300.reset_tip_tracking()
            count = 0
