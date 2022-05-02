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

    def mix(pip, reps, vol, loc):
        for _ in range(reps):
            pip.aspirate(vol, loc.bottom(5))
            pip.dispense(vol, loc.center())

    # create proper order
    max_extracts_per_refill = sum([len(rack.wells()) for rack in tuberacks_50])
    num_refills = math.ceil(num_extracts/max_extracts_per_refill)
    for refill_ind in range(num_refills):
        if refill_ind < num_refills - 1:
            num_extracts_refill = max_extracts_per_refill
        else:
            num_extracts_refill = num_extracts % 48 if num_extracts % 48 != 0 \
                else 48
        num_sets = math.ceil(num_extracts_refill/2)
        sources = [
            well for rack in tuberacks_50
            for well in rack.wells()][:num_extracts_refill]
        source_sets = [
            sources[i*2:(i+1)*2] if i < num_sets - 1 else sources[i*2:]
            for i in range(num_sets)]
        intermediates = [
            well for col in tuberack_15.columns()
            for well in col[:8]][:num_extracts_refill]
        intermediate_sets = [
            intermediates[i*2:(i+1)*2]
            if i < num_sets - 1 else intermediates[i*2:]
            for i in range(num_sets)]
        finals = [
            well for row in tuberack_hplc.rows()
            for well in row][:num_extracts_refill]
        final_sets = [
            finals[i*2:(i+1)*2] if i < num_sets - 1 else finals[i*2:]
            for i in range(num_sets)]

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

        ctx.comment(f'Extract set {refill_ind+1} out of {num_refills} \
complete.')
        if refill_ind < num_refills - 1:
            ctx.pause(f'Please refill all tubes on the deck for the next \
extract set ({refill_ind+2} out of {num_refills}).')
