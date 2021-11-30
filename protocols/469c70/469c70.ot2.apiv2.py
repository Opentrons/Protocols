metadata = {
    'protocolName': 'Serial Dilution of Analyte Stock',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{"csv":"Slot No,Position,Sample ID,Volume (mL),Slot No,Tube number,Sample ID\\n4,A1,Stock-1,0.25,1,A1,Int-1\\n3,Reservior,Diluent,11.75,1,A1,Int-1\\n1,A1,Int-1,1.2,1,A2,Int-2\\n3,Reservior,Diluent,8.8,1,A2,Int-2\\n1,A2,Int-2,1,1,A3,STD8\\n3,Reservior,Diluent,11,1,A3,STD8\\n1,A3,STD8,2.2,1,A4,STD7\\n3,Reservior,Diluent,7.8,1,A4,STD7\\n1,A4,STD7,2,1,A5,STD6\\n3,Reservior,Diluent,8,1,A5,STD6\\n1,A5,STD6,3.5,1,B1,STD5\\n3,Reservior,Diluent,6.5,1,B1,STD5\\n1,B1,STD5,4,1,B2,STD4\\n3,Reservior,Diluent,6,1,B2,STD4\\n1,B2,STD4,6.5,1,B3,STD3\\n3,Reservior,Diluent,3.5,1,B3,STD3\\n1,B3,STD3,3,1,B4,STD2\\n3,Reservior,Diluent,7,1,B4,STD2\\n1,B4,STD2,1.2,1,B5,STD1\\n3,Reservior,Diluent,8.8,1,B5,STD1\\n4,A2,Stock-2,0.3,2,A1,Int-1\\n3,Reservior,Diluent,9.7,2,A1,Int-1\\n2,A1,Int-1,2,2,A2,Int-2\\n3,Reservior,Diluent,8,2,A2,Int-2\\n2,A2,Int-2,1.5,2,A3,DQC\\n3,Reservior,Diluent,10.5,2,A3,DQC\\n2,A3,DQC,6.2,2,A4,HQC\\n3,Reservior,Diluent,3.8,2,A4,HQC\\n2,A4,HQC,3.5,2,A5,MQC\\n3,Reservior,Diluent,6.5,2,A5,MQC\\n2,A5,HQC,0.6,2,B1,LQC\\n3,Reservior,Diluent,9.4,2,B1,LQC\\n2,B1,HQC,1.2,2,B2,LLOQ QC\\n3,Reservior,Diluent,8.8,2,B2,LLOQ QC",
                                 "initial_vol_stock":230,
                                 "initial_vol_dilution":9770,
                                 "step_vol_stock":1200,
                                 "step_vol_dilution":8800,
                                  "mount":"right"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [csv, mount] = get_values(  # noqa: F821
        "csv", "mount")

    # load labware
    serial_rack1 = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '1',
                    label='SERIAL RACK 1')
    serial_rack2 = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '2',
                    label='SERIAL RACK 2')
    diluent_labware = ctx.load_labware('nest_1_reservoir_195ml', '3',
                                       label='DILUTION RESERVOIR')
    analyte_stock_rack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '4',
        label='STOCK RACK')

    tiprack = ctx.load_labware('opentrons_96_tiprack_1000ul', '6')

    # load instrument
    pip = ctx.load_instrument('p1000_single_gen2', mount, tip_racks=[tiprack])

    # protocol
    list_of_rows = [[val.strip() for val in line.split(',')]
                    for line in csv.splitlines()
                    if line.split(',')[0].strip()][1:]

    slot_num_source = 0
    tube_source = 1
    vol = 3
    slot_num_dest = 4
    tube_dest = 5
    all_labware = [serial_rack1,
                   serial_rack2,
                   diluent_labware,
                   analyte_stock_rack]

    for _ in list_of_rows:
        source = all_labware[int(_[slot_num_source])-1]
        dest = all_labware[int(_[slot_num_dest])-1]
        pip.pick_up_tip()
        pip.transfer(float(_[vol])*1000,
                     source.wells_by_name()[_[tube_source]
                     if int(_[slot_num_source]) != 3 else 'A1'],
                     dest.wells_by_name()[_[tube_dest]].top(),
                     new_tip='never',
                     blow_out=True,
                     blowout_location='destination well')
        if int(_[slot_num_source]) == 3:
            pip.mix(2, 0.6*float(_[vol])*1000
                    if 0.6*float(_[vol])*1000 < 1000 else 1000,
                    dest.wells_by_name()[_[tube_dest]].bottom(z=60))
        pip.drop_tip()
        ctx.comment('\n\n')
