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
        [val.strip() for val in line.split(',')]
        for line in input_file.splitlines()[1:]
        if line and line.split(',')[0].strip()]

    # order
    wells_ordered = [
        well for plate in plates for row in plate.rows() for well in row]

    for line in data:
        sources = [wells_ordered[int(val)-1] for val in line[:4]]
        dest = rack.wells_by_name()[line[4].upper()]
        if len(line) >= 6 and line[5]:
            vol = float(line[5])
        else:
            vol = default_transfer_vol

        p300.pick_up_tip()
        for s in sources:
            p300.transfer(vol, s.bottom(0.5), dest.top(-1), new_tip='never')
        p300.drop_tip()
