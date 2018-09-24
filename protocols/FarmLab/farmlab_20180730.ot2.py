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
liquid_trash = labware.load(trough_name, '4')
tiprack = labware.load('tiprack-200ul', '6')

dilution_buffer = trough_12.wells('A1')
conjugate = trough_12.wells('A2')
substrate = trough_12.wells('A3')
stop_solution = trough_12.wells('A4')

# Pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(strip_number: int=10):

    target_strips = plate.cols(0, length=strip_number)

    # Transfer dilution buffer
    m300.transfer(90, dilution_buffer, target_strips, blow_out=True)

    # Empty wells
    m300.transfer(110, target_strips, liquid_trash.top(), blow_out=True)

    # Wash wells with wash buffer 5 times
    m300.pick_up_tip()
    for each_strip in target_strips:
        for mix_repetition in range(5):
            m300.transfer(300, trough_1, each_strip, new_tip='never',
                          blow_out=True)
            m300.transfer(320, each_strip, liquid_trash.top(), new_tip='never',
                          blow_out=True)
    m300.drop_tip()

    # Transfer conjugate
    m300.transfer(100, conjugate, target_strips, blow_out=True)

    # Empty wells
    m300.transfer(120, target_strips, liquid_trash.top(), blow_out=True)

    # Wash wells with wash buffer 5 times
    m300.pick_up_tip()
    for each_strip in target_strips:
        for mix_repetition in range(5):
            m300.transfer(300, trough_1, each_strip, new_tip='never',
                          blow_out=True)
            m300.transfer(320, each_strip, liquid_trash.top(), new_tip='never',
                          blow_out=True)
    m300.drop_tip()

    # Transfer substrate
    m300.transfer(100, substrate, target_strips, blow_out=True)

    # Transfer stop solution
    m300.transfer(100, stop_solution, target_strips, blow_out=True)
