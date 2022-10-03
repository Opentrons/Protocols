metadata = {
    'protocolName': 'Luminex Assay Creating Replicates',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{ "num_samp":48,
                                  "sample_volume": 50,
                                  "antibody_vol":60,
                                  "p300_mount":"left",
                                  "p1000_mount":"right"}""")
    return [_all_values[n] for n in names]


def run(ctx):

    [sample_volume, antibody_vol,
        p300_mount, p1000_mount] = get_values(  # noqa: F821
         "sample_volume", "antibody_vol",
            "p300_mount", "p1000_mount")

    # labware
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', 3)
    plates = [ctx.load_labware('greiner_96_wellplate_200ul', slot)
                               for slot in [1, 2]]
    source_isopaks = [ctx.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', slot)
                      for slot in [4, 5, 7, 8]]
    tips = [ctx.load_labware('opentrons_96_tiprack_300ul', slot) for slot in [9, 10, 11]]

    # pipettes
    p300 = ctx.load_instrument('p300_multi_gen2', p300_mount, tip_racks=tips)

    # mapping
    beads = reservoir.wells()[0]
    antibodies = reservoir.wells()[1]
    sape = reservoir.wells()[2]

    plate_wells = [col for plate in plates for col in plate.rows()[0]]
    full_tips = [col for col in tips[0].rows()[0]]
    alternate_tips = [col for rack in tips[1:] for col in rack.rows()[0]]
    full_tip_count = 0
    alternate_tip_count = 0

    def pick_up_full():
        nonlocal full_tip_count
        p300.pick_up_tip(full_tips[full_tip_count])
        full_tip_count += 1

    def pick_up_alternate():
        nonlocal alternate_tip_count
        p300.pick_up_tip(alternate_tips[alternate_tip_count])
        alternate_tip_count += 1

    # protocol
    ctx.comment('\n---------------Transferring Beads----------------\n\n')

    pick_up_full()
    p300.aspirate(p300.max_volume, beads)
    vol_ctr = p300.max_volume
    for col in plate_wells:
        p300.dispense(50, col)
        vol_ctr -= 50
        if vol_ctr < 50 + sample_volume*0.1:
            p300.dispense(p300.current_volume, beads)
            p300.aspirate(p300.max_volume, beads)
            vol_ctr = p300.max_volume
    p300.dispense(p300.current_volume, beads)
    p300.drop_tip()
    ctx.comment('\n')

    ctx.comment('\n---------------Transferring Sample----------------\n\n')
    plate1_source_isopaks = source_isopaks[:2]
    plate2_source_isopaks = source_isopaks[2:]

    for j, pak in enumerate(plate1_source_isopaks):
        for i, s_col in zip(range(0, 12, 2), pak.rows()[0]):
            pick_up_alternate()
            p300.aspirate(200, s_col)
            p300.dispense(100, plates[0].rows()[j][i].top(z=-3))
            p300.touch_tip()
            p300.dispense(100, plates[0].rows()[j][i+1].top(z=-3))
            p300.blow_out()
            p300.touch_tip()
            p300.drop_tip()
        ctx.comment('\n')

    for j, pak in enumerate(plate2_source_isopaks):
        for i, s_col in zip(range(0, 12, 2), pak.rows()[0]):
            pick_up_alternate()
            p300.aspirate(200, s_col)
            p300.dispense(100, plates[1].rows()[j][i])
            p300.touch_tip()
            p300.dispense(100, plates[1].rows()[j][i+1])
            p300.blow_out()
            p300.touch_tip()
            p300.drop_tip()
        ctx.comment('\n')

    ctx.comment('\n')

    ctx.comment('\n---------------Transferring Antibodies----------------\n\n')

    pick_up_full()
    for col in plate_wells:
        p300.aspirate(antibody_vol, antibodies)
        p300.dispense(antibody_vol, col.top())
        p300.blow_out()
    p300.drop_tip()
    ctx.comment('\n')

    ctx.comment('\n---------------Transferring SA-PE----------------\n\n')
    pick_up_full()
    for col in plate_wells:
        p300.aspirate(75, sape)
        p300.dispense(75, col.top())
        p300.blow_out()
    p300.drop_tip()
    ctx.comment('\n')
