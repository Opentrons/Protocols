import math
import json
import os
from opentrons.types import Point

metadata = {
    'protocolName': 'Zymo-Seq RiboFree™ Total RNA Library Prep Select-a-Size \
MagBead Clean-up (robot 2)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    [number_of_samples, cleanup_stage, p10_mount,
        p300_mount] = get_values(  # noqa: F821
            'number_of_samples', 'cleanup_stage', 'p10_mount', 'p300_mount')
    # [number_of_samples, cleanup_stage, p10_mount, p300_mount] = [
    #     96, 'post-first-strand synthesis and universal depletion', 'right',
    #     'left'
    # ]

    # load modules and labware
    racks10 = [
        ctx.load_labware('opentrons_96_tiprack_10ul', slot)
        for slot in ['1', '4', '5']
    ]
    elution_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '2', 'elution PCR plate')
    reagent_res = ctx.load_labware(
        'nest_12_reservoir_15ml', '3', 'reagent reservoir')
    magdeck = ctx.load_module('magdeck', '6')
    mag_plate = magdeck.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    racks300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['8', '9', '10', '11']
    ]

    # pipettes
    if p10_mount == p300_mount:
        raise Exception('Pipette mounts cannot match.')
    m10 = ctx.load_instrument('p10_multi', p10_mount)
    m300 = ctx.load_instrument('p300_multi', p300_mount)

    file_path = '/data/csv/tip_track.json'
    # file_path = 'protocols/tip_track.json'
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            if 'tips10' in data:
                tip10_count = data['tips10']
            else:
                tip10_count = 0
            if 'tips300' in data:
                tip300_count = data['tips300']
            else:
                tip300_count = 0
    else:
        tip10_count = 0
        tip300_count = 0

    all_tips10 = [tip for rack in racks10 for tip in rack.rows()[0]]
    all_tips300 = [tip for rack in racks300 for tip in rack.rows()[0]]
    tip10_max = len(all_tips10)
    tip300_max = len(all_tips300)

    def pick_up(pip):
        nonlocal tip10_count
        nonlocal tip300_count
        if pip == m10:
            if tip10_count == tip10_max:
                ctx.pause('Replace 10µl tipracks before resuming.')
                tip10_count = 0
                [rack.reset() for rack in racks300]
            pip.pick_up_tip(all_tips10[tip10_count])
            tip10_count += 1
        else:
            if tip300_count == tip300_max:
                ctx.pause('Replace tipracks before resuming.')
                tip300_count = 0
                [rack.reset() for rack in racks300]
            pip.pick_up_tip(all_tips300[tip300_count])
            tip300_count += 1

    # reagents and sample setup
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples (must be 1-96).')
    mag_samples = mag_plate.rows()[0][:math.ceil(number_of_samples/8)]
    elution_samples = elution_plate.rows()[0][:math.ceil(number_of_samples/8)]
    beads = reagent_res.wells()[0]
    wash_buffer = reagent_res.wells()[1:4]
    dna_eb = reagent_res.wells()[4]
    waste = [chan.top() for chan in reagent_res.wells()[6:]]

    # setup cleanup parameters
    if cleanup_stage == 'post-first-strand synthesis and universal depletion':
        start_vol = 75
        bead_vol = 150
        elution_vol = 10
        tempdeck = ctx.load_module('tempdeck', '7')
        # tempplate = tempdeck.load_labware(
        #     'opentrons_96_aluminumblock_nest_wellplate_100ul')
        inc_temp = 95
        inc_time = 5
        end_msg = 'This is a safe stopping point. Cleaned-up DNA can be safely \
stored at ≤ 4°C overnight or ≤ −20°C for up to one week.'
    elif cleanup_stage == 'post-P7 adapter ligation':
        start_vol = 40
        bead_vol = 60
        elution_vol = 10
        inc_temp = None
        inc_time = None
        end_msg = 'This is a safe stopping point. Cleaned-up DNA can be safely \
stored at ≤ 4°C overnight or ≤ −20°C for up to one week.'
    elif cleanup_stage == 'post-P5 adapter ligation':
        start_vol = 100
        bead_vol = 100
        elution_vol = 20
        inc_temp = None
        inc_time = None
        end_msg = 'This is a safe stopping point. Cleaned-up DNA can be safely \
stored at ≤ 4°C overnight or ≤ −20°C for up to one week.'
    elif cleanup_stage == 'post-library index PCR':
        start_vol = 100
        bead_vol = 85
        elution_vol = 20
        inc_temp = None
        inc_time = None
        end_msg = 'The eluate is your final RNA-Seq library 3. Libraries may be \
stored at ≤ 4°C overnight or ≤ -20°C for long-term storage.'

    """ Appendix A: Select-a-Size MagBead Clean-up Protocol """
    # mix and transfer beads
    pick_up(m300)
    for _ in range(10):
        m300.aspirate(250, beads.bottom(2))
        m300.dispense(250, beads.bottom(20))
    for m in mag_samples:
        if not m300.hw_pipette['has_tip']:
            pick_up(m300)
        m300.transfer(
            bead_vol,
            beads,
            m,
            air_gap=30,
            mix_after=(5, bead_vol),
            new_tip='never'
        )
        m300.drop_tip()

    ctx.delay(minutes=5, msg='Incubating at room temperature for 5 minutes')

    # separate beads and remove supernatant
    magdeck.engage()
    ctx.delay(minutes=3, msg='Incubating on magnet for 3 minutes.')
    supernatant_vol = start_vol + bead_vol
    for i, m in enumerate(mag_samples):
        pick_up(m300)
        m300.aspirate(supernatant_vol*1.1, m)
        m300.air_gap(30)
        m300.dispense(supernatant_vol*1.1+30, waste[i//6])
        m300.air_gap(30)
        # m300.transfer(
        #     supernatant_vol*1.1, m, waste[i//6], air_gap=30, new_tip='never')
        m300.drop_tip()

    # 2x washes
    for wash in range(2):
        pick_up(m300)
        for i, m in enumerate(mag_samples):
            chan = (i+wash*12)//8
            m300.transfer(
                200,
                wash_buffer[chan],
                m.top(),
                air_gap=30,
                new_tip='never'
            )
        for i, m in enumerate(mag_samples):
            if not m300.hw_pipette['has_tip']:
                pick_up(m300)
            chan = (i+wash*12)//8
            # m300.transfer(
            #     210,
            #     m,
            #     waste[chan+2],
            #     air_gap=30,
            #     new_tip='never'
            # )
            m300.aspirate(supernatant_vol*1.1, m)
            m300.air_gap(30)
            m300.dispense(supernatant_vol*1.1+30, waste[chan+2])
            m300.air_gap(30)
            m300.drop_tip()

    magdeck.disengage()
    ctx.delay(minutes=3, msg='Airdrying beads for 3 minutes.')

    # resuspend in elution buffer
    for i, m in enumerate(mag_samples):
        side = 1 if i % 2 == 0 else -1
        loc = m.bottom().move(Point(x=side*m.diameter/2*0.9, y=0, z=2))
        pick_up(m10)
        if elution_vol > 10:
            pre_vol = elution_vol - 10
            m10.transfer(pre_vol, dna_eb, m.top(), new_tip='never')
            m10.blow_out(m.top())
        m10.aspirate(10, dna_eb)
        m10.move_to(m.center())
        m10.dispense(10, loc)
        m10.mix(10, 9, m)
        m10.blow_out(m.top(-2))
        m10.air_gap(5)
        m10.drop_tip()

    if inc_temp and inc_time:
        tempdeck.set_temperature(inc_temp)
        # m10.move_to(tempplate.wells()[0].top(10))
        m10.home()
        ctx.pause('Transfer plate from magnetic module to aluminum block on \
temperature module. Once you resume, the plate will incubate for \
' + str(inc_temp) + ' minutes.')
        ctx.delay(minutes=inc_time)
        ctx.pause('Transfer plate back to magnetic module from aluminum block \
on temperature module.')

    magdeck.engage()
    ctx.delay(minutes=3, msg='Incubating on magnet for 3 minutes.')

    # transfer elution to new plate
    for m, e in zip(mag_samples, elution_samples):
        pick_up(m10)
        m10.transfer(elution_vol, m, e, new_tip='never')
        m10.blow_out(e.top(-2))
        m10.air_gap(5)
        m10.drop_tip()

    magdeck.disengage()
    tempdeck.deactivate()
    ctx.comment(end_msg)

    # track final used tip
    if not ctx.is_simulating():
        file_path = '/data/csv/tip_track.json'
        # file_path = '/protocols/tip_track.json'
        if cleanup_stage == 'post-library index PCR':
            data = {
                'tips10': 0,
                'tips300': 0
            }
        else:
            data = {
                'tips10': tip10_count,
                'tips300': tip300_count
            }
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)
