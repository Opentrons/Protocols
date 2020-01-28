# metadata
metadata = {
    'protocolName': 'Normalization from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    [input_csv, p10_mount, p50_mount] = get_values(  # noqa: F821
        'input_csv', 'p10_mount', 'p50_mount')
    # [input_csv, p10_mount, p50_mount] = [
    #     "source plate well, destination plate well, volume sample (µl),\
    #     volume diluent (µl)\nA1, A1, 2, 28", 'right', 'left'
    # ]

    # labware
    source_plate = ctx.load_labware(
        'eppendorf_96_well_on_block', '1', 'source plate')
    destination_plate = ctx.load_labware(
        'eppendorf_96_well_on_block', '2', 'destination plate')
    tiprack10 = [
        ctx.load_labware('opentrons_96_tiprack_10ul', slot, '10ul tiprack')
        for slot in ['3', '6']
    ]
    water = ctx.load_labware(
        'usascientific_12_reservoir_22ml', '5',
        'reservoir for water (channel 1)').wells()[0].bottom(5)
    tiprack50 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot, '300ul tiprack')
        for slot in ['8', '9']
    ]

    # pipettes
    p10 = ctx.load_instrument(
        'p10_single', p10_mount, tip_racks=tiprack10)
    p50 = ctx.load_instrument(
        'p50_single', p50_mount, tip_racks=tiprack50)

    # parse
    sources = [
        source_plate.wells_by_name()[line.split(',')[0].strip().upper()]
        for line in input_csv.splitlines()[1:] if line
    ]
    dests = [
        destination_plate.wells_by_name()[line.split(',')[1].strip().upper()]
        for line in input_csv.splitlines()[1:] if line
    ]
    vols_sample = [
        float(line.split(',')[2])
        for line in input_csv.splitlines()[1:] if line
    ]
    vols_water = [
        float(line.split(',')[3])
        for line in input_csv.splitlines()[1:] if line
    ]

    # perform normalization
    for s, d, vol_s, vol_w in zip(sources, dests, vols_sample, vols_water):
        # move larger volume first
        if vol_s > vol_w:
            r1, r2 = s, water
            vol1, vol2 = vol_s, vol_w
            drop = True
        else:
            r1, r2 = water, s
            vol1, vol2 = vol_w, vol_s
            drop = False

        # pre-transfer diluent
        pip = p50 if vol1 > 10 else p10
        pip.pick_up_tip()
        pip.transfer(vol1, r1, d.bottom(2), new_tip='never')
        pip.blow_out(d.top(-2))
        if drop:
            pip.drop_tip()

        # transfer sample
        pip = p50 if vol2 > 10 else p10
        if not pip.hw_pipette['has_tip']:
            pip.pick_up_tip()
        pip.transfer(vol2, r2, d, new_tip='never')
        pip.blow_out(d.top(-2))
        for p in [p10, p50]:
            if p.hw_pipette['has_tip']:
                p.drop_tip()
