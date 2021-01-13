def get_values(*names):
    import json
    _all_values = json.loads("""{"dna_csv":"Plate LC (Source),Source Well #,ID ,concentration (ug/ml),yield (ug),Destination 1 volume (ul),Destination 1 (Dil),Destination 1 (Dil Plate) Well,concentration dil (ug/ml),yield (ug),Destination 2 volume (ul),Destination 2 (final norm plate),Destination 2 (well #)\\nLC 96-well plate,A1,pET4286,3000.00,6.00,10,LC Dil Plate,A1,300.00,6.00,20.00,Norm Plate,A1\\nLC 96-well plate,B1,pET4287,3400.00,6.00,10,LC Dil Plate,B1,340.00,6.00,17.65,Norm Plate,B1\\nLC 96-well plate,C1,pET4288,840.00,6.00,0,LC Dil Plate,C1,840.00,6.00,7.14,Norm Plate,C1\\nLC 96-well plate,D1,pET4289,2500.00,6.00,10,LC Dil Plate,D1,250.00,6.00,24.00,Norm Plate,D1\\nLC 96-well plate,E1,pET4290,580.00,6.00,0,LC Dil Plate,E1,580.00,6.00,10.34,Norm Plate,E1\\nLC 96-well plate,F1,pET4291,2800.00,6.00,10,LC Dil Plate,F1,280.00,6.00,21.43,Norm Plate,F1\\nLC 96-well plate,E2,pET4292,2600.00,6.00,10,LC Dil Plate,E2,260.00,6.00,23.08,Norm Plate,E2\\nLC 96-well plate,F2,pET4293,440.00,6.00,0,LC Dil Plate,F2,440.00,6.00,13.64,Norm Plate,F2\\nLC 96-well plate,G2,pET4294,3000.00,6.00,10,LC Dil Plate,G2,300.00,6.00,20.00,Norm Plate,G2\\nLC 96-well plate,H2,pET4295,760.00,6.00,0,LC Dil Plate,H2,760.00,6.00,7.89,Norm Plate,H2\\nLC 96-well plate,A3,pET4296,3000.00,6.00,10,LC Dil Plate,A3,300.00,6.00,20.00,Norm Plate,A3\\nLC 96-well plate,B3,pET4297,3000.00,6.00,10,LC Dil Plate,B3,300.00,6.00,20.00,Norm Plate,B3\\nLC 96-well plate,C3,pET4298,3000.00,6.00,10,LC Dil Plate,C3,300.00,6.00,20.00,Norm Plate,C3\\nLC 96-well plate,D3,pET4298,3000.00,6.00,10,LC Dil Plate,D3,300.00,6.00,20.00,Norm Plate,D3\\nLC 96-well plate,E3,pET4298,3000.00,6.00,10,LC Dil Plate,E3,300.00,6.00,20.00,Norm Plate,E3\\nLC 96-well plate,F3,pET4298,3000.00,6.00,10,LC Dil Plate,F3,300.00,6.00,20.00,Norm Plate,F3\\nLC 96-well plate,G3,pET4298,3000.00,6.00,10,LC Dil Plate,G3,300.00,6.00,20.00,Norm Plate,G3\\nLC 96-well plate,H3,pET4298,3000.00,6.00,10,LC Dil Plate,H3,300.00,6.00,20.00,Norm Plate,H3\\nLC 96-well plate,A3,pET4299,3000.00,6.00,10,LC Dil Plate,A3,300.00,6.00,20.00,Norm Plate,A3\\nLC 96-well plate,B3,pET4300,3000.00,6.00,10,LC Dil Plate,B3,300.00,6.00,20.00,Norm Plate,B3\\nLC 96-well plate,C3,pET4015,3300,6.00,10,LC Dil Plate,C3,330.00,6.00,18.18,Norm Plate,C3\\nLC 96-well plate,D3,pET4016,3000,6.00,10,LC Dil Plate,D3,300.00,6.00,20.00,Norm Plate,D3\\nLC 96-well plate,E3,pET4017,3300,6.00,10,LC Dil Plate,E3,330.00,6.00,18.18,Norm Plate,E3\\nLC 96-well plate,F3,pET4015,3300,6.00,10,LC Dil Plate,F3,330.00,6.00,18.18,Norm Plate,F3\\nLC 96-well plate,G3,pET4016,3000,6.00,10,LC Dil Plate,G3,300.00,6.00,20.00,Norm Plate,G3\\nLC 96-well plate,H3,pET4017,3300,6.00,10,LC Dil Plate,H3,330.00,6.00,18.18,Norm Plate,H3\\nHC 96-well plate,A1,pET4027,1600,6.00,10,HC Dil Plate,A1,160,6.00,37.50,Norm Plate,A1\\nHC 96-well plate,B1,pET4027,1600,6.00,10,HC Dil Plate,B1,160,6.00,37.50,Norm Plate,B1\\nHC 96-well plate,C1,pET4027,1600,6.00,10,HC Dil Plate,C1,160,6.00,37.50,Norm Plate,C1\\nHC 96-well plate,D1,pET4027,1600,6.00,10,HC Dil Plate,D1,160,6.00,37.50,Norm Plate,D1\\nHC 96-well plate,E1,pET4027,1600,6.00,10,HC Dil Plate,E1,160,6.00,37.50,Norm Plate,E1\\nHC 96-well plate,F1,pET4027,1600,6.00,10,HC Dil Plate,F1,160,6.00,37.50,Norm Plate,F1\\nHC 96-well plate,E2,pET4033,1800,6.00,10,HC Dil Plate,E2,180,6.00,33.33,Norm Plate,E2\\nHC 96-well plate,F2,pET4033,1800,6.00,10,HC Dil Plate,F2,180,6.00,33.33,Norm Plate,F2\\nHC 96-well plate,G2,pET4033,1800,6.00,10,HC Dil Plate,G2,180,6.00,33.33,Norm Plate,G2\\nHC 96-well plate,H2,pET4033,1800,6.00,10,HC Dil Plate,H2,180,6.00,33.33,Norm Plate,H2\\nHC 96-well plate,A3,pET4033,1800,6.00,10,HC Dil Plate,A3,180,6.00,33.33,Norm Plate,A3\\nHC 96-well plate,B3,pET4033,1800,6.00,10,HC Dil Plate,B3,180,6.00,33.33,Norm Plate,B3\\nHC 96-well plate,C3,pET4033,1800,6.00,10,HC Dil Plate,C3,180,6.00,33.33,Norm Plate,C3\\nHC 96-well plate,D3,pET4302,3000,6.00,10,HC Dil Plate,D3,300,6.00,20.00,Norm Plate,D3\\nHC 96-well plate,E3,pET4303,3000,6.00,10,HC Dil Plate,E3,300,6.00,20.00,Norm Plate,E3\\nHC 96-well plate,F3,pET4304,3000,6.00,10,HC Dil Plate,F3,300,6.00,20.00,Norm Plate,F3\\nHC 96-well plate,G3,pET4305,3000,6.00,10,HC Dil Plate,G3,300,6.00,20.00,Norm Plate,G3\\nHC 96-well plate,H3,pET4306,3000,6.00,10,HC Dil Plate,H3,300,6.00,20.00,Norm Plate,H3\\nHC 96-well plate,A3,pET4033,1800,6.00,10,HC Dil Plate,A3,180,6.00,33.33,Norm Plate,A3\\nHC 96-well plate,B3,pET4033,1800,6.00,10,HC Dil Plate,B3,180,6.00,33.33,Norm Plate,B3\\nHC 96-well plate,C3,pET4307,3000,6.00,10,HC Dil Plate,C3,300,6.00,20.00,Norm Plate,C3\\nHC 96-well plate,D3,pET4307,3000,6.00,10,HC Dil Plate,D3,300,6.00,20.00,Norm Plate,D3\\nHC 96-well plate,E3,pET4307,3000,6.00,10,HC Dil Plate,E3,300,6.00,20.00,Norm Plate,E3\\nHC 96-well plate,F3,pET4308,3000,6.00,10,HC Dil Plate,F3,300,6.00,20.00,Norm Plate,F3\\nHC 96-well plate,G3,pET4308,3000,6.00,10,HC Dil Plate,G3,300,6.00,20.00,Norm Plate,G3\\nHC 96-well plate,H3,pET4308,3000,6.00,10,HC Dil Plate,H3,300,6.00,20.00,Norm Plate,H3\\nwater,A1,,,,,,,,,62.50,Norm Plate,A1\\nwater,B1,,,,,,,,,64.85,Norm Plate,B1\\nwater,C1,,,,,,,,,75.36,Norm Plate,C1\\nwater,D1,,,,,,,,,58.50,Norm Plate,D1\\nwater,E1,,,,,,,,,72.16,Norm Plate,E1\\nwater,F1,,,,,,,,,61.07,Norm Plate,F1\\nwater,E2,,,,,,,,,63.59,Norm Plate,E2\\nwater,F2,,,,,,,,,73.03,Norm Plate,F2\\nwater,G2,,,,,,,,,66.67,Norm Plate,G2\\nwater,H2,,,,,,,,,78.77,Norm Plate,H2\\nwater,A3,,,,,,,,,66.67,Norm Plate,A3\\nwater,B3,,,,,,,,,66.67,Norm Plate,B3\\nwater,C3,,,,,,,,,66.67,Norm Plate,C3\\nwater,D3,,,,,,,,,80.00,Norm Plate,D3\\nwater,E3,,,,,,,,,80.00,Norm Plate,E3\\nwater,F3,,,,,,,,,80.00,Norm Plate,F3\\nwater,G3,,,,,,,,,80.00,Norm Plate,G3\\nwater,H3,,,,,,,,,80.00,Norm Plate,H3\\nwater,A3,,,,,,,,,66.67,Norm Plate,A3\\nwater,B3,,,,,,,,,66.67,Norm Plate,B3\\nwater,C3,,,,,,,,,81.82,Norm Plate,C3\\nwater,D3,,,,,,,,,80.00,Norm Plate,D3\\nwater,E3,,,,,,,,,81.82,Norm Plate,E3\\nwater,F3,,,,,,,,,81.82,Norm Plate,F3\\nwater,G3,,,,,,,,,80.00,Norm Plate,G3\\nwater,H3,,,,,,,,,81.82,Norm Plate,H3\"}""")
    return [_all_values[n] for n in names]

