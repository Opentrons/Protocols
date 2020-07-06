metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}


def run(ctx):

    pipette_type, pipette_mount, transfer_csv = get_values(  # noq: F821
        "pipette_type", "pipette_mount", "transfer_csv")

    tiprack_map = {
        'p10_single_gen1': 'opentrons_96_tiprack_10ul',
        'p50_single_gen1': 'opentrons_96_tiprack_300ul',
        'p300_single_gen1': 'opentrons_96_tiprack_300ul',
        'p1000_single_gen1': 'opentrons_96_tiprack_1000ul',
        'p20_single_gen2': 'opentrons_96_tiprack_20ul',
        'p300_single_gen2': 'opentrons_96_tiprack_3000ul',
        'p1000_single_gen2': 'opentrons_96_tiprack_1000ul'
    }

    # load labware
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in  transfer_csv.splitlines()]
    for line in transfer_info:
        s_slot, s_lw, d_slot, d_lw = line[:2] + line[3:4]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                ctx.load_labware(lw.lower(), slot)

    # load tipracks in remaining slots
    tiprack_type = tiprack_map[pipette_type]
    tipracks = []
    for slot in range(1, 13):
        if slot not in ctx.loaded_labwares:
            tiprack.append(ctx.load_labware(tiprack_type, str(slot)))

    # load pipette
    pip = ctx.load_instrument(pipette_type, pipette_mount, tip_racks=tipracks)

    tip_count = 0
    tip_max = len(tip_racks*96)

    def pick_up():
        nonlocal tip_count
        if tip_count == tip_max:
            ctx.pause('Please refill tipracks before resuming.')
            pip.reset_tipracks()
            tip_count = 0
        pip.pick_up_tip()
        tip_count += 1

    for line in transfer_info:
        s_lw, _, s_well, _, d_slot, d_well, vol = line[:7]
        source = ctx.loaded_labwares[int(s_slot)].wells_by_name(s_well.upper())
        dest = ctx.loaded_labwares[int(d_slot)].wells_by_name(d_slot.upper())
        pick_up()
        pip.transfer(vol, source, dest, new_tip='never')
        pip.drop_tip()
