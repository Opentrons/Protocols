metadata = {
    'protocolName': 'DNA and Water Transfer with CSV File',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'

}

def get_values(*names):
    import json
    _all_values = json.loads("""{ "csv":"samples, dna volume of stock, water stock, well\\n s1, 2, 98, A1\\n s2, 4, 90, A2",
                                  "p20_mount":"right",
                                  "p300_mount":"right"}""")
    return [_all_values[n] for n in names]

def run(ctx):

    [csv, p20_mount, p300_mount] = get_values(  # noqa: F821
        "csv", "p20_mount", "p300_mount")

    # add labware
    final_plate = ctx.load_labware('vwr_square_96_microplate_2000ul', '1')
    dna_plate = ctx.load_labware('vwrpcr_96_wellplate_200ul', '2')
    water_res = ctx.load_labware('nest_1_reservoir_195ml', '5')
    tiprack300 = ctx.load_labware('opentrons_96_tiprack_300ul', '3')
    tiprack20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
                 for slot in ['7', '8']]

    # add instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount,
                                tip_racks=tiprack20)
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                            tip_racks=[tiprack300])


    nested_list = [[val.strip() for val in line.split(',')]
                    for line in csv.splitlines()
                    if line.split(',')[0].strip()][1:]

    # add reagent
    # let's pretend it's cherrypicking
    water = water_res.wells()[0]
    dna_vol = 1
    water_vol = 2
    well = 3

    # add water first
    p300.pick_up_tip()
    for row, final_well in zip(nested_list, final_plate.wells()):
        p300.aspirate(int(row[water_vol]), water)
        p300.dispense(int(row[water_vol]), final_well)
    p300.drop_tip()

    # add dna
    for row, final_well in zip(nested_list, final_plate.wells()):
        p20.pick_up_tip()
        p20.aspirate(int(row[dna_vol]), row[well])
        p20.dispense(int(row[dna_vol]), final_well)
        p20.mix(5, 20, final_well)
        p20.drop_tip()
