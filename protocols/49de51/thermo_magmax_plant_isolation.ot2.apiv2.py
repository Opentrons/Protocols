from time import sleep

def run(ctx):
    plate_count = get_values('plate_count')

    plate = ctx.load_labware(
            'nest_96_wellplate_2ml_deep', '8')
    # This protocol is broken in 3 steps:
    # 1. Initial lysis
    # 2. Precipitation
    # 3. Initial wash
    # 4. Final wash

    # labware
    reagents = ctx.load_labware(
            'nest_12_reservoir_15ml', '3')

    ## Lysis
    lysis_buffer_b = reagents.columns()[0]
    rnase_a = reagents.columns()[1]
    lysis_buffer_a = ctx.load_labware(
            'nest_1_reservoir_195ml', '5')
    ## Precipitation
    precipitation_solution = reagents.columns()[2]
    ## Initial wash
    beads = reagents.columns()[3]
    ethanol = ctx.load_labware(
            'nest_1_reservoir_195ml', '2')
    ## Final washes
    wash_1 = ctx.load_labware(
            'nest_1_reservoir_195ml', '6')
    wash_2 = ctx.load_labware(
            'nest_1_reservoir_195ml', '9')
    elution_buffer = reagents.columns()[4]
    
    ## Modules
    magdeck = ctx.load_module('magnetic module gen2', '1')
    magdeck.disengage()
    mag_plate = magdeck.load_labware('nest_96_wellplate_2ml_deep',
                                    'deepwell plate')
    tempdeck = ctx.load_module('Temperature Module Gen2', '4')
    temp_plate = tempdeck.load_labware('nest_96_wellplate_2ml_deep')

    ## tipracks
    tip_racks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', x) for x in ['10','11']]

    # pipette
    p300m = ctx.load_instrument(
            'p300_multi_gen2', p300_mount, tip_racks=tip_racks)

    # define tip pickups
    tip_count = 0
    tip_max = len(tipracks*96)
    def pick_up():
        nonlocal tip_count
        nonlocal tip_max
        if tip_count == tip_max:
            ctx.pause('Please refill tipracks before resuming.')
            p300m.reset_tipracks()
            tip_count = 0
        p300m.pick_up_tip()
        tip_count += 8


    ##################
    ## Initial Wash ##
    ##################
    ctx.home()
    tempdeck.set_temperature(65)

    p300m.transfer(500, lysis_buffer_a, plate)
    p300m.transfer(70, lysis_buffer_b, plate)
    p300m.transfer(20, rnase_a, plate)
    ctx.home()
    
    ###################
    ## Precipitation ##
    ###################
    ctx.pause('Homogenize samples, then return plate tempdeck on robot')
    sleep(600)
    p300m.transfer(130, precipitation_solution, temp_plate)
    ctx.home()

    ##################
    ## Initial wash ##
    ##################
    ctx.pause('Incubate on ice for 5 minutes, then return plate to deck position 8')
    p300m.transfer(400, plate, mag_plate)
    p300m.transfer(25, beads, mag_plate)
    p300m.transfer(400, ethanol, mag_plate)
    magdeck.engage()
    sleep(300)
    p300m.transfer(825, mag_plate, trash)
    magdeck.disengage()
    p300m.transfer(400, wash_1, mag_plate)
    
    ################
    ## Final wash ##
    ################
    ctx.pause('Vortex plate for 1 minute at 750 RPM, then replace onto magdeck')
    magdeck.engage()
    sleep(120)
    p300m.transfer(400, mag_plate, trash)

    def wash_2_function():
        magdeck.disengage()
        p300m.transfer(400, wash_2, mag_plate)
        # mix?
        magdeck.engage()
        sleep(120)
        p300m.transfer(400, mag_plate, trash)
    wash_2_function()
    wash_2_function()

    sleep(300)
    magdeck.disengage()
    p300m.transfer(150, elution_buffer, mag_plate)

    ################
    ## Heat plate ##
    ################
    ctx.pause('Vortex plate, then return to tempdeck on robot')
    tempdeck.set_temperature(70)
    sleep(300)

    #############
    ## Elution ##
    #############
    ctx.pause('Return plate to magdeck. Replace original plate at position 8 with a new skirted plate')
    new_plate = plate = ctx.load_labware(
            'nest_96_wellplate_100ul_pcr_full_skirt', '8')
    magdeck.engage()
    sleep(300)
    p300m.transfer(150, temp_plate, new_plate)
