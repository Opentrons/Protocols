import os
import csv

metadata = {
    'protocolName': 'Diluting DNA with TE, Using .csv File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"tip_track":false, "csv_samp":"Well,initial conc (ng/μL),initial volume (μL),final conc (ng/μL),volume final,volume to add (μL),Name,Pipette\\nA7,613,30,250,73.56,44,3 645 349,P100\\nB7,790.4,30,250,94.848,65,3 645 356,P100\\nC7,682,30,250,81.84,52,3645363,P100\\nD7,255.8,30,250,30.696,1,3645372,No dilution\\nE7,2276,15,250,136.56,122,364c,P200\\nA8,593,30,250,71.16,41,3246294,P100\\nB8,1862,25,250,186.2,161,324c,P200\\nC8,1131,30,250,135.72,106,4441174,P200\\nD8,2271,15,250,136.26,121,444c,P200\\nE8,2895,10,250,115.8,106,281c,P200\\nF8,181.7,30,250,-1,-1,3546284,No dilution\\nG8,2370,15,250,142.2,127,354c,P200\\nH8,780.6,30,250,93.672,64,3095338,P100\\nA9,1819,10,100,181.9,172,4378,P200\\nB9,2954,5,100,147.7,143,R1105 08/22B dry,P200\\nC9,506.1,30,250,60.732,31,3411184,P100\\nD9,510.5,30,250,61.26,31,437001-005,P100\\nE9,483.1,30,250,57.972,28,445001-005,P100\\nF9,698.5,30,250,83.82,54,BRW-342,P100\\nG9,1119,30,250,134.28,104,355c,P200\\nH9,690.9,30,250,82.908,53,413c,P100\\nA10,3125,5,100,156.25,151,R1098 02/22 dry,P200\\nB10,1494,10,100,149.4,139,R1098 03/22 dry,P200\\nC10,2056,5,100,102.8,98,R1105 09/22A dry,P100\\nD10,2319,5,100,115.95,111,R1124 03/22B dry,P200\\nE10,1640,10,100,164,154,Bashani I 17-09-20,P200\\nF10,574.1,25,100,143.525,119,R1105 09/22A dry,P200\\nG10,568.9,25,100,142.225,117,R1105 09/22A,P200\\nH10,660.2,25,100,165.05,140,R1124 06/22A,P200\\nA11,826.5,20,100,165.3,145,R1124 03/22B,P200\\nB11,1289,10,100,128.9,119,R1098 02/22,P200\\nC11,274.6,30,100,82.38,52,R1105 08/22B,P100\\nD11,490.8,25,100,122.7,98,R1098 03/22,P100\\nE11,1566,10,100,156.6,147,LBCC 0417 c1,P200\\nF11,1103,10,100,110.3,100,LBCC 0417 c2,P200\\nG11,1434,10,100,143.4,133,LBCC 0417 mix,P200\\nH11,261.8,30,100,78.54,49,LBCC 0413 c1,P100\\nA12,78.11,30,100,23.433,-1,LBCC 1046 mix,No dilution\\nB12,302.3,30,100,90.69,61,LBCC 0422 c2,P100\\nC12,87.13,30,100,26.139,-1,LBCC 1046 c1,No dilution\\nD12,149.4,30,100,44.82,15,LBCC 0422 mix,P20\\nE12,29.27,30,100,8.781,-1,LBCC 1046 c2,No dilution\\nF12,194,30,100,58.2,28,LBCC 0422 c1,P100\\nG12,130.5,30,100,39.15,9,LBCC 0413 mix,P20\\nH12,87.02,30,100,26.106,-1,LBCC 0413 c2,No dilution\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n,,,,,,,\\n","dna_asp_rate":0.5,"p20_mount":"right","p300_mount":"left"}""")
    return [_all_values[n] for n in names]



def run(ctx):

    [csv_samp, dna_asp_rate, tip_track,
        p20_mount, p300_mount] = get_values(  # noqa: F821
        "csv_samp", "dna_asp_rate", "tip_track",
            "p20_mount", "p300_mount")

    # load Labware
    dna_plate = ctx.load_labware('kingfisher_96_wellplate_100ul', 1)
    final_plate = ctx.load_labware('starstedt_96_wellplate_200ul', 2)
    tuberack = ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 3)
    tipracks20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                  for slot in [4, 5]]
    tipracks300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
                   for slot in [7, 8]]

    # load instrument
    p20 = ctx.load_instrument("p20_single_gen2", p20_mount,
                              tip_racks=tipracks20)

    p300 = ctx.load_instrument("p300_single_gen2", p300_mount,
                               tip_racks=tipracks300)

    # Tip tracking between runs
    if not ctx.is_simulating():
        file_path = '/data/csv/tiptracking.csv'
        file_dir = os.path.dirname(file_path)
        # check for file directory
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # check for file; if not there, create initial tip count tracking
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as outfile:
                outfile.write("0, 0\n")

    tip_count_list = []
    if ctx.is_simulating():
        tip_count_list = [0, 0]
    else:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            tip_count_list = next(csv_reader)

    num_one = int(tip_count_list[0]) if tip_track else 0
    num_two = int(tip_count_list[1]) if tip_track else 0

    tips20 = [tip for rack in tipracks20 for tip in rack.wells()]
    tips300 = [tip for rack in tipracks300 for tip in rack.wells()]

    tipcount20 = num_one
    tipcount300 = num_two

    def pick_up20():
        nonlocal tipcount20

        if tipcount20 == 191:
            ctx.pause("Replace 20ul tip racks")
            tipcount20 = 0
            p20.pick_up_tip(tips20[0])
            tipcount20 += 1
        else:
            p20.pick_up_tip(tips20[tipcount20])
            tipcount20 += 1

    def pick_up300():
        nonlocal tipcount300

        if tipcount300 == 191:
            ctx.pause("Replace 300ul tip racks")
            tipcount300 = 0
            p300.pick_up_tip(tips300[tipcount300])
            tipcount300 += 1
        else:
            p300.pick_up_tip(tips300[tipcount300])
            tipcount300 += 1

    # mapping and parsing
    te = tuberack.wells()[0]
    csv_rows = [[val.strip() for val in line.split(',')]
                for line in csv_samp.splitlines()
                if line.split(',')[0].strip()][1:]

    num_samp = 0
    for row in csv_rows:

        if len(row[4]) == 0:
            break
        else:
            num_samp += 1
    csv_rows = csv_rows[:num_samp]

    for row in csv_rows:
        if float(row[4]) >= 180:
            raise Exception("Volume greater than 180ul TE in csv file")
    num_samp = len(csv_rows)

    # transferring TE
    ctx.comment('\n\n TRANSFERRING TE TO PLATE\n')
    for row in csv_rows:
        well = row[0]
        te_vol = float(row[4])
        pip = p20 if te_vol < 20 else p300
        if not pip.has_tip and pip == p20:
            pick_up20()
        elif not pip.has_tip and pip == p300:
            pick_up300()
        if te_vol > 0:
            pip.aspirate(te_vol, te.bottom(z=3))
            pip.dispense(te_vol, final_plate.wells_by_name()[well].bottom(z=3))
        else:
            continue
    if p20.has_tip:
        p20.drop_tip()

    if p300.has_tip:
        p300.drop_tip()

    ctx.comment('\n\n TRANSFERRING DNA TO PLATE\n')

    for row in csv_rows:

        dna_vol = float(row[2])
        well = row[0]
        te_vol = float(row[4])
        total_vol = te_vol + dna_vol
        pip = p20 if dna_vol < 20 else p300
        if not pip.has_tip and pip == p20:
            pick_up20()
        elif not pip.has_tip and pip == p300:
            pick_up300()
        pip.aspirate(dna_vol, dna_plate.wells_by_name()[well].bottom(z=3), rate=dna_asp_rate)  # noqa: E501
        pip.dispense(dna_vol, final_plate.wells_by_name()[well].bottom(z=3))
        if total_vol*0.8 > 20:
            if not p300.has_tip:
                p300.pick_up_tip()
                p300.mix(3, total_vol*0.8, final_plate.wells_by_name()[well].bottom(z=3))  # noqa: E501
                p300.drop_tip()
            else:
                p300.mix(3, total_vol*0.8, final_plate.wells_by_name()[well].bottom(z=3))  # noqa: E501
        else:
            pip.mix(3, total_vol*0.8, final_plate.wells_by_name()[well].bottom(z=3))  # noqa: E501
        pip.drop_tip()

    num_one = tipcount20
    num_two = tipcount300

    # write updated tipcount to CSV
    new_tip_count = str(num_one)+", "+str(num_two)+"\n"
    if not ctx.is_simulating():
        with open(file_path, 'w') as outfile:
            outfile.write(new_tip_count)
