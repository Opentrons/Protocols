metadata = {
    'protocolName': 'nCoV-2019 Lo Cost protocol',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [num_col, m20_mount, m300_mount] = get_values(  # noqa: F821
        "num_col", "m20_mount", "m300_mount")

    num_col = int(num_col)
    num_samp = num_col*8

    # load labware
    temp_mod = ctx.load_module('temperature module gen2', '10')
    temp_plate = temp_mod.load_labware(
                    'opentrons_96_aluminumblock_nest_wellplate_100ul')
    tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                  for slot in ['3', '8']]
    tiprack20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
                 for slot in ['9', '11']]
    amp_pt1 = ctx.load_labware(
                    'nest_96_wellplate_100ul_pcr_full_skirt', '4')
    amp_pt2 = ctx.load_labware(
                    'nest_96_wellplate_100ul_pcr_full_skirt', '5')
    final_plate = ctx.load_labware(
                    'nest_96_wellplate_100ul_pcr_full_skirt', '6')
    res = ctx.load_labware('nest_12_reservoir_15ml', '2')
    tuberack = ctx.load_labware(
                'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '1')

    # load instrument
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tiprack20)
    m300 = ctx.load_instrument('p300_multi_gen2',
                               m300_mount, tip_racks=tiprack300)

    num_channels_per_pickup = 1
    tips_ordered = [
        tip for rack in tiprack20
        for row in rack.rows()[
            len(rack.rows())-num_channels_per_pickup::
                            -1*num_channels_per_pickup]
        for tip in row]

    tip_count = 0

    def pick_up():
        nonlocal tip_count
        m20.pick_up_tip(tips_ordered[tip_count])
        tip_count += 1

    def create_chunks(list, n):
        for i in range(0, len(list), n):
            yield list[i:i+n]

    # load reagents
    water = res.wells()[0]
    end_prep_mmx = tuberack.rows()[0][0]
    barcode_mmx = tuberack.rows()[0][1]
    pool_tube = tuberack.rows()[0][5]

    # PROTOCOL
    ctx.comment('~~~~~~~~Adding Amp Product from Plate 1 to Plate 2~~~~~~~~~')
    for source, dest in zip(amp_pt1.rows()[0][:num_col], amp_pt2.rows()[0]):
        m300.pick_up_tip()
        m300.aspirate(25, source)
        m300.dispense(25, dest)
        m300.mix(10, 35, dest, rate=0.6)
        m300.touch_tip()
        m300.drop_tip()
    ctx.comment('\n\n\n\n')

    ctx.comment('~~~~~~~~Adding Water to Final Plate~~~~~~~~~')
    m300.pick_up_tip()
    m300.distribute(45,
                    water,
                    [col for col in final_plate.rows()[0][:num_col]],
                    new_tip='never')
    m300.drop_tip()
    ctx.comment('\n\n\n\n')

    ctx.comment('~~~~~~~~Adding Amp Product from Plate 2 to Water~~~~~~~~~')
    for source, dest in zip(amp_pt2.rows()[0][:num_col],
                            final_plate.rows()[0]):
        m20.pick_up_tip()
        m20.aspirate(5, source)
        m20.dispense(5, dest)
        m20.mix(20, 20, dest)
        m20.touch_tip()
        m20.return_tip()
    ctx.comment('\n\n\n\n')

    ctx.comment('~~~~~~~~Adding Mastermix to Temp Plate~~~~~~~~~')
    chunks = [temp_plate.wells()[i:i+2] for i in range(
                0, len(temp_plate.wells()[:num_samp]), 2)]
    pick_up()
    for chunk in chunks:
        m20.aspirate(15, end_prep_mmx)
        for well in chunk:
            m20.dispense(6.7, well)
        m20.dispense(1.6, end_prep_mmx)
    m20.drop_tip()
    ctx.comment('\n\n\n\n')

    ctx.comment('~~~~~~~~Adding Diluted PCR Product~~~~~~~~~')
    m20.reset_tipracks()
    for source, dest in zip(final_plate.rows()[0][:num_col],
                            temp_plate.rows()[0]):
        m20.pick_up_tip()
        m20.aspirate(3.3, source)
        m20.dispense(3.3, dest)
        m20.mix(10, 7.5, dest, rate=0.85)
        m20.blow_out(dest.top())
        m20.touch_tip()
        m20.drop_tip()
    ctx.comment('\n\n\n\n')

    ctx.delay(minutes=15, msg='INCUBATING AT ROOM TEMPERATURE')
    temp_mod.set_temperature(65)
    ctx.delay(minutes=15, msg='INCUBATING AT 65C')
    temp_mod.set_temperature(4)
    ctx.delay(minutes=1, msg='INCUBATING AT 4C')

    ctx.pause('''
    Incubation steps complete. Please take the 96 block off of the temperature
    module and replace it with the empty NEST PCR plate in Slot 4. Place a new
    NEST 100ul 96 well plate on the magnetic module, and then select "Resume"
    on the Opentrons App.
    ''')

    ctx.comment('~~~~~~~~Adding Barcode Mastermix~~~~~~~~~')
    pick_up()
    for chunk in chunks:
        m20.aspirate(18, barcode_mmx)
        for well in chunk:
            m20.dispense(7.75, well)
        m20.dispense(2.5, barcode_mmx)
    m20.drop_tip()
    ctx.comment('\n\n\n\n')

    ctx.pause('''
    Barcode mastermix is added to the plate. Remove the plate from the
    temperature module to add barcode, then put the plate back on the
    temperature module and select "Resume" on the Opentrons App.
    ''')

    # switch nomenclature for discarded plate and and prep plate
    end_prep_plate = amp_pt1
    ctx.comment('~~~~~~~~Adding Endprep Reaction and Mixing~~~~~~~~~')
    for source, dest in zip(end_prep_plate.rows()[0][:num_col],
                            final_plate.rows()[0]):
        m20.pick_up_tip()
        m20.aspirate(1, source, rate=0.5)
        m20.dispense(1, dest, rate=0.5)
        m20.mix(10, 7.5, dest)
        m20.touch_tip(radius=0.75, v_offset=-12)
        m20.drop_tip()

    ctx.delay(minutes=30, msg='INCUBATING AT ROOM TEMPERATURE')
    temp_mod.set_temperature(65)
    ctx.delay(minutes=10, msg='INCUBATING AT 65C')
    temp_mod.set_temperature(4)
    ctx.delay(minutes=1, msg='INCUBATING AT 4C')

    ctx.comment('~~~~~~~~Pooling Samples~~~~~~~~~')
    pick_up()
    for chunk in create_chunks(final_plate.wells()[:num_samp], 7):
        for well in chunk:
            m20.aspirate(2.5, well)
        m20.dispense(17.5, pool_tube)
        m20.blow_out()
    m20.drop_tip()
