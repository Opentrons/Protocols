# flake8: noqa

metadata = {
    'protocolName': 'Diluting Samples with DMSO',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"csv":"vial #,amount (mg),amount,formula weight,desired conc. ,dmso needed\\n1,4.3,0.0043,448.53,0.01,500\\n2,4.6,0.0046,462.55,0.01,700\\n3,4.3,0.0043,801,0.01,900\\n4,4.1,0.0041,462.57,0.01,1000\\n5,4.4,0.0044,333.65,0.01,1100\\n6,4.3,0.0043,483.51,0.01,1200\\n7,4.5,0.0045,466.48,0.01,1300\\n8,4.2,0.0042,480.5,0.01,1500\\n9,4.5,0.0045,476.53,0.01,1700\\n10,4.1,0.0041,494,0.01,678","p1000_mount":"left"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [csv, p1000_mount] = get_values(  # noqa: F821
        "csv", "p1000_mount")

    p1000_mount = "left"

    all_rows = [[val.strip() for val in line.split(',')]
                for line in csv.splitlines()
                if line.split(',')[0].strip()][1:]

    # labware
    res = ctx.load_labware('nest_1_reservoir_195ml', 1)
    tiprack = ctx.load_labware('opentrons_96_filtertiprack_1000ul', 6)
    final_96_plate = ctx.load_labware('micronic_96_wellplate_1000ul', 5)
    middle_48_plate = ctx.load_labware('altemislab_48_wellplate_2000ul', 2)
    sample_racks = ctx.load_labware('opentrons_15_tuberack_2000ul', 4)

    # pipettes
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=[tiprack])

    # protocol
    sample_tubes = [tube for tube in sample_racks.wells()]
    for i, row in enumerate(all_rows):
        vol = float(row[5])
        p1000.transfer(vol, res.wells()[0], sample_tubes[i].top(z=-1), new_tip='always', air_gap=30, blow_out=True, blowout_location='destination well')
        p1000.pick_up_tip()
        p1000.mix(10, vol if vol < 1000 else 1000, sample_tubes[i].bottom(z=2))
        p1000.blow_out(sample_tubes[i].top(z=-1))
        p1000.drop_tip()

    ctx.pause("Check to see if powder has dissolved in DMSO")
    ctx.comment('\n\n\n')

    for i, row in enumerate(all_rows):
        vol = float(row[5])
        p1000.pick_up_tip()
        p1000.transfer(vol+100,
                       sample_tubes[i].bottom(z=2),
                       middle_48_plate.wells()[i],
                       new_tip='never',
                       air_gap=30)
        p1000.transfer(200,
                       middle_48_plate.wells()[i],
                       final_96_plate.wells()[i].top(z=-5),
                       new_tip='never',
                       air_gap=30,
                       touch_tip=True)
        p1000.blow_out()
        p1000.drop_tip()
        ctx.comment('\n')