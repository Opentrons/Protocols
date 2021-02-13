metadata = {
    'protocolName': 'PCB Board Plating',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    p20_mount = 'left'

    # Load Labware
    pcb = ctx.load_labware('pcb_board_250_wells', 1)
    trough = ctx.load_labware('nest_1_reservoir_195ml', 6, 'Tetrahydrofuran')['A1']
    tiprack = ctx.load_labware('opentrons_96_tiprack_20ul', 3)
    
    # Load Pipette
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=[tiprack])

    # Transfer 10 uL to all wells
    p20.transfer(10, trough, pcb.wells(), new_tip='once')
