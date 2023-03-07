import math

metadata = {
    'protocolName': 'VIB UGENT - Part 1',
    'author': 'Rami Farawi <rami.farawi@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}


def run(ctx):

    [num_samp, sds_vol, init_vol_bsa, init_vol_bca,
        p20_mount, p300_mount] = get_values(  # noqa: F821
        "num_samp", "sds_vol", "init_vol_bsa",
            "init_vol_bca", "p20_mount", "p300_mount")

    if not 1 <= num_samp <= 24:
        raise Exception("Enter a sample number between 1-24")

    modules
    hs_mod = ctx.load_module('heaterShakerModuleV1', 10)
    hs_mod.close_labware_latch()

    # labware
    reservoir = ctx.load_labware('agilent_1_reservoir_290ml', 11)
    sample_rack = ctx.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 1)  # noqa:E501
    pixul_plate = ctx.load_labware('costar_96_wellplate_330ul', 2)
    bsa_tuberack = ctx.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 4)  # noqa:E501

    strip_tube_plate = ctx.load_labware('3dprint_96_tuberack_200ul', 7)
    sample_plate = ctx.load_labware('costar_96_wellplate_330ul', 8)
    agilent_plate = ctx.load_labware('agilent_96_wellplate_500ul', 3)
    uv_plate = ctx.load_labware('greineruvstar_96_wellplate_392ul', 5)
    tips300 = [ctx.load_labware('opentrons_96_tiprack_300ul', slot)
               for slot in [9]]
    tips20 = [ctx.load_labware('opentrons_96_tiprack_20ul', slot)
              for slot in [6]]

    # liquid height tracking
    v_naught_bsa = init_vol_bsa*1000
    v_naught_bca = init_vol_bca*1000
    radius_bsa = bsa_tuberack.rows()[0][0].diameter/2
    radius_bca = bsa_tuberack.rows()[0][2].diameter/2
    h_naught_bsa = 0.85*v_naught_bsa/(math.pi*radius_bsa**2)
    h_naught_bca = 0.85*v_naught_bca/(math.pi*radius_bca**2)
    h_bsa = h_naught_bsa
    h_bca = h_naught_bca

    def adjust_height(vol, bsa_or_bca):
        nonlocal h_bsa
        nonlocal h_bca
        radius = radius_bsa if bsa_or_bca == 'bsa' else radius_bca
        dh = (vol/(math.pi*radius**2))*1.33
        if bsa_or_bca == 'bsa':
            h_bsa -= dh
        elif bsa_or_bca == 'bca':
            h_bca -= dh

        if h_bsa < 12:
            h_bsa = 1
        if h_bca < 12:
            h_bca = 1

    # pipettes
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tips20)
    p300 = ctx.load_instrument('p300_single_gen2',
                               p300_mount, tip_racks=tips300)

    # mapping
    sds = reservoir.wells()[0]
    samples = sample_rack.wells()[:num_samp]
    start_samp_vol = 10

    # protocol
    ctx.comment('\n-------ADDING SDS AND SAMPLE TO PIXUL PLATE-----\n\n\n')
    total_vol = start_samp_vol+sds_vol
    num_samp_wells = math.ceil(total_vol/100)
    split_vol = sds_vol/num_samp_wells
    pixul_chunks = [
                    pixul_plate.wells()[i:i+num_samp_wells]
                    for i in range(0, len(pixul_plate.wells()),
                                   num_samp_wells)
                    ]
    bca = bsa_tuberack.rows()[0][2]
    bsa = bsa_tuberack.wells()[0]  # CHECK FOR LIQUID HEIGHT TRACKING
    standards = [well for row in sample_rack.rows() for well in row][:8]

    sample_ctr = 0

    for sample, chunk in zip(samples, pixul_chunks):
        p300.pick_up_tip()
        p300.aspirate(sds_vol, sds)
        p300.dispense(sds_vol, sample)
        p300.mix(5, sds_vol*0.8, sample, rate=0.5)
        for well in chunk:
            p300.aspirate(split_vol if split_vol <= 100 else 100,
                          sample, rate=0.5)
            ctx.delay(seconds=1)
            p300.dispense(split_vol if split_vol <= 100 else 100,
                          well, rate=0.5)
            sample_ctr += 1

        p300.drop_tip()
        ctx.comment('\n\n')

    ctx.pause("""
    Take out PIXUL plate, fill empty wells of each started column
    with SDS buffer, seal plate and perform PIXUL sonication.
    After sonication, wash bottom of the plate, centrifuge and transfer
    supernatant to new plate using a multichannel pipette offline.
    Place new plate containing supernatant on slot 2.
    Remove empty epps from slot 1.
    """)

    ctx.comment('\n-------ADDING BSA TO STANDARD TUBES-----\n\n\n')
    standards = [well for row in sample_rack.rows() for well in row][:8]

    standard_vols = [500, 375, 250, 187.5, 125, 62.5, 31.25, 0]

    p300.pick_up_tip()
    for tube, vol in zip(standards, standard_vols):
        num_dispenses = math.ceil(vol/300)
        vol_ctr = vol
        for _ in range(num_dispenses):

            p300.aspirate(p300.max_volume if vol_ctr > 300 else vol_ctr, bsa)
            p300.dispense(p300.max_volume if vol_ctr > 300 else vol_ctr, tube)
            adjust_height(p300.max_volume if vol_ctr > 300 else vol_ctr, 'bsa')
            vol_ctr -= p300.max_volume if vol_ctr > 300 else vol_ctr
        ctx.comment('\n')

    p300.drop_tip()

    ctx.comment('\n-------ADDING SDS TO STANDARD TUBES-----\n\n\n')

    sds_vols = list(reversed(standard_vols))
    p300.pick_up_tip()
    for tube, vol in zip(standards, sds_vols):
        num_dispenses = math.ceil(vol/300)
        vol_ctr = vol
        for _ in range(num_dispenses):
            p300.aspirate(p300.max_volume if vol_ctr > 300 else vol_ctr, sds)
            p300.dispense(p300.max_volume if vol_ctr > 300 else vol_ctr,
                          tube.top())
            vol_ctr -= p300.max_volume if vol_ctr > 300 else vol_ctr
        ctx.comment('\n')

    # mix from low concentration tube to highest
    for tube, vol in zip(list(reversed(standards[1:7])), sds_vols):

        p300.mix(3, 300, tube)

    p300.drop_tip()

    ctx.pause("""
    Close epps and transfer 4-in-1-rack with epps to heater-shaker module on
    slot 10. Remove 15 ml tube containing leftover BSA.
    Shake plate at RT for 5 min at 1000 rpm.
    Centrifuge eppendorfs containing BSA solutions for a few seconds to gather
    solution at the bottom of the tubes. Place open eppendorfs back
    in 4-in-1-rack on slot 1.
    """)

    ctx.comment('\n-------ADDING STANDARDS TO PLATE-----\n\n\n')
    for tube, dest_row in zip(standards, strip_tube_plate.rows()):
        p300.pick_up_tip()
        for well in dest_row:
            p300.aspirate(35, tube)
            p300.dispense(35, well)
        p300.drop_tip()
        ctx.comment('\n')

    ctx.pause('''

    Seal PCR tubes and store in -20°C freezer, leave one strip in slot 7
    (column 1, A1-H1) for current experiment. Remove eppendorf tubes
    from slot 1. Place a PP 96-well plate on slot 3 and a UV-star 96-well plate
    (for BCA measurement) on slot 5. Make sure the 96-well plate containing
    sample is on slot 8.
    ''')

    ctx.comment('\n-------ADDING SDS TO PLATE-----\n\n\n')
    p300.pick_up_tip()
    for well in agilent_plate.wells()[:num_samp]:  # check this sample counter!!!!!
        p300.aspirate(30, sds)
        p300.dispense(30, well)
    p300.drop_tip()

    ctx.comment('\n-------ADDING SAMPLE TO PLATE-----\n\n\n')

    uv_dispense_wells = [
                        well
                        for i in range(6)
                        for row in uv_plate.rows()
                        for well in row[2+2*i:4+2*i]
    ]

    chunked_uv_wells = [uv_dispense_wells[i:i+2]
                        for i in range(0, len(uv_dispense_wells), 2)]

    for s, d, chunk in zip(sample_plate.wells(),
                           agilent_plate.wells()[:num_samp],
                           chunked_uv_wells):
        p20.pick_up_tip()
        p20.aspirate(10, s)
        p20.dispense(10, d)
        p20.mix(5, 20, d)
        for uv_well in chunk:
            p20.aspirate(10, d)
            p20.dispense(10, uv_well)
        p20.drop_tip()
        ctx.comment('\n')

    ctx.comment('\n-------TRANSFER STANDARDS TO UV PLATE-----\n\n\n')

    for i, s in enumerate(strip_tube_plate.wells()[:8]):
        p20.pick_up_tip()
        p20.aspirate(10, s)
        p20.dispense(10, uv_plate.rows()[i][0])
        p20.aspirate(10, s)
        p20.dispense(10, uv_plate.rows()[i][1])
        p20.drop_tip()

    # step 18
    ctx.comment('\n-------TRANSFER BCA TO PLATE-----\n\n\n')

    # transfer bca to standards
    p300.pick_up_tip()
    for i in range(8):
        p300.aspirate(200, bca)
        p300.dispense(200, uv_plate.rows()[i][0])
        p300.aspirate(200, bca)
        p300.dispense(200, uv_plate.rows()[i][1])
        adjust_height(200, 'bsa')
    ctx.comment('\n')

    # transfer bca to samples
    for well in uv_dispense_wells[:num_samp*2]:
        p300.aspirate(200, bca)
        p300.dispense(200, well)
        adjust_height(200, 'bca')
    p300.drop_tip()

    ctx.pause("""Seal UV-start plate on slot 5 and transfer to heater-shaker
                 module on slot 10""")
