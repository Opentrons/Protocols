metadata = {
    'protocolName': 'PCB Board Plating',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [p20_mount, samples, volume, trough_type] = get_values(  # noqa: F821
        "p20_mount", "samples", "volume", "trough_type")

    volume = float(volume)
    trough_type = int(trough_type)

    troughs = {1: "agilent_1_reservoir_290ml", 2: "axygen_1_reservoir_90ml",
               3: "nest_12_reservoir_15ml", 4: "nest_1_reservoir_195ml",
               5: "usascientific_12_reservoir_22ml"}

    # Load Labware
    pcb = ctx.load_labware('pcb_board_250_wells', 1)
    trough = ctx.load_labware(troughs[trough_type], 6, 'Tetrahydrofuran')['A1']
    tiprack = ctx.load_labware('opentrons_96_tiprack_20ul', 3)

    # Load Pipette
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                              tip_racks=[tiprack])

    # Transfer 10 uL to all wells
    p20.transfer(volume, trough, pcb.wells()[:samples], new_tip='once')
