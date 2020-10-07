from time import sleep

metadata={"apiLevel": "2.3"}

def run(ctx):
    #plate_count = get_values('plate_count')

    plate = ctx.load_labware(
            'nest_96_wellplate_2ml_deep', '6')
    # labware
    liquid_trash = ctx.load_labware(
            'nest_1_reservoir_195ml','8').wells()[0]
    reagents = ctx.load_labware(
            'nest_12_reservoir_15ml', '3')

    ## Lysis
    lysis_buffer_b = reagents.columns()[0]
    rnase_a = reagents.columns()[1]
    lysis_buffer_a_wash_1 = ctx.load_labware(
            'nest_1_reservoir_195ml', '5').wells()[0]
    ## Precipitation
    precipitation_solution = reagents.columns()[2]
    ## Initial wash
    beads = reagents.columns()[3]
    ethanol_wash_2 = ctx.load_labware(
            'nest_1_reservoir_195ml', '2').columns()[0]
    elution_buffer = reagents.columns()[4]
    
    ## Modules
    magdeck = ctx.load_module('magnetic module gen2', '1')
    magdeck.disengage()
    mag_plate = magdeck.load_labware('nest_96_wellplate_2ml_deep',
                                    'deepwell plate')
    tempdeck = ctx.load_module('Temperature Module Gen2', '4')
    temp_plate = tempdeck.load_labware('nest_96_wellplate_2ml_deep')

    ## tipracks
    tip_racks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', x) for x in ['7','10','11']]

    # pipette
    p300m = ctx.load_instrument(
            'p300_multi_gen2', "right", tip_racks=tip_racks)

    # define tip pickups
    tip_count = 0
    tip_max = len(tip_racks*96)
    def pick_up():
        nonlocal tip_count
        nonlocal tip_max
        if tip_count == tip_max:
            ctx.pause('Please refill tipracks before resuming.')
            p300m.reset_tipracks()
            tip_count = 0
        tip_count += 8
    def pick_up_plate():
        for _ in range(0,12):
            pick_up()

    ###################
    ## Initial Lysis ##
    ###################
    ctx.home()
    tempdeck.set_temperature(65)
    
    def initial_lysis(plate):
        pick_up_plate()
        [p300m.transfer(500, lysis_buffer_a_wash_1, col) for col in plate.columns()]
        pick_up_plate()
        [p300m.transfer(70, lysis_buffer_b, col) for col in plate.columns()]
        pick_up_plate()
        [p300m.transfer(20, rnase_a, col) for col in plate.columns()]
        ctx.home()
    initial_lysis(plate)
    
    ###################
    ## Precipitation ##
    ###################
    ctx.pause('Homogenize samples, then return plate tempdeck on robot')
    #sleep(600)
    pick_up_plate()
    [p300m.transfer(130, precipitation_solution, col) for col in temp_plate.columns()]
    ctx.home()

    ##################
    ## Initial wash ##
    ##################
    ctx.pause('Incubate on ice for 5 minutes, then return plate to deck')
    def initial_wash():
        pick_up_plate()
        [p300m.transfer(400, plate.columns()[x], mag_plate.columns()[x]) for x in range(0,12)]
        pick_up_plate()
        [p300m.transfer(25, beads, col, mix_before=(3,100)) for col in mag_plate.columns()]
        pick_up_plate()
        [p300m.transfer(400, ethanol_wash_2, col, mix_after=(3,200)) for col in mag_plate.columns()]
        magdeck.engage()
        #sleep(300)
        pick_up_plate()
        [p300m.transfer(825, col, liquid_trash) for col in mag_plate.columns()]
        pick_up_plate()
        magdeck.disengage()
        [p300m.transfer(400, lysis_buffer_a_wash_1, col) for col in mag_plate.columns()]
    initial_wash()
    
    ################
    ## Final wash ##
    ################
    ctx.pause('Vortex plate for 1 minute at 750 RPM, then replace onto magdeck')
    magdeck.engage()

    def wash_2_function():
        magdeck.engage()
        #sleep(120)
        pick_up_plate()
        [p300m.transfer(400, col, liquid_trash) for col in mag_plate.columns()]
        magdeck.disengage()
        pick_up_plate()
        [p300m.transfer(400, ethanol_wash_2, col) for col in mag_plate.columns()]
        # mix?
        magdeck.engage()
        #sleep(120)
        pick_up_plate()
        [p300m.transfer(400, col, liquid_trash) for col in mag_plate.columns()]
        #sleep(300)
        magdeck.disengage()
        pick_up_plate()
        [p300m.transfer(150, elution_buffer, col) for col in mag_plate.columns()]
        ctx.home()
    wash_2_function()
    wash_2_function()


    ################
    ## Heat plate ##
    ################
    ctx.pause('Vortex plate, then return to tempdeck on robot')
    tempdeck.set_temperature(70)
    #sleep(300)

    #############
    ## Elution ##
    #############
    # Not being able to overload current labware gets really annoying here...
    ctx.pause('Return plate to magdeck. Replace original plate at position 6 with a new skirted plate')
    magdeck.engage()
    #sleep(300)
    pick_up_plate()
    [p300m.transfer(400, temp_plate.columns()[x], plate.columns()[x]) for x in range(0,12)]
    ctx.home()
