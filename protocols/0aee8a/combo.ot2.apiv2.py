

#Variable input idea as follows:
def get_values(*names):
    import json
    _all_values = json.loads("""{final_vol":,"compA_vol_init":,"compB_vol_init":,"compC_vol_init":,"compD_vol_init":,
                              "pre_dil_factA":,"pre_dil_factB":,"pre_dil_factC":,"pre_dil_factD":, "serial_dil_factA":,
                              "serial_dil_factB":,"serial_dil_factC":,"serial_dil_factD": }""")
    return[_all_values[n]for n in names]


from opentrons import protocol_api
metadata = {
    'protocolName': 'Combo IC',
    'author': 'Abel.Tesfaslassie@opentrons.com',
    'description': 'Sterile Workflows',
    'apiLevel': '2.11'
}
def run(ctx):
    # Labware setup:

    #Reagent Resevoir
    dmso_res = ctx.load_labware('nest_12_reservoir_15ml', '1')
    #Tips
    p20_tip_rack = ctx.load_labware('opentrons_96_filtertiprack_20ul', '3')
    p200_tip_rack = ctx.load_labware('opentrons_96_filtertiprack_200ul', '6')
    #Plates
    compound_plate = ctx.load_labware('nest_96_wellplate_100ul', '2')
    hdpf1 = ctx.load_labware('nest_96_wellplate_100ul', '4')
    hdpf2 = ctx.load_labware('nest_96_wellplate_100ul', '5')
    vsp = ctx.load_labware('nest_96_wellplate_2ml_deep', '7')
    hsp = ctx.load_labware('nest_96_wellplate_2ml_deep', '8')
    vdpf1 = ctx.load_labware('nest_96_wellplate_100ul', '10')
    vdpf2 = ctx.load_labware('nest_96_wellplate_100ul', '11')
    
    # Pipette setup
    p20 = ctx.load_instrument('p20_single_gen2', 'left', tip_racks=[p20_tip_rack])
    p300 = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=[p200_tip_rack])

    #volume Definitiions:
    vol19= final_vol
    vol1 = vol19 * 12 * 1.1
    vol2 = vol19 * 8 * 1.1
    vol3 = vol11 - vol7
    vol4 = vol13 - vol8
    vol5 = vol15 - vol9
    vol6 = vol17 - vol10
    vol7 = vol11 / pre_dil_factC
    vol8 = vol13 / pre_dil_factD
    vol9 = vol15 / pre_dil_factA
    vol10 = vol17 / pre_dil_factB
    vol11 = vol12 + vol1
    vol12 = vol1 / (-1 + serial_dil_factC)
    vol13 = vol14 + vol1
    vol14 = vol1 / (-1 + serial_dil_factD)
    vol15 = vol16 + vol2
    vol16 = vol2 / (-1 + serial_dil_factA)
    vol17 = vol18 + vol2
    vol18 = vol2 / (-1 + serial_dil_factB)

    #1
    p300.pick_up_tip()
    destination = []
