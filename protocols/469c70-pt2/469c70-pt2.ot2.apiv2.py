from itertools import groupby

metadata = {
    'protocolName': 'Fresh Spiking with CSV',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"csv":"Slot No,Position,Sample ID,Volume (µL),Slot No,Tube number,Sample ID\\n3,A1,Blank Matrix,200,2,A1,Blk\\n3,A1,Blank Matrix,200,2,A2,Zero\\n3,A1,Blank Matrix,195,2,A3,STD1\\n3,A1,Blank Matrix,195,2,A4,STD2\\n3,A1,Blank Matrix,195,2,A5,STD3\\n3,A1,Blank Matrix,195,2,A6,STD4\\n3,A1,Blank Matrix,195,2,B1,STD5\\n3,A1,Blank Matrix,195,2,B2,STD6\\n3,A1,Blank Matrix,195,2,B3,STD7\\n3,A1,Blank Matrix,195,2,B4,STD8\\n3,A1,Blank Matrix,195,2,C1,DQC\\n3,A1,Blank Matrix,195,2,C2,DQC\\n3,A1,Blank Matrix,195,2,C3,DQC\\n3,A1,Blank Matrix,195,2,C4,DQC\\n3,A1,Blank Matrix,195,2,C5,DQC\\n3,A1,Blank Matrix,195,2,C6,DQC\\n3,A1,Blank Matrix,160,2,D1,DQC-5\\n3,A1,Blank Matrix,160,2,D2,DQC-5\\n3,A1,Blank Matrix,160,2,D3,DQC-5\\n3,A1,Blank Matrix,160,2,D4,DQC-5\\n3,A1,Blank Matrix,160,2,D5,DQC-5\\n3,A1,Blank Matrix,160,2,D6,DQC-5\\n3,A2,Blank Matrix,195,4,A1,HQC\\n3,A2,Blank Matrix,195,4,A2,HQC\\n3,A2,Blank Matrix,195,4,A3,HQC\\n3,A2,Blank Matrix,195,4,A4,HQC\\n3,A2,Blank Matrix,195,4,A5,HQC\\n3,A2,Blank Matrix,195,4,A6,HQC\\n3,A2,Blank Matrix,195,4,B1,MQC\\n3,A2,Blank Matrix,195,4,B2,MQC\\n3,A2,Blank Matrix,195,4,B3,MQC\\n3,A2,Blank Matrix,195,4,B4,MQC\\n3,A2,Blank Matrix,195,4,B5,MQC\\n3,A2,Blank Matrix,195,4,B6,MQC\\n3,A2,Blank Matrix,195,4,C1,LQC\\n3,A2,Blank Matrix,195,4,C2,LQC\\n3,A2,Blank Matrix,195,4,C3,LQC\\n3,A2,Blank Matrix,195,4,C4,LQC\\n3,A2,Blank Matrix,195,4,C5,LQC\\n3,A2,Blank Matrix,195,4,C6,LQC\\n3,A2,Blank Matrix,195,4,D1,LLOQ QC\\n3,A2,Blank Matrix,195,4,D2,LLOQ QC\\n3,A2,Blank Matrix,195,4,D3,LLOQ QC\\n3,A2,Blank Matrix,195,4,D4,LLOQ QC\\n3,A2,Blank Matrix,195,4,D5,LLOQ QC\\n3,A2,Blank Matrix,195,4,D6,LLOQ QC\\n1,A1,STD1,5,2,A3,STD1\\n1,A2,STD2,5,2,A4,STD2\\n1,A3,STD3,5,2,A5,STD3\\n1,A4,STD4,5,2,A6,STD4\\n1,A5,STD5,5,2,B1,STD5\\n1,A6,STD6,5,2,B2,STD6\\n1,B1,STD7,5,2,B3,STD7\\n1,B2,STD8,5,2,B4,STD8\\n1,D1,DQC,5,2,C1,DQC\\n1,D1,DQC,5,2,C2,DQC\\n1,D1,DQC,5,2,C3,DQC\\n1,D1,DQC,5,2,C4,DQC\\n1,D1,DQC,5,2,C5,DQC\\n1,D1,DQC,5,2,C6,DQC\\n2,C1,DQC,40,2,D1,DQC-5\\n2,C2,DQC,40,2,D2,DQC-5\\n2,C3,DQC,40,2,D3,DQC-5\\n2,C4,DQC,40,2,D4,DQC-5\\n2,C5,DQC,40,2,D5,DQC-5\\n2,C6,DQC,40,2,D6,DQC-5\\n1,D2,HQC,5,4,A1,HQC\\n1,D2,HQC,5,4,A2,HQC\\n1,D2,HQC,5,4,A3,HQC\\n1,D2,HQC,5,4,A4,HQC\\n1,D2,HQC,5,4,A5,HQC\\n1,D2,HQC,5,4,A6,HQC\\n1,D3,MQC,5,4,B1,MQC\\n1,D3,MQC,5,4,B2,MQC\\n1,D3,MQC,5,4,B3,MQC\\n1,D3,MQC,5,4,B4,MQC\\n1,D3,MQC,5,4,B5,MQC\\n1,D3,MQC,5,4,B6,MQC\\n1,D4,LQC,5,4,C1,LQC\\n1,D4,LQC,5,4,C2,LQC\\n1,D4,LQC,5,4,C3,LQC\\n1,D4,LQC,5,4,C4,LQC\\n1,D4,LQC,5,4,C5,LQC\\n1,D4,LQC,5,4,C6,LQC\\n1,D5,LLOQ QC,5,4,D1,LLOQ QC\\n1,D5,LLOQ QC,5,4,D2,LLOQ QC\\n1,D5,LLOQ QC,5,4,D3,LLOQ QC\\n1,D5,LLOQ QC,5,4,D4,LLOQ QC\\n1,D5,LLOQ QC,5,4,D5,LLOQ QC\\n1,D5,LLOQ QC,5,4,D6,LLOQ QC\\n2,C1,ISTD,5,2,A2,Zero\\n2,C1,ISTD,5,2,A3,STD1\\n2,C1,ISTD,5,2,A4,STD2\\n2,C1,ISTD,5,2,A5,STD3\\n2,C1,ISTD,5,2,A6,STD4\\n2,C1,ISTD,5,2,B1,STD5\\n2,C1,ISTD,5,2,B2,STD6\\n2,C1,ISTD,5,2,B3,STD7\\n2,C1,ISTD,5,2,B4,STD8\\n2,C1,ISTD,5,2,D1,DQC-5\\n2,C1,ISTD,5,2,D2,DQC-5\\n2,C1,ISTD,5,2,D3,DQC-5\\n2,C1,ISTD,5,2,D4,DQC-5\\n2,C1,ISTD,5,2,D5,DQC-5\\n2,C1,ISTD,5,2,D6,DQC-5\\n2,C1,ISTD,5,4,A1,HQC\\n2,C1,ISTD,5,4,A2,HQC\\n2,C1,ISTD,5,4,A3,HQC\\n2,C1,ISTD,5,4,A4,HQC\\n2,C1,ISTD,5,4,A5,HQC\\n2,C1,ISTD,5,4,A6,HQC\\n2,C1,ISTD,5,4,B1,MQC\\n2,C1,ISTD,5,4,B2,MQC\\n2,C1,ISTD,5,4,B3,MQC\\n2,C1,ISTD,5,4,B4,MQC\\n2,C1,ISTD,5,4,B5,MQC\\n2,C1,ISTD,5,4,B6,MQC\\n2,C1,ISTD,5,4,C1,LQC\\n2,C1,ISTD,5,4,C2,LQC\\n2,C1,ISTD,5,4,C3,LQC\\n2,C1,ISTD,5,4,C4,LQC\\n2,C1,ISTD,5,4,C5,LQC\\n2,C1,ISTD,5,4,C6,LQC\\n2,C1,ISTD,5,4,D1,LLOQ QC\\n2,C1,ISTD,5,4,D2,LLOQ QC\\n2,C1,ISTD,5,4,D3,LLOQ QC\\n2,C1,ISTD,5,4,D4,LLOQ QC\\n2,C1,ISTD,5,4,D5,LLOQ QC\\n2,C1,ISTD,5,4,D6,LLOQ QC", "p20_mount":"left", "p1000_mount": "right"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [csv, p20_mount, p1000_mount] = get_values(  # noqa: F821
        "csv", "p20_mount", "p1000_mount")

    # load labware
    final_rack1 = ctx.load_labware(
                    'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
                    '2',
                    label='FINAL RACK 1')
    final_rack2 = ctx.load_labware(
                    'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
                    '4',
                    label='FINAL RACK 2')

    matrix_rack = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '3',
                    label='MATRIX RACK')
    analyte_rack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', '1',
        label='ANALYTE RACK')

    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                 for slot in ['5']]
    tiprack1000 = [ctx.load_labware('opentrons_96_tiprack_1000ul', slot)
                   for slot in ['8']]
    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2',
                              p20_mount, tip_racks=tiprack20)
    p1000 = ctx.load_instrument('p1000_single_gen2',
                                p1000_mount, tip_racks=tiprack1000)

    # protocol
    list_of_rows = [[val.strip() for val in line.split(',')]
                    for line in csv.splitlines()
                    if line.split(',')[0].strip()][1:]

    slot_num_source = 0
    tube_source = 1
    vol = 3
    slot_num_dest = 4
    tube_dest = 5
    all_labware = [analyte_rack,
                   final_rack1,
                   matrix_rack,
                   final_rack2]

    dividers = []
    for row in list_of_rows:
        dividers.append(row[slot_num_source])

    # transfer target cell
    sections = [list(j) for i, j in groupby(dividers)]

    for i, _ in enumerate(list_of_rows[:len(sections[0])]):
        source = all_labware[int(_[slot_num_source])-1]
        source_well = _[tube_source]
        dest = all_labware[int(_[slot_num_dest])-1]
        dest_well = _[tube_dest]

        transfer_vol = float(_[vol])
        pip = p20 if transfer_vol < 100 else p1000
        if i == 0:
            pip.pick_up_tip()

        if pip.current_volume < transfer_vol-100:
            if pip.current_volume > 0:
                pip.dispense(pip.current_volume,
                             source.wells_by_name()[source_well])
            pip.aspirate(pip.max_volume, source.wells_by_name()[source_well])

        pip.dispense(transfer_vol, dest.wells_by_name()[dest_well].top())
        pip.blow_out()

        if i == len(sections[0])-1:
            pip.dispense(pip.current_volume,
                         source.wells_by_name()[source_well])
            pip.drop_tip()

    ctx.comment('\n\n\n')

    for _ in list_of_rows[len(sections[0]):]:
        source = all_labware[int(_[slot_num_source])-1]
        source_well = _[tube_source]
        dest = all_labware[int(_[slot_num_dest])-1]
        dest_well = _[tube_dest]
        transfer_vol = float(_[vol])
        pip = p20 if transfer_vol < 100 else p1000

        pip.pick_up_tip()
        pip.transfer(transfer_vol,
                     source.wells_by_name()[source_well],
                     dest.wells_by_name()[dest_well].top(),
                     new_tip='never',
                     mix_after=(2, 0.6*transfer_vol if 0.6*transfer_vol <
                                pip.max_volume else pip.max_volume),
                     blow_out=True,
                     blowout_location='destination well'
                     )

        pip.drop_tip()
