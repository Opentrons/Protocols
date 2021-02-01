metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}


def run(ctx):

    transfer_csv = get_values(  # noqa: F821
        "transfer_csv")

    tiprack = ctx.load_labware()


    # load labware
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]
    for line in transfer_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                ctx.load_labware(lw.lower(), slot)