metadata = {
    'protocolName': 'DNA Normalization from .csv',
    'author': 'Sakib <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(ctx):

    [dna_csv] = get_values(  # noqa: F821
        "dna_csv")

    # Load Labware
    tiprack_300ul = [ctx.load_labware('opentrons_96_tiprack_300ul', slot) for slot in range(1,2)]
    tiprack_20ul = [ctx.load_labware('opentrons_96_tiprack_20ul', slot) for slot in range(2,3)]

    plates = {
        'LC 96-well plate': ctx.load_labware('thermofisher_96_skirted_pcr_200ul', 5, label='LC 96-well plate'),
        'HC 96-well plate': ctx.load_labware('thermofisher_96_skirted_pcr_200ul', 6, label='HC 96-well plate'),
        'water': ctx.load_labware('agilent_1_reservoir_290ml', 7, label='water'),
        'LC Dil Plate': ctx.load_labware('thermofisher_96_skirted_pcr_200ul', 8, label='LC Dil Plate'),
        'HC Dil Plate': ctx.load_labware('thermofisher_96_skirted_pcr_200ul', 9, label='HC Dil Plate'),
        'Norm Plate': ctx.load_labware('thermofisher_96_skirted_pcr_200ul', 10, label='Norm Plate')
    }

    # Load Pipettes
    p300 = ctx.load_instrument('p300_single_gen2', 'left', tip_racks=tiprack_300ul)
    p20 = ctx.load_instrument('p20_single_gen2', 'right', tip_racks=tiprack_20ul)

    # Transfer 90 uL of Water to LC Dil Plate and HC Dil Plate
    p300.transfer(90, plates['water'].wells(), [plates['LC Dil Plate'].wells(), plates['HC Dil Plate'].wells()])

    # Parse CSV
    data = [[val.strip() for val in line.split(',')] for line in dna_csv.splitlines()[1:] if line and line.split(',')[0]]
    dna_data = []
    water_data = []

    for row in data:
        if row[0] == 'water':
            water_data.append(row)
        else:
            dna_data.append(row)

    # Transfer Water
    for row in water_data:
        s_plate, d2_vol, d2_plate, d2_well = row[0], row[10], row[11], row[12]

        d2_vol = float(d2_vol)
        s_plate = plates[s_plate]
        d2_plate = plates[d2_plate]

        pip = p300 if d2_vol > 20 else p20
        pip.transfer(d2_vol, plates['water'].wells(), d2_plate.wells_by_name()[d2_well])

    # Transfer DNA
    for row in dna_data:
        s_plate, s_well, d1_vol, d1_plate, d1_well, d2_vol, d2_plate, d2_well = row[0], row[1], row[5], row[6], row[7], row[10], row[11], row[12]

        d1_vol = float(d1_vol)
        d2_vol = float(d2_vol)
        s_plate = plates[s_plate]
        d1_plate = plates[d1_plate]
        d2_plate = plates[d2_plate]

        pip = p300 if d1_vol > 20 else p20
        pip.transfer(d1_vol, s_plate.wells_by_name()[s_well], d1_plate.wells_by_name()[d1_well])

        pip = p300 if d2_vol > 20 else p20
        pip.transfer(d2_vol, s_plate.wells_by_name()[s_well], d2_plate.wells_by_name()[d2_well])
