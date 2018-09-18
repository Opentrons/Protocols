from opentrons import instruments, labware, modules

# labware setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
trough = labware.load('trough-12row', '2')
source_plate = labware.load('96-flat', '3', 'source_plate')
tiprack_p50 = labware.load('tiprack-200ul', '4', 'tiprack50')
tiprack_p300_1 = labware.load('tiprack-200ul', '5', 'tiprack300_1')
tiprack_p300_2 = labware.load('tiprack-200ul', '6', 'tiprack300_2')
tiprack_p300_3 = labware.load('tiprack-200ul', '7', 'tiprack300_3')
tiprack_p300_4 = labware.load('tiprack-200ul', '8', 'tiprack300_4')
tiprack_p300_5 = labware.load('tiprack-200ul', '9', 'tiprack300_5')
tiprack_p300_6 = labware.load('tiprack-200ul', '11', 'tiprack300_6')
liquid_trash = labware.load('point', '10', 'liquid_trash')

# variables and reagents setup
water = trough.wells('A1')  # location of water in trough
fbs = source_plate.cols('1')  # location of fbs in source plate
np = source_plate.cols('2')  # location of nanoparticles in trough

# instrument setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack_p50])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_p300_1, tiprack_p300_2, tiprack_p300_3, tiprack_p300_4,
               tiprack_p300_5, tiprack_p300_6])


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
        aspirate_height: int=1
        ):

    dest_loc = mag_plate.cols[0:number_of_columns]

    water_vol = 0

    # Transfer water from trough to mag-plate
    m300.pick_up_tip()
    for col in dest_loc:
        water_vol += 261*8
        water_vol = check_trough_volume(water_vol)
        m300.transfer(261, water, col, new_tip='never')
    m300.drop_tip()

    # Transfer FBS from column 1 of source plate to mag-plate
    m50.pick_up_tip()
    for loc in dest_loc:
        m50.transfer(30, fbs, loc.top(), new_tip='never')
    m50.drop_tip()

    # Transfer NP from column 2 of source plate ot mag-plate
    m50.pick_up_tip()
    for loc in dest_loc:
        if m50.current_volume < 9:
            m50.blow_out(np)
            m50.aspirate(np)
        m50.dispense(9, loc.top())
    m50.drop_tip()

    # Mix content in each well 3 times with 250 uL
    for index, col in enumerate(dest_loc):
        m300.pick_up_tip()
        m300.mix(3, 250, col)
        m300.return_tip()

    # Delay for 30 minutes
    m50.delay(minutes=30)

    # Turn on magnetic module for 15 minutes
    mag_module.engage(height=18)
    m50.delay(minutes=15)

    # Discard solution from mag-plate
    for col in dest_loc:
        m300.transfer(
            270,
            col.bottom(aspirate_height),
            liquid_trash,
            new_tip='always')

    # Turn off magnetic module
    mag_module.disengage()

    # Wash with water 4 times
    # Using the same tip to add water and to remove waste in each cycle
    for cycle in range(3):
        # add 250 uL of water
        for index, col in enumerate(dest_loc):
            water_vol += 250*8
            water_vol = check_trough_volume(water_vol)
            m300.pick_up_tip()
            if index == 0:
                tip_loc = m300.current_tip()
            m300.transfer(250, water, col, mix_after=(3, 250), new_tip='never')
            m300.return_tip()

        # wait 15 minutes for NP to settle
        mag_module.engage(height=18)
        m300.delay(minutes=15)

        # remove 250 uL of water
        m300.start_at_tip(tip_loc)
        for col in dest_loc:
            m300.transfer(
                270,
                col.bottom(aspirate_height),
                liquid_trash,
                new_tip='always')
        mag_module.disengage()
