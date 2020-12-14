import math

# metadata
metadata = {
    'protocolName': 'Cherrypicking from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    csv_input, p10_mount, p300_mount, change_tips = get_values(  # noqa: F821
        'csv_input', 'p10_mount', 'p300_mount', 'change_tips')
#     csv_input, p10_mount = [
#         'source labware,source slot,source well,volume,destination labware,\
# destination slot,destination well,height offset from top of source well \
# (mm)\nplate,1,A2,7,tuberack,5,A4,-4\nplate,2,H10,9,tuberack,3,D1,-4', 'left']

    # labware
    tiprack10 = [ctx.load_labware('biotix_96_filtertiprack_10ul', slot)
                 for slot in ['4', '9']]
    tiprack300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
                  for slot in ['7', '8']]

    # pipette
    p10 = ctx.load_instrument(
        'p10_single', p10_mount, tip_racks=tiprack10)
    p300 = ctx.load_instrument(
        'p300_single', p300_mount, tip_racks=tiprack300)

    # parse
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in csv_input.splitlines()
        if line and line.split(',')[0].strip()][1:]

    # loop and perform transfers
    labware_load_dict = {
        'plate': 'biorad_96_wellplate_200ul_pcr',
        'tuberack': 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        'deepplate': 'nest_96_wellplate_2ml_deep'
    }
    for d in data:
        s_lw, s_slot, s_well, vol, d_lw, d_slot, d_well, h_offset, vol_mix = d
        vol, h_offset, vol_mix = float(vol), float(h_offset), float(vol_mix)
        s_lw, d_lw = s_lw.lower().strip(), d_lw.lower().strip()
        if int(s_slot) not in ctx.loaded_labwares:
            ctx.load_labware(
                labware_load_dict[s_lw], s_slot, 'source plate ' + s_slot)
        if int(d_slot) not in ctx.loaded_labwares:
            ctx.load_labware(
                labware_load_dict[d_lw], d_slot, 'destination plate ' + d_slot)
        source = ctx.loaded_labwares[int(s_slot)].wells_by_name()[s_well]
        dest = ctx.loaded_labwares[int(d_slot)].wells_by_name()[d_well]
        if h_offset > source.geometry._depth:
            ctx.pause('Warning: Specified height may result in crashing. \
Press resume to ignore.')

        pip = p300 if vol > 30 else p10
        num_trans = math.ceil(vol/pip.max_volume)
        vol_per_trans = vol/num_trans
        if change_tips == 'once per well':
            pip.pick_up_tip()
        for _ in range(num_trans):
            if change_tips == 'always':
                pip.pick_up_tip()
            if vol_mix != 0:
                pip.transfer(
                    vol_per_trans,
                    source.top(h_offset),
                    dest.bottom(-1),
                    mix_after=(3, vol_mix),
                    new_tip='never'
                )
            else:
                pip.transfer(
                    vol_per_trans,
                    source.top(h_offset),
                    dest.bottom(-1),
                    new_tip='never'
                )
            pip.blow_out(dest.top(-8))
            pip.touch_tip(v_offset=-6)
            if change_tips == 'always':
                pip.drop_tip()
        if change_tips == 'once per well':
            pip.drop_tip()
