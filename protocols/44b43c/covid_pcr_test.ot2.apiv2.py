# metadata
metadata = {
    'protocolName': 'COVID-19 RT-PCR Setup',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}


def run(ctx):

    num_plates, num_cols, m300_mount, m20_mount = get_values(  # noqa: F821
        'num_plates', 'num_cols', 'm300_mount', 'm20_mount')

    # load labware
    deep_plates = [
        ctx.load_labware(
            'thermofisherdwplate_96_wellplate_2000ul',
            slot, 'PCR plate ' + str(i+1))
        for i, slot in enumerate(['2', '5', '8'])][:num_plates]
    pcr_plates = [
        ctx.load_labware(
            'thermofishermicroampfast96well0.1_96_wellplate_100ul',
            slot, 'PCR plate ' + str(i+1))
        for i, slot in enumerate(['3', '6', '9'])][:num_plates]
    tipracks20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in ['1', '4', '7']]
    tipracks300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in ['10']]
    reagent_plate = ctx.load_labware(
        'thermofisherdwplate_96_wellplate_2000ul', '11', 'reagent plate')

    # pipettes
    m300 = ctx.load_instrument('p300_multi', m300_mount, tip_racks=tipracks300)
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount,
                              tip_racks=tipracks20)

    m300.home()
    vol_mm = 20*1.1*num_cols*num_plates
    ctx.pause('Ensure ' + str(vol_mm) + 'µl of mastermix is in each well of \
column 1 in reagent plate (slot 11).')

    # sample and reagent setup
    mm = reagent_plate.rows()[0][0]
    ntc = reagent_plate.rows()[0][10]
    ptc = reagent_plate.rows()[0][11]

    # distribute mastermix
    for plate in pcr_plates:
        if num_cols % 2 == 0:
            dest_sets = [
                plate.rows()[0][i*2:i*2+2] for i in range(num_cols//2)]
        else:
            dest_sets = [
                plate.rows()[0][i*2:i*2+2] for i in range(num_cols//2)] + [
                    plate.rows()[0][num_cols-1:num_cols]]
        m300.pick_up_tip()
        for set in dest_sets:
            m300.aspirate(len(set)*20+5)
            m300.air_gap(10)
            for well in set:
                m300.dispense(20, well.bottom(3.5))
            m300.blow_out(mm.top(-2))
        m300.drop_tip()

    # transfer NTC
    m20.transfer(5, ntc.bottom(2),
                 [plate.rows()[0][0].bottom(2) for plate in pcr_plates])

    # transfer samples
    for s_plate, d_plate in zip(deep_plates, pcr_plates):
        for s, d in zip(s_plate.rows()[0][:num_cols],
                        d_plate.rows()[0][:num_cols]):
            m20.pick_up_tip()
            m20.transfer(5, s, d.bottom(2), new_tip='never')
            m20.air_gap(5)
            m20.drop_tip()

    # transfer PTC
    for plate in pcr_plates:
        m20.pick_up_tip()
        m20.transfer(5, ptc.bottom(2), plate.rows()[0][num_cols-1].bottom(2),
                     new_tip='never')
        m20.air_gap(5)
        m20.drop_tip()

    ctx.comment('PCR set up completed. Please remove PCR plates on blocks, \
seal, vortex and spin')
