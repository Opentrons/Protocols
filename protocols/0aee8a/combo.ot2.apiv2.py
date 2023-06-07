from opentrons import protocol_api
metadata = {
    'protocolName': 'Combo IC',
    'author': 'Abel.Tesfaslassie@opentrons.com',
    'description': 'Sterile Workflows',
    'apiLevel': '2.11'
}
def run(ctx):
    # Labware setup
    dmso_res = ctx.load_labware('nest_12_reservoir_15ml', '1')
    compound_plate = ctx.load_labware('nest_96_wellplate_100ul', '2')
    p20_tip_rack = ctx.load_labware('opentrons_96_filtertiprack_20ul', '3')
    hdpf1 = ctx.load_labware('nest_96_wellplate_100ul', '4')
    hdpf2 = ctx.load_labware('nest_96_wellplate_100ul', '5')
    p200_tip_rack = ctx.load_labware('opentrons_96_filtertiprack_200ul', '6')
    vsp = ctx.load_labware('nest_96_wellplate_2ml_deep', '7')
    hsp = ctx.load_labware('nest_96_wellplate_2ml_deep', '8')
    vdpf1 = ctx.load_labware('nest_96_wellplate_100ul', '10')
    vdpf2 = ctx.load_labware('nest_96_wellplate_100ul', '11')
    # Pipette setup
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[p20_tip_rack])
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p200_tip_rack])