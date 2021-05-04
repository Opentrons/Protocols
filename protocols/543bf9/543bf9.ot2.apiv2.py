metadata = {
    'protocolName': 'Standard Curve Dilutions',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"p300_mount":"left","curves":2, "stock1_conc":18.12, "stock2_conc":18.12,"csv_file":"Stock1 Conc.,12120000,ng/ml,,,,,,,\\nInts,Source starting Conc./Source name,,Source Vol (uL),Diluent vol (uL),Final Con (ng/ml),Final Vol (uL),Fold Dil of Source,,\\n,,,,,,,,,\\nInt1,12120000,stock1,8.3,41.7,2000000,50,6.06,,\\nInt2,2000000, Int1,12.5,37.5,500000,50,4,,\\nInt3,500000, Int2,5.0,45.0,50000,50,10,,\\nInt4,50000, Int3,25.0,25.0,25000,50,2,,\\n,,,,,,,,,\\nStandard Curve Dilutions from the diluted stock solution,,,,,,,,,\\nStd #,Source starting Conc./Source Name,,Source Vol (uL),Diluent vol (uL),Final Con (ng/ml),Final Vol (uL),Fold Dil of source,,\\n,,,,,,,,,\\nStd1,25000.0,Int4,5,45,2500,50,10,,\\nStd2,2500.0,Std1,12.5,37.5,625,50,4,,\\nStd3,625.0,Std2,12.5,37.5,156.3,50,4,,\\nStd4,156.3,Std3,12.5,37.5,39.1,50,4,,\\nStd5,39.1,Std4,12.5,37.5,9.8,50,4,,\\nStd6,9.8,Std5,12.5,37.5,2.4,50,4,,\\nStd7,2.4,Std6,12.5,37.5,0.6,50,4,,\\nStd8,0.6,Std7,12.5,37.5,0.15,50,4,,\\nBlank (Std9),,,,50,,50.0,,,\\nQC Samples ,,,,,,,,,\\nQC1,25000,Int4,5.2,59.8,2000,65,12.5,,\\nQC2,2000,QC1,5,45,200,50,10,,\\nQC3,200,QC2,5,45,20,50,10,,\\nQC4,20,QC3,5,45,2,50,10,,\\n,,,,,,,,,\"}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [p300_mount, csv_file, curves, stock1_conc, stock2_conc] = get_values(  # noqa: F821
        "p300_mount", "csv_file", "curves", "stock1_conc", "stock2_conc")

    curves = int(curves)
    stock1_conc = stock1_conc*10**6
    stock2_conc = stock2_conc*10**6

    # Load Labware
    plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 6)
    tuberack = ctx.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 3)
    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul', slot) for slot in range(1,3)]

    # Load Pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount, tip_racks=tipracks)

    # Reagents
    stock1 = tuberack['A1']
    diluent = tuberack['B1']

    well_positions_curve1 = {"Int1":"A1", "Int2":"A2", "Int3":"A3", "Int4":"A4",
                             "Std1":"B1", "Std2":"B2", "Std3":"B3", "Std4":"B4", "Std5":"B5", "Std6":"B6", "Std7":"B7", "Std8":"B8", "Blank (Std9)":"B9", "QC1":"C1", "QC2":"C2", "QC3":"C3", "QC4":"C4"}

    well_positions_curve2 = {"Int1":"E1", "Int2":"E2", "Int3":"E3", "Int4":"E4",
                             "Std1":"F1", "Std2":"F2", "Std3":"F3", "Std4":"F4", "Std5":"F5", "Std6":"F6", "Std7":"F7", "Std8":"F8", "Blank (Std9)":"F9", "QC1":"G1", "QC2":"G2", "QC3":"G3", "QC4":"G4"}

    data = [[val.strip() for val in line.split(',')] for line in csv_file.splitlines() if line.split(',')[0].strip()]

    transformed_data_c1 = []
    transformed_data_c2 = []

    def transform_data(data, stock_conc, well_positions, results):
        for i, line in enumerate(data):
            if line[0] in well_positions_curve1:
                if line[1] == '':
                    src_conc = None
                    sample_src = None
                    dest = plate[well_positions[line[0]]]
                    dil_vol = float(line[4])
                    src_vol = None
                    results.append([src_conc, sample_src, dest, dil_vol, src_vol])
                    continue
                src_conc = stock_conc if i == 2 else float(line[1])
                sample_src = stock1 if line[2] == 'stock1' else plate[well_positions[line[2]]]
                src_vol = round((float(line[5]) * float(line[6])/src_conc)*2)/2 # Round to nearest 0.5
                dest = plate[well_positions[line[0]]]
                dil_vol = float(line[6]) - src_vol
                results.append([src_conc, sample_src, dest, dil_vol, src_vol])

    # Liquid Handling Steps
    def liquid_handle(data):
        for line in data:
            src_conc = line[0]
            sample_src = line[1]
            dest = line[2]
            dil_vol = line[3]
            src_vol = line[4]
            # Add diluent and then transfer samples
            p300.pick_up_tip()
            p300.aspirate(dil_vol, diluent)
            p300.dispense(dil_vol, dest)
            p300.drop_tip()
            if src_conc != None:
                p300.pick_up_tip()
                p300.aspirate(src_vol, sample_src)
                p300.dispense(src_vol, dest)
                p300.mix(3, (src_vol+dil_vol)/2)
                p300.blow_out()
                p300.touch_tip()
                p300.drop_tip()

    # Add multi-tube volume tracking function

    # First Standard Curve
    transform_data(data, stock1_conc, well_positions_curve1, transformed_data_c1)
    liquid_handle(transformed_data_c1)

    # Second Standard Curve
    if curves == 2:
        transform_data(data, stock2_conc, well_positions_curve2, transformed_data_c2)
        liquid_handle(transformed_data_c2)