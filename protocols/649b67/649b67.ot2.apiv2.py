from protocol_api import ProtocolContext

metadata = {
    'protocolName': 'Cherrypicking with multiple pipettes and modules',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "transfer_csv":"",
                                  "deck_setup_csv":"",
                                  "left_mount_pipette_type":"p20_single_gen2",
                                  "right_mount_pipette_type":"p300_single_gen2",
                                  "left_tip_type":"standard",
                                  "right_tip_type":"standard",
                                  "tip_reuse":"always",
                                  "left_pip_tiprack_slots":"10,11",
                                  "right_pip_tiprack_slots":"5,8"
                                  }
                                  """)  # noqa: E501 Do not report 'line too long' warnings
    return [_all_values[n] for n in names]


def run(ctx: ProtocolContext):

    [transfer_csv,
     deck_setup_csv,
     left_mount_pipette_type,
     right_mount_pipette_type,
     left_tip_type,
     right_tip_type,
     tip_reuse,
     left_pip_tiprack_slots,
     right_pip_tiprack_slots] = get_values(  # noqa: F821
     "transfer_csv",
     "deck_setup_csv",
     "left_mount_pipette_type",
     "right_mount_pipette_type",
     "left_tip_type",
     "right_tip_type",
     "tip_reuse",
     "left_pip_tiprack_slots",
     "right_pip_tiprack_slots")

    tiprack_map = {
        'p10_single': {
            'standard': 'opentrons_96_tiprack_10ul',
            'filter': 'opentrons_96_filtertiprack_20ul'
        },
        'p50_single': {
            'standard': 'opentrons_96_tiprack_300ul',
            'filter': 'opentrons_96_filtertiprack_200ul'
        },
        'p300_single': {
            'standard': 'opentrons_96_tiprack_300ul',
            'filter': 'opentrons_96_filtertiprack_200ul'
        },
        'p1000_single': {
            'standard': 'opentrons_96_tiprack_1000ul',
            'filter': 'opentrons_96_filtertiprack_1000ul'
        },
        'p20_single_gen2': {
            'standard': 'opentrons_96_tiprack_20ul',
            'filter': 'opentrons_96_filtertiprack_20ul'
        },
        'p300_single_gen2': {
            'standard': 'opentrons_96_tiprack_300ul',
            'filter': 'opentrons_96_filtertiprack_200ul'
        },
        'p1000_single_gen2': {
            'standard': 'opentrons_96_tiprack_1000ul',
            'filter': 'opentrons_96_filtertiprack_1000ul'
        }
    }

    # load labware
    transfer_info = [[val.strip().lower() for val in line.split(',')]
                     for line in transfer_csv.splitlines()
                     if line.split(',')[0].strip()][1:]
    for line in transfer_info:
        s_lw, s_slot, d_lw, d_slot = line[:2] + line[4:6]
        for slot, lw in zip([s_slot, d_slot], [s_lw, d_lw]):
            if not int(slot) in ctx.loaded_labwares:
                ctx.load_labware(lw.lower(), slot)

    # load tipracks in defined slots
    tiprack_type = tiprack_map[pipette_type][tip_type]
    tipracks = []
    for slot in range(1, 13):
        if slot not in ctx.loaded_labwares:
            tipracks.append(ctx.load_labware(tiprack_type, str(slot)))

    # load pipette(s)
    pip = ctx.load_instrument(pipette_type, pipette_mount, tip_racks=tipracks)

    tip_count = 0
    tip_max = len(tipracks*96)

    def pick_up():
        nonlocal tip_count
        if tip_count == tip_max:
            ctx.pause('Please refill tipracks before resuming.')
            pip.reset_tipracks()
            tip_count = 0
        pip.pick_up_tip()
        tip_count += 1

    def parse_well(well):
        letter = well[0]
        number = well[1:]
        return letter.upper() + str(int(number))

    if tip_reuse == 'never':
        pick_up()
    for line in transfer_info:
        _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
        source = ctx.loaded_labwares[
            int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
        dest = ctx.loaded_labwares[
            int(d_slot)].wells_by_name()[parse_well(d_well)]
        if tip_reuse == 'always':
            pick_up()
        pip.transfer(float(vol), source, dest, new_tip='never')
        if tip_reuse == 'always':
            pip.drop_tip()
    if pip.hw_pipette['has_tip']:
        pip.drop_tip()
