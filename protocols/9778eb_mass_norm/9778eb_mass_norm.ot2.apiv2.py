"""OPENTRONS."""
import math
import csv

metadata = {
    'protocolName': 'Normalization',
    'author': 'Opentrons <protocols@opentrons.com>',
    'apiLevel': '2.12'
}


def run(ctx):
    """PROTOCOL."""
    [num_samples, vol_water, conc_target,
     p20_mount, file_input] = get_values(  # noqa: F821
        'num_samples', 'vol_water', 'conc_target', 'p20_mount', 'file_input')

    source_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                    '1')
    dest_plate = ctx.load_labware('nest_96_wellplate_100ul_pcr_full_skirt',
                                  '2')
    reagent_tubes = ctx.load_labware('opentrons_10_tuberack_falcon_4x50ml_'
                                     '6x15ml_conical', '3')

    # Reagents and Well Lists

    nfw_source = reagent_tubes.wells()[0]
    source_wells = source_plate.wells()[:num_samples]
    dest_wells = dest_plate.wells()[:num_samples]
    # parse
    data = [
        [val.strip() for val in line.split(',')]
        for line in file_input.splitlines()[1:]
        if line and line.split(',')[0].strip()]

    tips20 = [ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
              for slot in ['7', '10'][:math.ceil(len(data)/48)]]
    p20 = ctx.load_instrument('p20_single_gen2', p20_mount, tip_racks=tips20)

    sample_mass = []
    sample_vol = []
    start_conc = []
    # doing it by nmols adds one extra calc and field if starting w/weight
    for mass, vol in zip(sample_mass, sample_vol):
        start_conc.append(mass/vol)
    # final conc can be calculated, set by variable, or imported via CSV
    # depending on what client says
    final_conc = 1  # ngrams/uL
    tot_vol = 30
    transfer_vol = []
    nfw_vol = []
    for final, start in zip(final_conc, start_conc):
        transfer_vol.append(round(final/start, 1))
    for vol in transfer_vol:
        nfw_vol.append(tot_vol-vol)

    # liquid height tracking
    v_naught_dil = vol_water*1000
    radius = reagent_tubes.wells()[0].diameter/2
    h_naught_water = 0.85*v_naught_dil/(math.pi*radius**2)
    h = h_naught_water

    def adjust_height(vol):
        nonlocal h
        dh = vol/(math.pi*radius**2)
        h -= dh
        if h < 12:
            h = 1

    # do NFW addition first to save tips, mix after sample addition
    p20.pick_up_tip()
    for nfw, d in zip(nfw_vol, dest_wells):
        p20.transfer(nfw, nfw_source.bottom(h), d)
        adjust_height(nfw)
    p20.drop_tip()

    for t_vol, s, d in (transfer_vol, source_wells, dest_wells):
        p20.pick_up_tip()
        p20.transfer(t_vol, s, d)
        p20.mix(tot_vol/2, d)
        p20.drop_tip()

    # bad_list = [well.display_name.split(' ')[0] for well in bad_wells]
    # if len(bad_list) > 0:
    #     bad_msg = '\n\n'.join(bad_list)
    #     ctx.comment(f'The following sample wells failed: \n\n{bad_msg}')
