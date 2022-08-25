# flake8: noqa

def get_values(*names):
    import json
    _all_values = json.loads("""{"csv":"3,4.3,0.0043,508.59,0.01,1845.47\\n4,4.1,0.0041,462.57,0.01,886.35","tubes_on_slot4":"bricklabwaretype1racklong_24_wellplate_4000ul","p1000_mount":"left", "slot_2_height":2, "slot_2_touch":3,
        "slot_5_touch":5}""")
    return [_all_values[n] for n in names]


metadata = {
    'protocolName': 'Diluting Samples with DMSO',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv, tubes_on_slot4, slot_2_height, slot_2_touch,
        slot_5_touch, p1000_mount] = get_values(  # noqa: F821
        "csv", "tubes_on_slot4", "slot_2_height", "slot_2_touch",
            "slot_5_touch", "p1000_mount")

    all_rows = [[val.strip() for val in line.split(',')]
                for line in csv.splitlines()
                if line.split(',')[0].strip()][1:]

    # labware
    res = ctx.load_labware('nest_1_reservoir_195ml', 1)
    tiprack = ctx.load_labware('opentrons_96_filtertiprack_1000ul', 6)
    final_96_plate = ctx.load_labware('micronic_96_wellplate_1000ul', 5)
    middle_48_plate = ctx.load_labware("altemislab_48_wellplate_2000ul", 2)
    sample_racks = ctx.load_labware(tubes_on_slot4, 4)

    # pipettes
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=[tiprack])



    # protocol
    sample_tubes = [tube for tube in sample_racks.wells()]
    for i, row in enumerate(all_rows):
        vol = float(row[5])
        p1000.transfer(vol, res.wells()[0], sample_tubes[i].bottom(z=2), new_tip='always', air_gap=30, blow_out=True, blowout_location='destination well')
        p1000.pick_up_tip()
        p1000.mix(10, vol if vol < 1000 else 1000, sample_tubes[i].bottom(z=2))
        p1000.blow_out(sample_tubes[i].top(z=-1))
        p1000.drop_tip()

    ctx.pause("Check to see if powder has dissolved in DMSO")
    ctx.comment('\n\n\n')
    airgap = 30

    for i, row in enumerate(all_rows):
        vol = float(row[5])
        p1000.pick_up_tip()
        p1000.transfer(vol+100,
                       sample_tubes[i].bottom(z=2),
                       middle_48_plate.wells()[i].bottom(slot_2_height),
                       new_tip='never',
                       air_gap=30)

        p1000.aspirate(200, middle_48_plate.wells()[i].bottom(slot_2_height))
        p1000.air_gap(airgap)
        p1000.touch_tip(v_offset=-slot_2_touch)
        p1000.dispense(200+airgap, final_96_plate.wells()[i].top(z=-5))
        p1000.blow_out()
        p1000.touch_tip(v_offset=-slot_5_touch)
        p1000.drop_tip()
        ctx.comment('\n')
