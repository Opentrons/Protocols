metadata = {
    'protocolName': 'PCR Preparation Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}


def run(ctx):

    [mm_lw, mm_slot, mm_vol, dna_vol, transfer_csv,
     p20_mount] = get_values(  # noqa: F821
        'mm_lw', 'mm_slot', 'mm_vol', 'dna_vol', 'transfer_csv', 'p20_mount')

    # load labware
    mm = ctx.load_labware(mm_lw, mm_slot, 'mastermix container').rows()[0]

    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]

    def parse_well(well):
        return well[0].upper() + str(int(well[1:]))

    # parse csv file
    lw_map = {
        '96': 'greinerbioone_96_wellplate_200ul',
        '384': 'sarstedt_384_wellplate_40ul'
    }
    transfer_dict = {}
    for line in transfer_info:
        s_slot, s_well, d_lw, d_slot, d_well = line[:5]
        if int(s_slot) not in ctx.loaded_labwares:
            ctx.load_labware(lw_map['96'], s_slot)
        if int(d_slot) not in ctx.loaded_labwares:
            ctx.load_labware(lw_map[d_lw], d_slot)
        source = ctx.loaded_labwares[int(s_slot)].wells_by_name()[
            parse_well(s_well)]
        dest = ctx.loaded_labwares[int(d_slot)].wells_by_name()[
            parse_well(d_well)]
        if source not in transfer_dict:
            transfer_dict[source] = [dest]
        else:
            transfer_dict[source].append(dest)

    # load tipracks in remaining slots
    tipracks = []
    for slot in range(1, 13):
        if slot not in ctx.loaded_labwares:
            tipracks.append(
                ctx.load_labware('opentrons_96_tiprack_20ul', str(slot)))

    # load pipette
    m20 = ctx.load_instrument('p20_multi_gen2', p20_mount, tip_racks=tipracks)

    tip_count = 0
    tip_max = len(tipracks*96)

    def pick_up():
        nonlocal tip_count
        if tip_count == tip_max:
            ctx.pause('Please refill tipracks before resuming.')
            m20.reset_tipracks()
            tip_count = 0
        m20.pick_up_tip()
        tip_count += 1

    # transfer mastermix
    all_dests = [d for dest_set in transfer_dict.values() for d in dest_set]
    pick_up()
    dests_per_col = mm[0].max_volume//mm_vol
    print(dests_per_col)
    for i, d in enumerate(all_dests):
        m20.air_gap(2)
        m20.aspirate(mm_vol, mm[i//dests_per_col])
        m20.dispense(2+mm_vol, d)
    m20.drop_tip()

    # transfer sample
    for source, dests in transfer_dict.items():
        pick_up()
        for d in dests:
            m20.air_gap(2)
            m20.aspirate(dna_vol, source)
            m20.dispense(2+dna_vol, dest.bottom(1))
        m20.drop_tip()
