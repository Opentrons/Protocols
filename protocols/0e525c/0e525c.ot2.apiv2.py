from opentrons import protocol_api

metadata = {
    'protocolName': 'droplet digital PCR Prep',
    'author': 'Parrish Payne <parrish.payne@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}

    # Step 1 Transfer 180 uL from custom labware (Biorad semi-skirted 96-well Plate held in a ELISA PLATE) 
        # from source plate 1 col 1 to dest plate 1 col 1, col 2 to col 2 and so on up to col 7 of dest plate 1
    # Step 2 transfer 160 uL from Source 1 col 8 to destination plate 1 col 8
    # Step 3 transfer 20 uL from col 9 of source plate 1 to col 1 of destination plate 1, mix 20 times (step 4)
    # Step 5 transfer 20 uL from col 1 to col 2 of dest plate 1, mix 20 times drop tips
        # repeat 20 uL serial dilution from col 2 thru col 7 (new tips between each column.)
    #Step 6. transfer 40 uL from col 6 of dest plate 1 to col 8 of dest plate 1, mix col 8 (20 times, step 7) drop tips.

    # Not in original submission
    # On dest plate 2
    # step 8 Transfer 20 uL master mix from col 10 (and 11 as needed) of source plate 1 to dest plate 2 col 1-5.
    # step 9 Transfer 5 uL from col. 6 on dest 1 to col 1 on dest 2
    # step 10 Transfer 5 uL from col 7 on dest 1 to col 2 on dest 2
    # step 11 Transfer 5 uL from col 8 on dest 1 to col 3 on dest 2
    # step 12 transfer 5 uL (water) from col 12 on source plate 1 to col 4-5 on dest 2
    # new tips between each transfer

def run(ctx):

    # [m300_mount, m20_mount] = get_values(  # noqa: F821
    #     'm300_mount', 'm20_mount')
    
    m300_mount = 'right'
    m20_mount = 'left'
    
    # labware
    tips200 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in [1, 4]]
    tips20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', 7)]
    dest_plate_1 = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 3, 'Prep Plate')  
        # custom labware Biorad semi-skirted 96-well plate held in a ELISA plate
    dest_plate_2 = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 6, 'Final Plate')
        # custom labware Biorad semi-skirted 96-well plate held in a ELISA plate
    source_plate = ctx.load_labware('biorad_96_wellplate_200ul_pcr', 5, 'Reagent Plate')
        # custom labware Biorad semi-skirted 96-well plate held in a ELISA plate

   
    # pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount, tip_racks=tips200)
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tips20)

    # reagents
    dpbs = source_plate.rows()[0][:8]   # col. 1-8
    article = source_plate.rows()[0][8]  # col. 9
    mas_mix = source_plate.rows()[0][10]  # col. 11
    water = source_plate.rows()[0][11]  # col. 12  
    dpbs_destinations = dest_plate_1.rows()[0][:8]  # col. 1-8
    art_destinations = dest_plate_1.rows()[0][0]

    # Helper Functions
    def pick_up(pip):
        """Function that can be used instead of .pick_up_tip() that will pause
        robot when robot runs out of tips, prompting user to replace tips
        before resuming"""
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            pip.home()
            ctx.pause("Replace the tips")
            pip.reset_tipracks()
            pip.pick_up_tip()

    def slow_withdraw(pip, well, delay_seconds=1.0):
        pip.default_speed /= 16
        if delay_seconds > 0:
            ctx.delay(seconds=delay_seconds)
        pip.move_to(well.top())
        pip.default_speed *= 16

    # step 1
    for i, d in zip(dpbs, dpbs_destinations):
        pick_up(m300)
        m300.aspirate(180, i.bottom(1.0))
        m300.dispense(180, d.bottom(2))
        m300.drop_tip()
        
    # step 2
    pick_up(m300)
    m300.aspirate(160, source_plate.rows()[0][7].bottom(1))
    m300.dispense(160, dest_plate_1.rows()[0][7].bottom(2))
    m300.drop_tip()

    # step 3 & 4
    pick_up(m20)
    m20.aspirate(20, article.bottom(1.0))
    slow_withdraw(m20)
    m20.dispense(20, dest_plate_1.rows()[0][0].bottom(2.0))
    m20.mix(20, 200)
    slow_withdraw(m20)
    m20.drop_tip()

    # step 5 serial dilution
    for s, d in zip(dest_plate_1.rows()[0][:6], dest_plate_1.rows()[0][1:7]):
        pick_up(m20)
        m20.aspirate(20, s.bottom(1.0))
        m20.dispense(20, d.bottom(2.0))
        m20.mix(20, 200)
        slow_withdraw(m20, d)
        m20.drop_tip()
        m20.drop_tip()

    # step 6 & 7
    pick_up(m300)
    m300.aspirate(40, dest_plate_1.rows()[0][5]) # col 6
    slow_withdraw(m300, dest_plate_1.rows()[0][5])
    m300.dispense(40, dest_plate_1.rows()[0][7]) # col 8
    slow_withdraw(m300, dest_plate_1.rows()[0][7])
    m300.mix(20, 200)
    m300.drop_tip()

    # step 8 transfer 20 uL of mas_mix into col 1-5 of dest plate 2
    pick_up(m20)
    for d in dest_plate_2.rows()[0][:5]:
        m20.aspirate(20, mas_mix)
        slow_withdraw(m20, mas_mix)
        m20.dispense(20, d.bottom(2))
        slow_withdraw(m20, d)
    m20.drop_tip()

    # step 9, 10, 11 
    for s, d in zip(dest_plate_1.rows()[0][5:8], dest_plate_2.rows()[0][:3]):
        pick_up(m20)
        m20.aspirate(5, s)
        m20.dispense(5, d)
        slow_withdraw(m20, d)
        m20.drop_tip()

     # step 12
     for d in dest_plate_2.rows()[0][3:5]:
        pick_up(m20)
        m20.aspirate(5, water)
        m20.dispense(5, d.bottom(2))
        slow_withdraw(m20, d)
        m20.drop_tip()
