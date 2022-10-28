import json
import os

metadata = {
    'protocolName': 'Liquid Transfer',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}

TIP_TRACK = True


def run(ctx):

    plates = [ctx.load_labware(
        'nest_96_wellplate_200ul_flat', str(slot), f'plate {slot}')
        for slot in range(1, 10)]
    reservoir = ctx.load_labware('nest_1_reservoir_195ml', '10')
    tiprack = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '11')]

    m300 = ctx.load_instrument('p300_multi_gen2', 'right', tip_racks=tiprack)
    m300.flow_rate.aspirate = 300
    m300.flow_rate.dispense = 300

    sivi_1 = reservoir.wells()[0]

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}

    folder_path = '/data/liquid_transfer'
    tip_file_path = folder_path + '/tip_log.json'
    if TIP_TRACK and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def _pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log[pip]['tips'][tip_log[pip]['count']])
            tip_log[pip]['count'] += 1

    # liquid transfers
    _pick_up(m300)
    for plate in plates:
        for d in plate.rows()[0]:
            m300.aspirate(20, sivi_1.top())
            m300.aspirate(100, sivi_1.bottom(1))
            m300.dispense(m300.current_volume, d.bottom(6.5))
    m300.drop_tip()

    # track final used tip
    if TIP_TRACK and not ctx.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
