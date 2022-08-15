from opentrons import protocol_api
import math

metadata = {
    'protocolName': 'Alpco Human Insulin ELISA',
    'author': 'Chaz Childers <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx: protocol_api.ProtocolContext):
    [
     _num_samps,
     _multi_mnt,
     _manual_ctrls,
     _manual_wash
    ] = get_values(  # noqa: F821 (<--- DO NOT REMOVE!)
        "_num_samps",
        "_multi_mnt",
        "_manual_ctrls",
        "_manual_wash")

    # VARIABLES
    num_samps = _num_samps
    manual_ctrls = _manual_ctrls
    multi_mnt = _multi_mnt
    manual_wash = _manual_wash

    # load labware
    dest_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '2')
    samp_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '3')
    res12 = ctx.load_labware('nest_12_reservoir_15ml', '1')
    wb_res = ctx.load_labware('nest_1_reservoir_195ml', '4')
    waste_res = ctx.load_labware('nest_1_reservoir_195ml', '11')
    tips = [
        ctx.load_labware(
            'opentrons_96_tiprack_300ul', s) for s in [5, 7, 8, 9, 10]
            ]

    # load pipette
    m300 = ctx.load_instrument('p300_multi_gen2', multi_mnt, tip_racks=tips)

    # reagent locations
    antibody = res12['A1']
    tmb = res12['A4']
    stop_sol = res12['A7']

    wash_buffer = wb_res['A1']

    liq_waste = waste_res['A1'].top()
    all_tips = [well for rack in tips for well in rack.rows()[0]]
    tip_ctr = 0

    def pick_up(pipette):
        """`pick_up()` will pause the protocol when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the protocol will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.
        :param pipette: The pipette desired to pick up tip
        as definited earlier in the protocol (e.g. p300, m20).
        """
        nonlocal tip_ctr
        try:
            pipette.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.home()
            ctx.pause("Replace empty tip racks")
            pipette.reset_tipracks()
            tip_ctr = 0
            pipette.pick_up_tip()

    def drop_used():
        """
        `drop_used` will drop used tips in empty tip rack for ease of
        waste removal and to help mitigate a full trash bin
        """
        nonlocal tip_ctr
        m300.drop_tip(all_tips[tip_ctr])
        tip_ctr += 1

    # Transfer 25ul of standards, controls, samples
    # standards/controls
    if not manual_ctrls:
        ctrl_rack = ctx.load_labware(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '3')
        s_mnt = 'left' if multi_mnt == 'right' else 'right'
        p300 = ctx.load_instrument('p300_single_gen2', s_mnt, tip_racks=tips)

        for src, dest in zip(ctrl_rack.wells(), dest_plate.wells()[:8]):
            p300.transfer(25, src, dest)
    else:
        ctx.pause('Please ensure standards + controls are in the first column')

    num_cols = math.ceil(num_samps/8)
    dest_cols = range(1, 12, 2)
    for d, col in zip(dest_cols, samp_plate.rows()[0][:num_cols]):
        pick_up(m300)
        m300.mix(3, 50, col)
        m300.aspirate(50, col)
        m300.dispense(25, dest_plate.rows()[0][d])
        m300.dispense(25, dest_plate.rows()[0][d+1])
        m300.drop_tip()

    # Add 100ul detection antibody
    ctx.comment(
        '\nAdding 100uL Dettection Antibody from A1 of 12-Well Reservoir')
    all_cols = num_cols + 1
    all_samps = dest_plate.rows()[0][:all_cols]
    pick_up(m300)
    for col in all_samps:
        m300.aspirate(100, antibody)
        m300.dispense(100, col.top(-1))
    m300.drop_tip()

    ctx.pause(
        '\nAddition of Detection Antibody complete. Please cover plate \
        and place on shaker for 1 hour at room temperature. When ready \
        for next steps, replace plate and click RESUME.')

    # 6 washes with 350uL wash buffer
    if not manual_wash:
        for idx in range(1, 7):
            ctx.comment(f'\nPerforming Wash {idx}')
            pick_up(m300)
            for col in all_samps:
                for _ in range(2):
                    m300.aspirate(175, wash_buffer)
                    m300.dispense(175, col.top())
            drop_used()
            for col in all_samps:
                pick_up(m300)
                for _ in range(2):
                    m300.aspirate(200, col)
                    m300.dispense(175, liq_waste)
                drop_used()
        ctx.pause(
            '\nWashes complete. \
            Please ensure all wash buffer has been removed from wells. \
            When ready, click RESUME.')
    else:
        ctx.pause('\nPlease perform 6 washes manually. \
        When ready for automated addition of TMB, click RESUME')

    # Add 100uL of TMB Sustrate
    ctx.comment('\nAdding 100uL of TMB Substrate')
    pick_up(m300)
    for col in all_samps:
        m300.aspirate(100, tmb)
        m300.dispense(100, col.top(-1))
    drop_used()

    ctx.pause('\nPlease place plate on shaker for 15 minutes. \
    When ready, replace plate and click RESUME')

    # Add 100uL of Stop Solution
    ctx.comment('\nAdding 100uL of Stop Solution')
    pick_up(m300)
    for col in all_samps:
        m300.aspirate(100, stop_sol)
        m300.dispense(100, col.top(-1))
    drop_used()

    ctx.comment('Protocol complete!')
