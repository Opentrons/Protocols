metadata = {
    'apiLevel': '2.5',
    'protocolName': 'TG Nextera XT index kit v2 Set A to D',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

def run(ctx):

    sample_count = 96

    thermocycler = ctx.load_module('thermocycler')
    thermocycler.open_lid()
    thermocycler_plate = thermocycler.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt')

    temp_deck = ctx.load_module(
        'temperature module',  # Update to Gen2
        '1')
    temp_rack = temp_deck.load_labware(
        'opentrons_24_aluminumblock_generic_2ml_screwcap')
    phusion_mm = temp_rack.wells_by_name()["A1"]
    kapa_mm = temp_rack.wells_by_name()["B1"]
    north_indexing_primers = [temp_rack.wells_by_name()[x] for x in ["{}{}".format(b,a) for a in ["2","3"] for b in ["A","B","C","D"]]]
    south_indexing_primers = [temp_racks.wells_by_name()[x] for x in ["{}{}".format(b,a) for a in ["4","5","6"] for b in ["A","B","C","D"]]]

    mag_deck = ctx.load_module('magnetic module', '4')  # update to gen2
    mag_deck.disengage()
    mag_plate = magdeck.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    DNA_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '3')
    Primer_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '5')

    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '2')
    beads = reservoir.wells_by_name()["A1"]
    h2o = reservoir.wells_by_name()["A2"]

    etoh = 
    liquid_trash = 
    
    p20s =
    p300s = 

    dna_wells = DNA_plate.wells()[:sample_count]
    primer_wells = Primer_plate.wells()[:sample_count]
    mag_wells = mag_plate.wells()[:sample_count]
    thermo_wells = thermocycler_plate.wells()[:sample_count]

    # Genomic DNA amplification

    p300s.transfer(21, phusion_mm, thermocycler_plate.wells()[:sample_count], new_tip='once')
    p20s.transfer(2, dna_wells, thermo_wells, new_tip='always')
    p20s.transfer(2, primer_wells, thermo_wells, new_tip='always')

    def stp(temp, hold):
        return {"temperature": temp, "hold_time_seconds": hold}
    steps = []
    steps.append(stp(98, 300))
    steps += [item for sublist in [[stp(98,10), stp(69-x,10), stp(72,30)] for x in range(0,10)] for item in sublist]
    steps += [item for sublist in [[stp(98,10), stp(72,30)] for _ in range(0,25)] for item in sublist]
    steps.append(stp(72,420))
    steps.append(stp(10,10))


    thermocycler.close_lid()
    thermocycler.set_lid_temperature(99)
    thermocycler.execute_profile(
        steps=steps,
        repetitions=1, block_max_volume=25)
    thermocycler.open_lid()
    
    ctx.pause("Move thermocycler plate to magdeck. Replace DNA plate with indexing plate I. Replace thermocycler plate with reaction plate C")

    # PCR amplicons beads clean
    
    def wash():
        p300s.transfer(45, beads, mag_wells, mix_before=(100,5), mix_after=(50,15), new_tip='always')
        ctx.delay(300)
        mag_deck.engage()
        ctx.delay(600)

        p300s.transfer(200, mag_wells, liquid_trash, new_tip='always')
        for _ in range(0,2):
            # Protocol from customer did not include a sample resuspension
            # or a step for removing EtOH. I am doing what I assume it meant.
            p300s.transfer(150, etoh,  mag_wells, new_tip='always')
            p300s.transfer(150, mag_wells, liquid_trash, new_tip='always')
        p20s.transfer(10, mag_wells, liquid_trash, new_tip='always')

        ctx.delay(360)
        mag_deck.disengage()
        
        p300s.transfer(40, h2o, mag_wells, mix_after=(30,20), new_tip='always')
        ctx.delay(120)
        mag_deck.engage()
        ctx.delay(180)
        p300s.transfer(36, mag_wells, DNA_plate.wells()[:sample_count])
    wash()


    # Library indexing PCR KAPA
    
    p20s.tranfer(17.5, kapa_mm, thermo_wells)
    p20s.transfer(2.5, dna_wells, thermo_wells)
    # transfer north index
    # transfer south index

    steps = []
    steps.append(stp(95,30))
    steps += [item for sublist in [[stp(95,10), stp(55,30), stp(72,30)] for _ in range(0,12)] for item in sublist]
    steps.append(stp(72,300))
    steps.append(stp(4, 10))

    thermocycler.close_lid()
    thermocycler.set_lid_temperature(99)
    thermocycler.execute_profile(
        steps=steps,
        repetitions=1, block_max_volume=25)
    
    thermocycler.open_lid()
    ctx.pause("Move thermocycler plate to magdeck. Replace indexing I plate with output plate.")

    # Index library beads clean
    wash()
