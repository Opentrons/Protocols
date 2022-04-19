import math

metadata = {
    'protocolName': 'Dilution with CSV File and Custom Tube Rack',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [csv, init_vol_dil, p20_mount, p1000_mount] = get_values(  # noqa: F821
        "csv", "init_vol_dil", "p20_mount", "p1000_mount")

    # load Labware and modules
    temp_mod = ctx.load_module('temperature module gen2', 1)
    temp_mod.set_temperature(4)

    final_rack = temp_mod.load_labware('thermofisher_40_tuberack_2000ul')
    sample_plate = ctx.load_labware('nest_96_wellplate_200ul_flat', 2)
    diluent_rack = ctx.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 4)  # noqa: E501
    tips = [ctx.load_labware('opentrons_96_tiprack_20ul', 5)]
    tips1000 = [ctx.load_labware('opentrons_96_filtertiprack_1000ul', 6)]

    # load instrument
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tips)
    p1000 = ctx.load_instrument('p1000_single_gen2', p1000_mount,
                                tip_racks=tips1000)

    csv_rows = [[val.strip() for val in line.split(',')]
                for line in csv.splitlines()
                if line.split(',')[0].strip()][1:]

    # liquid height tracking
    v_naught_dil = init_vol_dil*1000
    radius = diluent_rack.wells()[0].diameter/2
    h_naught_dil = 1.15*v_naught_dil/(math.pi*radius**2)
    h = h_naught_dil

    def adjust_height(vol):
        nonlocal h
        dh = vol/(math.pi*radius**2)
        h -= dh
        if h < 12:
            h = 1

    # protocol
    ctx.comment('\n~~~~ADDING DILUENT~~~~\n\n')
    for row in csv_rows:
        dil_vol = int(row[3])
        airgap = (p1000.max_volume-dil_vol)*0.05
        disp_tube = row[2]

        p1000.pick_up_tip()
        p1000.aspirate(dil_vol, diluent_rack.wells()[0].bottom(z=h))
        p1000.air_gap(airgap)
        p1000.dispense(dil_vol+airgap, final_rack.wells_by_name()[disp_tube])
        p1000.drop_tip()
        adjust_height(dil_vol)
        ctx.comment('\n')

    ctx.comment('\n~~~~ADDING SAMPLE~~~~\n\n')
    for row in csv_rows:
        sample_vol = int(row[1])
        samp_well = sample_plate.wells_by_name()[row[0]]
        disp_tube = final_rack.wells_by_name()[row[2]]

        p20.pick_up_tip()
        p20.transfer(sample_vol, samp_well, disp_tube, new_tip='never')
        p20.mix(3, p20.max_volume, disp_tube)
        p20.blow_out()
        p20.drop_tip()
        ctx.comment('\n')
