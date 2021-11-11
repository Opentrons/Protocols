metadata = {
    'protocolName': 'Sample Prep MALDI spotting - Serial Dilution',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{"num_dilutions":8,
                                    "initial_vol_stock":230,
                                    "initial_vol_dilution":9770,
                                    "step_vol_stock":1200,
                                    "step_vol_dilution":8800,
                                  "mount":"right"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [num_dilutions, initial_vol_stock, initial_vol_dilution,
     step_vol_stock, step_vol_dilution, mount] = get_values(  # noqa: F821
        "num_dilutions", "initial_vol_stock", "initial_vol_dilution",
         "step_vol_stock", "step_vol_dilution", "mount")

    if not 1 <= num_dilutions <= 15:
        raise Exception("Enter a number of dilution tubes 1-15")

    # load labware
    stock_rack = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '1')
    dilute_rack = ctx.load_labware(
                    'opentrons_15_tuberack_falcon_15ml_conical', '2')
    diluent_labware = ctx.load_labware('nest_1_reservoir_195ml', '3')
    tiprack = ctx.load_labware('opentrons_96_tiprack_1000ul', '4')

    # load instrument
    pip = ctx.load_instrument('p1000_single_gen2', mount, tip_racks=[tiprack])

    # protocol
    stock_tube = stock_rack.wells()[0]
    wells_by_row = [well for row in dilute_rack.rows() for well in row]

    all_tubes = {}
    for k in range(num_dilutions):
        key = k
        value = wells_by_row[k]
        all_tubes[key] = value

    diluent = diluent_labware.wells()[0]

    # add first tube
    pip.pick_up_tip()
    pip.transfer(initial_vol_stock, stock_tube, all_tubes[0], new_tip='never')
    pip.drop_tip()
    pip.pick_up_tip()
    pip.transfer(initial_vol_dilution, diluent, all_tubes[0], new_tip='never')
    pip.mix(5, 1000, all_tubes[0])
    pip.drop_tip()
    ctx.comment('\n\n\n')

    # add diluent to all tubes
    pip.pick_up_tip()
    pip.distribute(step_vol_dilution,
                   diluent,
                   [all_tubes[i] for i in range(1, num_dilutions)],
                   new_tip='never')
    pip.drop_tip()
    ctx.comment('\n\n\n')

    # add stock
    pip.pick_up_tip()
    for i in range(num_dilutions-1):
        pip.transfer(step_vol_stock,
                     all_tubes[i],
                     all_tubes[i+1],
                     new_tip='never')
        pip.mix(5, 1000, all_tubes[i+1])
    pip.drop_tip()
    ctx.comment('\n\n\n')
