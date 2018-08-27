from opentrons import instruments, labware

# labware setup
output_plate = labware.load('96-PCR-tall', '1')
trough = labware.load('trough-12row', '2')
tiprack_p10 = labware.load('tiprack-10ul', '4')
tiprack_p300_1 = labware.load('tiprack-200ul', '3')
tiprack_p300_2 = labware.load('tiprack-200ul', '5')
tiprack_p300_3 = labware.load('tiprack-200ul', '6')
tiprack_p300_4 = labware.load('tiprack-200ul', '7')
tiprack_p300_5 = labware.load('tiprack-200ul', '8')
tiprack_p300_6 = labware.load('tiprack-200ul', '9')
liquid_trash = labware.load('point', '10')

# variables and reagents setup
water = trough.well('A1')  # location of water in trough
fbs = trough.well('A8')  # location of fbs in trough
np = trough.well('A9')  # location of nanoparticles in trough

# instrument setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=[tiprack_p10]
)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_p300_1, tiprack_p300_2, tiprack_p300_3, tiprack_p300_4,
               tiprack_p300_5, tiprack_p300_6]
)


def check_trough_volume(water_vol):
    global water
    # upper limit of liquid volume in trough is max_volume - 1 mL
    trough_vol = water.max_volume()-1000
    if water_vol > trough_vol:
        new_loc = next(water)
        water = new_loc
        water_vol = 0
    return water_vol


def run_custom_protocol(
    number_of_columns: int=12,
    aspirate_height: int=5
        ):

    dest_loc = output_plate.cols[0:number_of_columns]

    water_vol = 0

    m300.pick_up_tip()
    for col in dest_loc:
        water_vol += 261*8
        water_vol = check_trough_volume(water_vol)
        m300.transfer(261, water, col, new_tip='never')
    m300.drop_tip()

    m300.transfer(30, fbs, dest_loc, new_tip='once')

    m10.transfer(9, np, dest_loc, new_tip='once')

    for index, col in enumerate(dest_loc):
        m300.pick_up_tip()
        if index == 0:
            tip_loc = m300.current_tip()
        m300.mix(3, 250, col)
        m300.return_tip()

    m10.delay(minutes=30)

    m300.start_at_tip(tip_loc)
    for col in dest_loc:
        m300.transfer(
            250,
            col.bottom(aspirate_height),
            liquid_trash,
            new_tip='always')

    # Wash with water 4 times
    # Using the same tip to add water and to remove waste in each cycle
    for cycle in range(4):
        # add 250 uL of water
        for index, col in enumerate(dest_loc):
            water_vol += 250*8
            water_vol = check_trough_volume(water_vol)
            m300.pick_up_tip()
            if index == 0:
                tip_loc = m300.current_tip()
            m300.transfer(250, water, col, mix_after=(3, 300), new_tip='never')
            m300.drop_tip()

        # wait 15 minutes for NP to settle
        m300.delay(minutes=15)

        # remove 250 uL of water
        m300.start_at_tip(tip_loc)
        for col in dest_loc:
            m300.transfer(
                250,
                col.bottom(aspirate_height),
                liquid_trash,
                new_tip='always')
