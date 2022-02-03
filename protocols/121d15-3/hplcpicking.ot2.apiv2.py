# metadata
metadata = {
    'protocolName': 'HPLC Picking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [input_file, default_transfer_vol, p300_mount] = get_values(  # noqa: F821
        'input_file', 'default_transfer_vol', 'p300_mount')

    # load labware
    rack = ctx.load_labware('eurofins_96x2ml_tuberack', '2', 'tuberack')
    plates = [
        ctx.load_labware('irishlifesciences_96_wellplate_2200ul', slot,
                         f'plate {i+1}')
        for i, slot in enumerate(['10', '7', '4', '1'])]
    tips300 = [ctx.load_labware('opentrons_96_tiprack_300ul', '11')]

    # pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tips300)

    # parse
    data = [
        line for line in input_file.splitlines()[1:]
        if line and line.split(',')[0].strip()]

    # order
    wells_ordered = [
        well for plate in plates for row in plate.rows() for well in row]
    dests = [well for col in rack.columns() for well in col[:8]]

    def parse_range(content):
        fraction_num = content[:content.index('(')][1:]
        range = [
            int(val) - 1
            for val in content[
                content.index('(')+1:content.index(')')].split('-')]
        num_samples = range[1] - range[0] + 1
        if num_samples < 6:
            raise Exception(
                f'Invalid number of samples for Fraction {fraction_num} \
                ({num_samples})')
        return wells_ordered[range[0]+2:range[0]+6]

    for i, line in enumerate(data):
        sources = parse_range(line)
        dest = dests[i]
        p300.pick_up_tip()
        for s in sources:
            p300.transfer(default_transfer_vol, s.bottom(0.5), dest.top(-1),
                          new_tip='never')
        p300.drop_tip()
