

#Variable input idea as follows:
def get_values(*names):
    import json
    _all_values = json.loads("""{"final_vol":70,"pre_dilution":true,"pre_dil_factA": 2,"pre_dil_factB": 2,"pre_dil_factC": 2,"pre_dil_factD": 2,"serial_dil_factA": 2,
                              "serial_dil_factB": 2,"serial_dil_factC": 2,"serial_dil_factD": 2 }""")
    return[_all_values[n]for n in names]


from opentrons import protocol_api
metadata = {
    'protocolName': 'Combo IC',
    'author': 'Abel.Tesfaslassie@opentrons.com',
    'description': 'Sterile Workflows',
    'apiLevel': '2.11'
}
def run(ctx):


    [final_vol, pre_dilution, pre_dil_factA, pre_dil_factB, pre_dil_factC, pre_dil_factD, serial_dil_factA, serial_dil_factB, serial_dil_factC, serial_dil_factD]= get_values    
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
    
    mix_reps = 4

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

  #Procedure Step:  
    #1
    destination1 = [well for col in [vsp.columns()[c] for c in [0,11]] for well in col[1:]]
    p300.pick_up_tip()
    for d in destination1:
          p300.transfer(vol1, dmso_res.well()['A1'], destination1, new_tip='never')
    p300.return_tip()
    
    # 2
    destination2 = [well for row in [hsp.rows()[c] for c in [0,7]] for well in row[1:]]
    p300.pick_up_tip()
    for d in destination2:
      p300.transfer(vol2, dmso_res.well()['A1'], destination2, new_tip='never')
    p300.drop_tip()

    # 3
    pip = p20 if vol3 <= 20 else p300

    pip.pick_up_tip()
    pip.transfer(vol3, dmso_res['A1'], vsp['A2'], new_tip='never')

    pip = p20 if vol4 <= 20 else p300
    if not pip.has_tip:
        pip.pick_up_tip()

    pip.transfer(vol4, dmso_res['A1'], vsp['A11'], new_tip='never')
    for pip in [p20, p300]:
         if pip.has_tip:
              pip.drop_tip()
    
    # 4
    pip = p20 if vol5 <=20 else p300
    if not pip.has_tip:
        pip.pick_up_tip()
        pip.transfer(vol5, dmso_res['A1'],hsp['B1'], new_tip='never')

    pip = p20 if vol6 <=20 else p300
    if not pip.has_tip:
        pip.pick_up_tip()
        pip.transfer(vol6, dmso_res['A1', hsp['G1']], new_tip='never')
    for pip in [p20, p300]:
         if pip.has_tip:
              pip.drop_tip()


    #5
    pip = p20 if vol7 <= 20 else p300

    pip.pick_up_tip()
    pip.transfer(vol7, compound_plate['B1'], vsp['A2'], new_tip='once')
    pip.drop_tip()

    pip = p20 if vol8 <= 20 else p300
    pip.pick_up_tip()
    pip.transfer(vol8, dmso_res['B2'], vsp['A11'], new_tip='once')
    pip.drop_tip()

    #6
    pip = p20 if vol9 <= 20 else p300

    pip.pick_up_tip()
    pip.transfer(vol9, compound_plate['A1'], hsp['B1'], new_tip='once')
    pip.drop_tip()

    pip = p20 if vol10 <= 20 else p300
    pip.pick_up_tip()
    pip.transfer(vol10, compound_plate['A2'], hsp['G1'], new_tip='once')
    pip.drop_tip()

#7 thru 9 ------will need to setup predilution input variable in field.json
    p300.pick_up_tip()
    if predilution:
        pip.transfer(vol11,vsp["A2"],vsp["A1"],new_tip='once')
        p300.mix(5,100,vsp["A1"])
    else:
        pip.transfer(vol11,compound_plate["B1"],vsp["A1"],new_tip='once')
        p300.mix(5,100,vsp["A1"])
    p300.drop_tip()

#Serial Dilution across row A of hsp plate
# might need to use zip feature to use source# & destination#
source3= [well for row in [vsp.row()[i] for i in [0:6] for well in col[0]]]
destination3= [well for row in [vsp.row()[c] for c in [1:6]] for well in col[0]]
p300.pick_up_tip()
    for i in source3:
        p300.transfer(vol12,source3,destination3, new_tip='never')
        p300.mix(5,100,destination3)
p300.drop_tip()
    
#10 thru 12 ------will need to setup predilution input variable in field.json
    p300.pick_up_tip()
    if predilution:
        pip.transfer(vol13,vsp["A11"],vsp["A12"],new_tip='once')
        p300.mix(5,100,vsp["A12"])
    else:
        pip.transfer(vol13,compound_plate["B2"],vsp["A12"],new_tip='once')
        p300.mix(5,100,vsp["A12"])
    p300.drop_tip()

#Serial Dilution across row A of hsp plate
# might need to use zip feature to use source# & destination#
source4= [well for row in [vsp.row()[i] for i in [0:6] for well in col[11]]]
destination4= [well for row in [vsp.row()[c] for c in [1:6]] for well in col[11]]
p300.pick_up_tip()
    for i in source4:
        p300.transfer(vol14,source4,destination4, new_tip='never')
        p300.mix(5,100,destination4)
p300.drop_tip()


#13 thru 15 ------will need to setup predilution input variable in field.json
    p300.pick_up_tip()
    if predilution:
        pip.transfer(vol15,hsp["B1"],vsp["A1"],new_tip='once')
        p300.mix(5,100,hsp["A1"])
    else:
        pip.transfer(vol15,compound_plate["A1"],hsp["A1"],new_tip='once')
        p300.mix(5,100,hsp["A1"])
    p300.drop_tip()

#Serial Dilution across row A of hsp plate
# might need to use zip feature to use source# & destination#
source5= [well for col in [hsp.columns()[i] for i in [0:11] for well in row [0]]]
destination5= [well for col in [hsp.columns()[c] for c in [1:12]] for well in row [0]]
p300.pick_up_tip()
    for i in source5:
        p300.transfer(vol16,source4,destination4, new_tip='never')
        p300.mix(5,100,destination4)
p300.drop_tip()


#16-18 ------will need to setup predilution input variable in field.json
    p300.pick_up_tip()
    if predilution:
        pip.transfer(vol17,hsp["B1"],vsp["A1"],new_tip='once')
        p300.mix(5,100,hsp["A1"])
    else:
        pip.transfer(vol17,compound_plate["A1"],hsp["A1"],new_tip='once')
        p300.mix(5,100,hsp["A1"])
    p300.drop_tip()

#Serial Dilution across row A of hsp plate
# might need to use zip feature to use source# & destination#
source5= [well for col in [hsp.columns()[i] for i in [0:11] for well in row [0]]]
destination5= [well for col in [hsp.columns()[c] for c in [1:12]] for well in row [0]]
p300.pick_up_tip()
    for i in source5:
        p300.transfer(vol18,source4,destination4, new_tip='never')
        p300.mix(5,100,destination4)
p300.drop_tip()

















