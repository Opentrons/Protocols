from opentrons import labware, instruments, modules, robot

# create custom labware
beckman_tube_rack = 'beckman-24-tube-rack'
if beckman_tube_rack not in labware.list():
    labware.create(
        beckman_tube_rack,
        grid=(6, 4),
        spacing=(20, 20),
        diameter=5,
        depth=40)

# labware setup
trough = labware.load('trough-12row', '7')
H2SO4_MeOH = trough.wells('A1')
water = trough.wells('A2')
hexane = trough.wells('A3')

tuberack = labware.load(beckman_tube_rack, '4')

tipracks = [
            labware.load('tiprack-200ul', '5'),
            labware.load('tiprack-200ul', '6'),
            labware.load('tiprack-200ul', '8'),
            labware.load('tiprack-200ul', '9')
            ]

# pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks)

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=tipracks)


def run_custom_protocol(
    number_of_plates: int=3,
    columns_to_fill: int=36,
    mix_aspirate_height: int=5,
    mix_dispense_height: int=12,
    hexane_layer_height: int=11
        ):

    # if only one plate is present, Temp Deck is deployed and set to 65 degree
    if number_of_plates == 1:
        temp_deck = modules.load('tempdeck', '1')
        # temp_deck.connect()
        temp_deck.set_temperature(65)
        plate = [labware.load('96-deep-well', '1', share=True)]
    # if more than one plate, plates are located in slot 1, 2, and/or 3
    else:
        plate = [
                 labware.load('96-deep-well', str(num+1))
                 for num in range(number_of_plates)
                 ]

    cols_in_plates = len(plate[0].cols())
    full_plates = columns_to_fill//cols_in_plates
    cols_left = columns_to_fill % cols_in_plates

    # list of columns to fill, when height does not matter
    cols_loc = [col
                for plate in plate[0:full_plates]
                for col in plate.cols()] + \
               [col
                for col in plate[full_plates-1].cols(0, length=cols_left)
                if cols_left > 0]

    # transfer Sulfuric acid-methanol to columns, using same tips
    m300.pick_up_tip()
    for col in cols_loc:
        m300.transfer(200, H2SO4_MeOH, col.top(-1), new_tip='never')
    m300.drop_tip()

    robot.pause()

    # turn off Temp Deck
    if number_of_plates == 1:
        temp_deck.deactivate()

    # transfer water to columns, using same tips
    m300.pick_up_tip()
    for col in cols_loc:
        m300.transfer(400, water, col.top(-1), new_tip='never')
    m300.drop_tip()

    # transfer hexane to columns, mix 3 times, changing tips between transfers
    for col in cols_loc:
        m300.pick_up_tip()
        m300.transfer(200, hexane, col.top(-1), new_tip='never')
        for mix_cycle in range(3):
            m300.aspirate(300, col.bottom(mix_aspirate_height))
            m300.dispense(300, col.bottom(mix_dispense_height))
        m300.drop_tip()

    # transform column list to a list of well for single pipette
    wells_loc = [well.bottom(hexane_layer_height)
                 for col in cols_loc
                 for well in col]

    # transfer 24 wells from the plate to custom tube rack
    # pause after 24 tubes have been filled, user replace rack and resume run
    count = 0
    p300.pick_up_tip()
    for well in wells_loc:
        p300.transfer(100, well, tuberack.wells(count), new_tip='never')
        p300.mix(2, 200, hexane)
        if count < 23:
            count += 1
        else:
            count = 0
            robot.pause()
