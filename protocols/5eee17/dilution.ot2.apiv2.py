import math

metadata = {
    'protocolName': 'HPLC Dilution',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}


def run(ctx):

    [num_extracts, lw_hplc, mixreps_dilution, height_source,
     height_intermediate_asp, height_intermediate_disp,
     height_final] = get_values(  # noqa: F821
        'num_extracts', 'lw_hplc', 'mixreps_dilution', 'height_source',
        'height_intermediate_asp', 'height_intermediate_disp', 'height_final')

    tuberacks_50 = [
        ctx.load_labware('bd_24_tuberack_50ml_green', slot, '50ml tubes')
        for slot in ['1', '2']]
    tuberack_15 = ctx.load_labware('bd_72_tuberack_15ml_orange', '3')
    tuberack_hplc = ctx.load_labware(lw_hplc, '11', 'HPLC tuberack')
    tiprack = [ctx.load_labware('opentrons_96_tiprack_1000ul', '10')]
    p1000l, p1000r = [
        ctx.load_instrument('p1000_single_gen2', mount, tip_racks=tiprack)
        for mount in ['left', 'right']]
    pips = [p1000l, p1000r]

    tip_max = len([well for rack in tiprack for well in rack.wells()])
    tip_count = 0

    def pick_up(pipettes):
        nonlocal tip_count
        for pip in pipettes:
            if tip_count == tip_max:
                ctx.pause('Refill tiprack before resuming.')
                [rack.reset() for rack in tiprack]
                tip_count = 0
            tip_count += 1
            pip.pick_up_tip()

    def mix(pip, reps, vol, loc):
        for _ in range(reps):
            pip.aspirate(vol, loc.bottom(height_intermediate_asp))
            pip.dispense(vol, loc.bottom(height_intermediate_disp))

    refill_map = {
        'source': len(
            [well for rack in tuberacks_50 for well in rack.wells()]),
        'intermediate': len(tuberack_15.wells()),
        'final': len(tuberack_hplc.wells())
    }

    def check_refill(index):
        refill_items = []
        for key, val in refill_map.items():
            if index % val == 0 and index > 0:
                refill_items.append(key)
        if len(refill_items) > 0:
            ctx.pause(f'Please refill {", ".join(refill_items)} tubes before \
resuming.')

    def get_set_index(set_index, tubes_set_type):
        set_index_transform = set_index % \
            math.floor(refill_map[tubes_set_type]/2)
        return set_index_transform

    sources = [
        well for rack in tuberacks_50
        for well in rack.wells()]
    source_sets = [
        sources[i*2:(i+1)*2] if i < math.ceil(len(sources)/2)
        else sources[i*2:]
        for i in range(math.ceil(len(sources)/2))]
    intermediates = [
        well for col in tuberack_15.columns()
        for well in col]
    intermediate_sets = [
        intermediates[i*2:(i+1)*2]
        if i < math.ceil(len(intermediates)/2) - 1
        else intermediates[i*2:]
        for i in range(math.ceil(len(intermediates)/2))]
    finals = [
        well for row in tuberack_hplc.rows()
        for well in row]
    final_sets = [
        finals[i*2:(i+1)*2] if i < math.ceil(len(finals)/2) - 1
        else finals[i*2:]
        for i in range(math.ceil(len(finals)/2))]

    # dilute
    num_sets = math.ceil(num_extracts/2)
    for set_ind in range(num_sets):
        check_refill(set_ind*2)
        source_set = source_sets[get_set_index(set_ind, 'source')]
        intermediate_set = intermediate_sets[
            get_set_index(set_ind, 'intermediate')]
        final_set = final_sets[get_set_index(set_ind, 'final')]
        pick_up([p1000l, p1000r][:len(source_set)])

        for pip, tube in zip(pips, source_set):
            pip.aspirate(500, tube.bottom(height_source))
            pip.air_gap(100)

        for pip, i_tube, f_tube in zip(pips, intermediate_set, final_set):
            pip.dispense(100, i_tube.top())
            pip.dispense(pip.current_volume,
                         i_tube.bottom(height_intermediate_disp))
            mix(pip, mixreps_dilution, 1000, i_tube)
            pip.transfer(800, i_tube.bottom(height_intermediate_asp),
                         f_tube.bottom(height_final),
                         new_tip='never')
        [pip.drop_tip() for pip in [p1000l, p1000r] if pip.has_tip]
