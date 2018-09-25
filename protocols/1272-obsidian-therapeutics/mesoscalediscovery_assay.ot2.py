from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

# labware setup
source = labware.load('96-flat', '5')
output = labware.load('96-flat', '2')
tuberack = labware.load('opentrons-tuberack-15ml', '3')
tipracks300 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['4', '7', '9', '10']]

tiprack50 = labware.load('opentrons-tiprack-300ul', '8')
liquid_trash = labware.load('trough-1row-deep', '6')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks300)

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack50])


def wash_plate(repetition, dest_cols, reservoir):
    """
    Wash plate 3 times with 150 uL/well of wash buffer
    """
    m300.pick_up_tip()
    tip_loc = m300.current_tip()
    for cycle in range(3):
        if not m300.tip_attached:
            m300.start_at_tip(tip_loc)
            m300.pick_up_tip()
        for col in dest_cols:
            if m300.current_volume < 150:
                m300.aspirate(reservoir.cols(cycle+repetition*3))
            m300.dispense(150, col)
        m300.return_tip()
        if cycle == 2:
            trash = True
        else:
            trash = False
        m300.transfer(160, output.cols(), liquid_trash, blow_out=True,
                      trash=trash, new_tip='always')


def run_custom_protocols(
        container_type: StringSelection(
            'trough-12row', '96-deep-well')='trough-12row',
        number_of_samples: int=35):

    global source

    # labware setup
    reservoir = labware.load(container_type, '1')

    # plate setup
    calibrators = source.wells('A1', length=8)
    controls = source.wells('A2', length=3)
    samples = source.wells('A3', length=number_of_samples)
    source_loc = calibrators + controls + samples

    # define output plate destination locations
    dest_loc = []
    for col1, col2 in zip(output.cols[::2], output.cols[1::2]):
        for well1, well2 in zip(col1, col2):
            dest_loc.append([well1, well2])
    dest_loc = dest_loc[:number_of_samples+8+3]

    # define output plate destination cols
    total_cols = (number_of_samples+8+3)*2//8 + (
        1 if (number_of_samples+8+3)*2 % 8 > 0 else 0)
    dest_cols = [col.top() for col in output.cols('1', length=total_cols)]

    # wash plate 3 times with wash buffer
    wash_plate(0, dest_cols, reservoir)

    # add 50 uL of samples, calibrators, and control to output plate
    for source, dest in zip(source_loc, dest_loc):
        p50.transfer(50, source, dest)

    # pause for user to seal plate and shake plate
    robot.pause()

    # wash plate 3 times with wash buffer
    wash_plate(1, dest_cols, reservoir)

    # add 25 uL of detection antibody to output plate
    dispense_loc = [well.top() for wells in dest_loc for well in wells]
    p50.transfer(25, tuberack.wells('A1'), dispense_loc)

    # pause for user to seal and shake plate
    robot.pause()

    # wash plate 3 times with wash buffer
    wash_plate(2, dest_cols, reservoir)

    # add 150 uL buffer T to output plate using multi-channel
    m300.pick_up_tip()
    for col in dest_cols:
        if m300.current_volume < 150:
            m300.aspirate(reservoir.cols('12'))
        m300.dispense(150, col)
    m300.drop_tip()
