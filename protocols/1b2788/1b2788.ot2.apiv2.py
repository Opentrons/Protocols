from opentrons.types import Point

metadata = {
    'protocolName': 'Zymo Quick-DNA Fecal/Soil Microbe 96 Magbead Kit',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_col, prewash_buff_vol,
        gdna_buff_vol, m300_mount] = get_values(  # noqa: F821
        "num_col", "prewash_buff_vol",
            "gdna_buff_vol", "m300_mount")

    if not 1 <= num_col <= 12:
        raise Exception("Enter a column number 1-12")

    prewash_buff_vol = int(prewash_buff_vol)
    gdna_buff_vol = int(gdna_buff_vol)

    # load module
    mag_mod = ctx.load_module('magnetic module gen2', 10)
    mag_plate = mag_mod.load_labware('zymo_96_wellplate_1200ul')

    # load labware
    reag_res = ctx.load_labware('nest_12_reservoir_15ml', 1)
    tipracks = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                for slot in [2, 4, 5, 7, 8, 9]]
    elute_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 3)
    elute_buff = ctx.load_labware('nest_12_reservoir_15ml', 6)
    waste_res = ctx.load_labware('nest_1_reservoir_195ml', 11)

    # pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', m300_mount,
                               tip_racks=tipracks)

    # mapping
    waste = waste_res.wells()[0]
    bind_buff = reag_res.wells()[:3]
    bind_beads = reag_res.wells()[3]
    prewash_buff = reag_res.wells()[4:6]
    gdna_wash_buff = reag_res.wells()[6:10]
    samples = mag_plate.rows()[0][:num_col]

    def pick_up_on_slot(slot):
        m300.starting_tip = ctx.loaded_labwares[slot].well('A1')
        m300.pick_up_tip()

    ctx.comment('\n\nDISPENSING 600ul BINDING BUFFER TO SAMPLES\n')
    pick_up_on_slot(4)
    for source_trough, col in zip(bind_buff*num_col, samples*3):
        m300.aspirate(200, source_trough)
        m300.dispense(200, col.top())
        m300.blow_out()

    ctx.comment('\n\nADDING BEADS TO SAMPLES\n')
    airgap = 10
    m300.mix(10, 50, bind_beads)
    for col in samples:
        m300.aspirate(25, bind_beads)
        m300.air_gap(airgap)
        m300.dispense(25+airgap, col.top())
        m300.blow_out()
    m300.drop_tip()

    ctx.pause('''
    Seal plate and place on rotator. Rotate at low speed for 10 minutes.
    Spin-down plate, unseal, and place back on mag deck.
    Select "Resume" in the Opentrons app to continue.
    ''')

    mag_mod.engage(height_from_base=6.7)
    ctx.delay(minutes=2)

    ctx.comment('\n\nREMOVING SUPERNATANT\n')
    for index, s_col in enumerate(samples):
        side = -1 if index % 2 == 0 else 1
        pick_up_on_slot(7)
        aspirate_loc = s_col.bottom(z=1).move(
                Point(x=(s_col.diameter/2-2)*side))

        for _ in range(5):
            m300.aspirate(166, aspirate_loc, rate=0.33)
            m300.touch_tip()
            m300.dispense(166, waste)
            m300.blow_out()
            m300.touch_tip()
        m300.drop_tip()

    mag_mod.disengage()

    ctx.comment('\n\nDISPENSING PRE-WASH BUFFER TO SAMPLES\n')
    pick_up_on_slot(5)
    for source_trough, col in zip(prewash_buff*num_col, samples):
        m300.transfer(prewash_buff_vol,
                      source_trough,
                      col.top(),
                      blow_out=True,
                      blowout_location='destination well',
                      new_tip='never')
    mag_mod.engage(height_from_base=6.7)
    ctx.delay(minutes=2)

    ctx.comment('\n\nREMOVING SUPERNATANT\n')
    for index, s_col in enumerate(samples):
        side = -1 if index % 2 == 0 else 1
        if not m300.has_tip:
            pick_up_on_slot(5)
        aspirate_loc = s_col.bottom(z=1).move(
                Point(x=(s_col.diameter/2-2)*side))

        for _ in range(2):
            m300.aspirate(150, aspirate_loc, rate=0.33)
            m300.touch_tip()
            m300.dispense(150, waste)
            m300.blow_out()
            m300.touch_tip()
        m300.drop_tip(ctx.loaded_labwares[8].rows()[0][index])

    mag_mod.disengage()

    for i in range(2):
        ctx.comment('\n\nDISPENSING gDNA BUFFER TO SAMPLES\n')
        pick_up_on_slot(4)
        for source_trough, col in zip(gdna_wash_buff*num_col, samples):
            m300.transfer(gdna_buff_vol,
                          source_trough,
                          col.top(),
                          blow_out=True,
                          blowout_location='destination well',
                          new_tip='never')

        mag_mod.engage(height_from_base=6.7)
        ctx.delay(minutes=2)

        ctx.comment('\n\nREMOVING SUPERNATANT\n')
        for index, s_col in enumerate(samples):
            side = -1 if index % 2 == 0 else 1
            if not m300.has_tip:
                pick_up_on_slot(8)
            aspirate_loc = s_col.bottom(z=1).move(
                    Point(x=(s_col.diameter/2-2)*side))

            for _ in range(2):
                m300.aspirate(150, aspirate_loc, rate=0.33)
                m300.touch_tip()
                m300.dispense(150, waste)
                m300.blow_out()
                m300.touch_tip()
            if i == 0:
                m300.drop_tip(ctx.loaded_labwares[8].rows()[0][index])
            else:
                m300.drop_tip()
        if i == 0:
            mag_mod.disengage()

    tips = []
    for tiprack in tipracks:
        for col in tiprack.rows()[0]:
            if col.has_tip:
                tips.append(col)

    ctx.delay(minutes=30)
    ctx.pause("""Drying for 30 minutes complete.
                 Select Resume on the Opentrons app to continue""")

    ctx.comment('\n\nADDING ELUTION BUFER AND MIXING\n')
    for i, col in enumerate(samples):
        pick_up_on_slot(2)
        m300.aspirate(50, elute_buff.wells()[0])
        m300.air_gap(airgap)
        m300.dispense(50+airgap, col.bottom(z=2))
        m300.mix(25, 40, col)
        m300.blow_out()
        m300.touch_tip()
        m300.drop_tip(ctx.loaded_labwares[2].rows()[0][i])

    mag_mod.engage(height_from_base=6.7)
    ctx.delay(minutes=2)

    ctx.comment('\n\nCOLLECTING ELUTE\n')

    for index, (s_col, d_col) in enumerate(zip(samples,
                                               elute_plate.rows()[0])):
        side = -1 if index % 2 == 0 else 1
        m300.pick_up_tip(ctx.loaded_labwares[2].rows()[0][index])
        aspirate_loc = s_col.bottom(z=1).move(
                Point(x=(s_col.diameter/2-2)*side))
        m300.aspirate(50, aspirate_loc)
        m300.touch_tip()
        m300.dispense(50, d_col)
        m300.blow_out()
        m300.touch_tip()
        m300.drop_tip()
