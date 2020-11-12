metadata = {
    'protocolName': 'Cherrypicking and Normalization',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.5'
}


def run(ctx):

    pipette_type, pipette_mount, d_csv, s_csv = get_values(  # noqa: F821
        "pipette_type", "pipette_mount", "d_csv", "s_csv")

    tiprack_map = {
        'p10_single': 'opentrons_96_filtertiprack_10ul',
        'p50_single': 'opentrons_96_filtertiprack_200ul',
        'p300_single_gen1': 'opentrons_96_filtertiprack_200ul',
        'p1000_single_gen1': 'opentrons_96_filtertiprack_1000ul',
        'p20_single_gen2': 'opentrons_96_filtertiprack_20ul',
        'p300_single_gen2': 'opentrons_96_filtertiprack_200ul',
        'p1000_single_gen2': 'opentrons_96_filtertiprack_1000ul'
    }

    # load labware
    transfer_info_d = [[val.strip().lower() for val in line.split(',')]
                       for line in d_csv.splitlines()
                       if line.split(',')[0].strip()][1:]

    transfer_info_s = [[val.strip().lower() for val in line.split(',')]
                       for line in s_csv.splitlines()
                       if line.split(',')[0].strip()][1:]

    for line in transfer_info_d:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                ctx.load_labware(lw.lower(), slot)

    for line in transfer_info_s:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                ctx.load_labware(lw.lower(), slot)

    # load tipracks in remaining slots
    tiprack_type = tiprack_map[pipette_type]
    tipracks = []
    for slot in range(1, 13):
        if slot not in ctx.loaded_labwares:
            tipracks.append(ctx.load_labware(tiprack_type, str(slot)))

    # load pipette
    pip = ctx.load_instrument(pipette_type, pipette_mount, tip_racks=tipracks)

    tip_count = 0
    tip_max = len(tipracks*96)

    def pick_up():
        nonlocal tip_count
        if tip_count == tip_max:
            ctx.pause('Please refill tipracks before resuming.')
            pip.reset_tipracks()
            tip_count = 0
        pip.pick_up_tip()
        tip_count += 1

    def parse_well(well):
        letter = well[0]
        number = well[1:]
        return letter.upper() + str(int(number))

    ctx.comment('Transferring dilutant to wells based on Dilutant CSV...')
    pick_up()
    for line in transfer_info_d:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        source = ctx.loaded_labwares[
            int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = ctx.loaded_labwares[
            int(d_slot)].wells_by_name()[parse_well(d_well)]
        pip.transfer(float(vol), source, dest, new_tip='never')
    pip.drop_tip()

    ctx.comment('Transferring DNA to wells based on Sample CSV...')
    for line in transfer_info_s:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        source = ctx.loaded_labwares[
            int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = ctx.loaded_labwares[
            int(d_slot)].wells_by_name()[parse_well(d_well)]
        pick_up()
        pip.transfer(float(vol), source, dest, new_tip='never')
        pip.mix(3, float(vol), dest)
        pip.blow_out()
        pip.drop_tip()

    ctx.comment('Protocol complete.')
