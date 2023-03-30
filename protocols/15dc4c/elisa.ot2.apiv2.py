import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'SMC IL-17A High Sensitivity Immunoassay Kit',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.13'
}

DO_MIX = True
DO_INCUBATIONS = True


def run(ctx):

    [num_samples, mount_m300, m20] = get_values(  # noqa: F821
        'num_samples', 'mount_m300', 'mount_m20')

    elution_plate = ctx.load_labware('nunc_384_wellplate_100ul', '1',
                                     'elution plate')
    sample_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '2',
                                    'sample preparation plate')
    standard_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '4',
                                      'standards plate')
    assay_plate = ctx.load_labware('nest_96_wellplate_2ml_deep', '5',
                                   'assay plate')
    assay_plate_on_magnet = ctx.load_labware('nest_96_wellplate_2ml_deep', '7',
                                             'sphere mag plate')
    reservoir = ctx.load_labware('nest_12_reservoir_15ml', '8',
                                 'reagents')
    tipracks200 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['10', '11']]
    tipracks20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['3', '6', '9']]

    # pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', 'left',
                               tip_racks=tipracks200)
    m20 = ctx.load_instrument('p20_multi_gen2', 'right', tip_racks=tipracks20)

    def pick_up(pip):
        try:
            pip.pick_up_tip()
        except protocol_api.labware.OutOfTipsError:
            ctx.pause(
                f'Replace P{pip.max_volume} pipette tips before resuming.')
            pip.reset_tipracks()
            pip.pick_up_tip()

    def slow_withdraw(pip, well, delay_seconds=2):
        ctx.delay(seconds=delay_seconds)
        ctx.max_speeds['A'] = 25
        ctx.max_speeds['Z'] = 25
        pip.move_to(well.top())
        del ctx.max_speeds['A']
        del ctx.max_speeds['Z']

    # reagents
    num_cols = math.ceil(num_samples/5)

    standard_diluent = reservoir.rows()[0][0]
    sample_diluent = reservoir.rows()[0][1]
    coated_beads = reservoir.rows()[0][2]
    detection_antibody = reservoir.rows()[0][3]
    elution_buffer_b = reservoir.rows()[0][4]
    buffer_d = reservoir.rows()[0][5]
    samples = sample_plate.rows()[0][:num_cols]

    """
    Create and plate standards
    """
    # single tip with P300
    default_current = 0.8
    current_modifier = 1/8
    current = default_current*current_modifier
    ctx._hw_manager.hardware._attached_instruments[
        m300._implementation.get_mount()
        ].update_config_item('pick_up_current', current)

    tip = m300.tip_racks[-1].rows()[-1][-1]
    standard_dest_sets = [col[:3] for col in assay_plate.columns()]
    standard_dil_vols = [1000]*3 + [500]*8

    m300.pick_up_tip(tip)

    # pre-add diluent
    for vol, d in zip(standard_dil_vols, standard_plate.rows()[0][1:]):
        num_trans = math.ceil(vol/tip.max_volume)
        vol_per_trans = round(vol/num_trans, 1)
        for _ in range(num_trans):
            m300.aspirate(vol_per_trans, standard_diluent)
            slow_withdraw(m300, standard_diluent)
            m300.dispense(vol, d.bottom(2))
            slow_withdraw(m300, d)

    # perform dilution
    for s, d in zip(standard_plate.rows()[0][:10],
                    standard_plate.rows()[0][1:11]):
        num_trans = math.ceil(500/tip.max_volume)
        vol_per_trans = round(vol/num_trans, 1)
        for n in range(num_trans):
            m300.aspirate(vol_per_trans, s.bottom(2))
            slow_withdraw(m300, s)
            m300.dispense(vol_per_trans, d.bottom(2))
            if n == num_trans - 1 and DO_MIX:
                m300.mix(5, 100, d.bottom(2))

    # transfer to assay plate
    for s, dest_set in zip(standard_plate.rows()[0], standard_dest_sets):
        for d in dest_set:
            m300.aspirate(100, s.bottom(2))
            slow_withdraw(m300, s)
            m300.dispense(100, d.bottom(2))
            slow_withdraw(m300, d)

    m300.drop_tip()

    """
    Dilute and transfer samples to assay plate
    """
    current_modifier = 5/8
    current = default_current*current_modifier
    ctx._hw_manager.hardware._attached_instruments[
        m300._implementation.get_mount()
        ].update_config_item('pick_up_current', current)

    tips_offset = [
        col[3] if i < 11 else col[2]
        for i, col in enumerate(m300.tip_racks[-1].columns())]

    sample_dests = assay_plate.rows()[3][:num_cols]
    for tip, s, d in zip(tips_offset, samples, sample_dests):
        m300.pick_up_tip(tip)
        m300.aspirate(200, sample_diluent)
        slow_withdraw(m300, sample_diluent)
        m300.dispense(200, s.bottom(2))
        if DO_MIX:
            m300.mix(5, 100, s.bottom(2))
        m300.aspirate(100, s.bottom(2))
        slow_withdraw(m300, s)
        m300.dispense(100, d.bottom(2))
        slow_withdraw(m300, d)
        m300.drop_tip()

    """
    Add coated beads
    """
    standards_and_samples = assay_plate.rows()[0][:2+num_cols]
    pick_up(m300)
    for i, d in enumerate(standards_and_samples):
        # pre-air_gap
        m300.aspirate(20, coated_beads.top())
        if i == 0 and DO_MIX:
            m300.mix(5, 100, coated_beads)
        m300.aspirate(100, coated_beads)
        slow_withdraw(m300, coated_beads)
        m300.dispense(m300.current_volume, d.top())
    m300.drop_tip()

    ctx.pause('Proceed with Target Capture incubation and Post-Capture Wash.')

    """
    Detection
    """
    standards_and_samples = assay_plate_on_magnet.rows()[0][:2+num_cols]
    for d in standards_and_samples:
        pick_up(m20)
        m20.aspirate(20, detection_antibody)
        slow_withdraw(m20, detection_antibody)
        m20.dispense(20, d.bottom(2))
        slow_withdraw(m20, d)
        m20.drop_tip()

    ctx.pause('Proceed with Detection incubation and Post-Detection Wash \
and Shake.')

    """
    Elution
    """
    for d in standards_and_samples:
        pick_up(m20)
        m20.aspirate(15, elution_buffer_b)  # reverse pipetting
        slow_withdraw(m20, elution_buffer_b)
        m20.dispense(10, d.bottom(1.5))
        slow_withdraw(m20, d)
        m20.drop_tip()

    ctx.pause('Proceed with Elution incubation')

    # add buffer D to elution plate
    elution_dests = elution_plate.rows()[0]
    pick_up(m20)
    m20.aspirate(5, buffer_d)
    for d in elution_dests:
        m20.aspirate(10, buffer_d)  # reverse pipetting
        slow_withdraw(m20, buffer_d)
        m20.dispense(10, d.bottom(1.5))
        slow_withdraw(m20, d)

    # void extra volume
    m20.dispense(m20.current_volume, buffer_d)
    slow_withdraw(m20, buffer_d)

    m20.flow_rate.aspirate /= 10
    for s, d in zip(standards_and_samples, elution_dests):
        if not m20.has_tip:
            pick_up(m20)
        m20.aspirate(10, s.bottom(0.5))
        slow_withdraw(m20, s)
        m20.dispense(10, d.bottom(1))
        slow_withdraw(m20, d)
        m20.drop_tip()

    m20.flow_rate.aspirate *= 10

    ctx.comment('Proceed with plate reading.')
