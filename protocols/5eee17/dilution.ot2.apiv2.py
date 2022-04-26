import math

metadata = {
    'protocolName': 'HPLC Dilution',
    'author': 'Nick Diehl <ndiehl@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.12'
}


def run(ctx):

    num_extracts, lw_hplc = get_values(  # noqa: F821
        'num_extracts', 'lw_hplc')

    tuberacks_50 = [
        ctx.load_labware('bd_24_tuberack_50ml_green', slot)
        for slot in ['1', '2']]
    tuberack_15 = ctx.load_labware('bd_72_tuberack_15ml_orange', '3')
    tuberack_hplc = ctx.load_labware(lw_hplc, '11', 'HPLC tuberack')
    tiprack = [ctx.load_labware('opentrons_96_tiprack_1000ul', '10')]
    p1000l, p1000r = [
        ctx.load_instrument('p1000_single_gen2', mount, tip_racks=tiprack)
        for mount in ['left', 'right']]
    pips = [p1000l, p1000r]

    # create proper order
    num_sets = math.ceil(num_extracts/2)
    sources = [
        well for rack in tuberacks_50 for well in rack.wells()][:num_extracts]
    source_sets = [
        sources[i*2:(i+1)*2] if i < num_sets - 1 else sources[i*2:]
        for i in range(num_sets)]
    intermediates = [
        well for col in tuberack_15.columns()
        for well in col[:8]][:num_extracts]
    intermediate_sets = [
        intermediates[i*2:(i+1)*2]
        if i < num_sets - 1 else intermediates[i*2:] for i in range(num_sets)]
    finals = [
        well for row in tuberack_hplc.rows()[::-1]
        for well in row][:num_extracts]
    final_sets = [
        finals[i*2:(i+1)*2] if i < num_sets - 1 else finals[i*2:]
        for i in range(num_sets)]

    def mix(pip, reps, vol, loc):
        for _ in range(reps):
            pip.aspirate(vol, loc.bottom(5))
            pip.dispense(vol, loc.center())

    # dilute
    for set_ind in range(num_sets):
        [pip.pick_up_tip()
         for pip in [p1000l, p1000r][:len(source_sets[set_ind])]]

        for pip, tube in zip(pips, source_sets[set_ind]):
            pip.aspirate(700, tube.bottom(5))
            pip.air_gap(100)

        for pip, i_tube, f_tube in zip(pips, intermediate_sets[set_ind],
                                       final_sets[set_ind]):
            pip.dispense(100, i_tube.top())
            pip.dispense(pip.current_volume, i_tube.bottom(5))
            mix(pip, 5, 1000, i_tube)
            pip.transfer(800, i_tube.bottom(5), f_tube.bottom(5),
                         new_tip='never')
        [pip.drop_tip() for pip in [p1000l, p1000r] if pip.has_tip]
