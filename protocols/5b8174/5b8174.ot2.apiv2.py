metadata = {
    'protocolName': 'Custom Cherrypicking PCR Prep',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.10'
}


def run(ctx):

    [p20_mount, ctrl_csv, assembly_csv, ctrl_transfer_vol,
        assembly_transfer_vol] = get_values(  # noqa: F821
        "p20_mount", "ctrl_csv", "assembly_csv", "ctrl_transfer_vol",
        "assembly_transfer_vol")

    # Load Labware
    temp_mod = ctx.load_module('temperature module gen2', 6)
    tiprack_20ul = [ctx.load_labware('opentrons_96_tiprack_20ul', slot) for
                    slot in range(8, 12)]

    # Load Pipette
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=tiprack_20ul)

    ctrl_info = [[val.strip().lower() for val in line.split(',')] for line in
                 ctrl_csv.splitlines() if line.split(',')[0].strip()][6:]

    assembly_info = [[val.strip().lower() for val in line.split(',')] for line
                     in assembly_csv.splitlines() if
                     line.split(',')[0].strip()][6:]

    # Load Control Labware
    for line in ctrl_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[3:5]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                if int(slot) == 6:
                    temp_mod.load_labware(lw.lower())
                else:
                    ctx.load_labware(lw.lower(), slot)

    # Load Assembly Labware
    for line in assembly_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[3:5]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                if int(slot) == 6:
                    temp_mod.load_labware(lw.lower())
                else:
                    ctx.load_labware(lw.lower(), slot)

    # Load Protocol Steps

    # Step 1: Control
    for line in ctrl_info:
        s_slot, s_well, d_slot, d_well = line[1:3] + line[4:6]
        p20.transfer(ctrl_transfer_vol, ctx.loaded_labwares[int(s_slot)][
                          s_well.upper()].bottom(0.5),
                     ctx.loaded_labwares[int(d_slot)][d_well.upper()])

    # Step 2: Assembly
    for line in assembly_info:
        s_slot, s_well, d_slot, d_well = line[1:3] + line[4:6]
        p20.transfer(assembly_transfer_vol, ctx.loaded_labwares[int(s_slot)][
                          s_well.upper()].bottom(0.5),
                     ctx.loaded_labwares[int(d_slot)][d_well.upper()])
