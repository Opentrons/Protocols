metadata = {
    'protocolName': 'Standard Curve Dilutions with CSV File',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(ctx):

    [p300_mount, csv_file, curves, stock1_conc,
        stock2_conc] = get_values(  # noqa: F821
        "p300_mount", "csv_file", "curves", "stock1_conc", "stock2_conc")

    curves = int(curves)
    stock1_conc = stock1_conc*10**6
    stock2_conc = stock2_conc*10**6

    # Load Labware
    plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', 6)
    tuberack = ctx.load_labware(
        'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 3)
    tipracks = [ctx.load_labware('opentrons_96_tiprack_300ul',
                                 slot) for slot in range(1, 3)]

    # Load Pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tipracks)

    # Reagents
    stock1 = tuberack['A1']
    diluent = tuberack['B1']

    well_positions_curve1 = {"Int1": "A1", "Int2": "A2", "Int3": "A3",
                             "Int4": "A4", "Std1": "B1", "Std2": "B2",
                             "Std3": "B3", "Std4": "B4", "Std5": "B5",
                             "Std6": "B6", "Std7": "B7", "Std8": "B8",
                             "Blank (Std9)": "B9", "QC1": "C1",
                             "QC2": "C2", "QC3": "C3", "QC4": "C4"}

    well_positions_curve2 = {"Int1": "E1", "Int2": "E2", "Int3": "E3",
                             "Int4": "E4", "Std1": "F1", "Std2": "F2",
                             "Std3": "F3", "Std4": "F4", "Std5": "F5",
                             "Std6": "F6", "Std7": "F7", "Std8": "F8",
                             "Blank (Std9)": "F9", "QC1": "G1",
                             "QC2": "G2", "QC3": "G3", "QC4": "G4"}

    data = [[val.strip() for val in line.split(',')] for line in
            csv_file.splitlines() if line.split(',')[0].strip()]

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
                    results.append([src_conc, sample_src, dest, dil_vol,
                                    src_vol])
                    continue
                src_conc = stock_conc if i == 2 else float(line[1])
                if line[2] == 'stock1':
                    sample_src = stock1
                else:
                    sample_src = plate[well_positions[line[2]]]
                # Round to nearest 0.5
                src_vol = round((float(line[5])*float(line[6])/src_conc)*2)/2
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
            if src_conc is not None:
                p300.pick_up_tip()
                p300.aspirate(src_vol, sample_src)
                p300.dispense(src_vol, dest)
                p300.mix(3, (src_vol+dil_vol)/2)
                p300.blow_out()
                p300.touch_tip()
                p300.drop_tip()

    # First Standard Curve
    transform_data(data, stock1_conc, well_positions_curve1,
                   transformed_data_c1)
    liquid_handle(transformed_data_c1)

    # Second Standard Curve
    if curves == 2:
        transform_data(data, stock2_conc, well_positions_curve2,
                       transformed_data_c2)
        liquid_handle(transformed_data_c2)
