import math

metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [pipette_type, num_samples, m20_mount, p20_mount, tip_type,
     tip_reuse, transfer_csv, mm_vol] = get_values(  # noqa: F821
        'pipette_type', 'num_samples', 'm20_mount', 'p20_mount' 'tip_type',
        'tip_reuse', 'transfer_csv', 'mm_vol')

    # load labware
    mm = ctx.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul'
                          '6', 'mastermix tubes (strip column 1)').wells()[0]
    source_plates = [
        ctx.load_labware('amplifyt_96_wellplate_200ul', slot, f'plate f{i+1}')
        for i, slot in enumerate(['11', '8', '5', '2'])
    ]
    tips20m = [ctx.load_labware('opentrons_96_tiprack_20ul', '3')]
    tips20s = [ctx.load_labware('opentrons_96_tiprack_20ul', '7')]
    dest_plate = ctx.load_labware('amplifyt_96_wellplate_200ul', '9',
                                  'destination plate')
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]
    for line in transfer_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                ctx.load_labware(lw.lower(), slot)

    # load pipette
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tips20s)
    m20 = ctx.load_instrument('p20_multi_gen2', m20_mount, tip_racks=tips20m)

    def parse_well(well):
        letter = well[0]
        number = well[1:]
        return letter.upper() + str(int(number))

    # pre-transfer mastermix with P20-multi
    mm_dests = dest_plate.rows()[0][:math.ceil(num_samples/8)]
    m20.pick_up_tip()
    for d in mm_dests:
        m20.transfer(mm_vol, mm, d.bottom(2), new_tip='never')
    m20.drop_tip()

    for line in transfer_info:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        source = ctx.loaded_labwares[
            int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = ctx.loaded_labwares[
            int(d_slot)].wells_by_name()[parse_well(d_well)]
        pick_up()
        pip.transfer(float(vol), source, dest, new_tip='never')
        pip.drop_tip()
    if pip.hw_pipette['has_tip']:
        pip.drop_tip()
