# metadata
metadata = {
    'protocolName': 'HPLC Picking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def run(ctx):

    [input_file, replacement_vol, plate_type,
     p300_mount] = get_values(  # noqa: F821
        'input_file', 'replacement_vol', 'plate_type', 'p300_mount')

    # load labware
    racks = [
        ctx.load_labware('aluminumblock_48_tuberack_2000ul', f'{slot}',
                         f'rack {i+1}')
        for i, slot in enumerate(['1', '4', '2', '5'])]
    plate = ctx.load_labware(plate_type, '3')
    tips300 = [
        ctx.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['6', '9', '7', '8']]

    # pipette
    p300 = ctx.load_instrument('p300_single_gen2', p300_mount,
                               tip_racks=tips300)

    # parse
    data = [
        [val.strip() for val in line.split(',')]
        for line in input_file.splitlines()[3:]
        if line and line.split(',')[0].strip()]

    tubes_ordered = [
        well for rack in racks for row in rack.rows()[::-1] for well in row]

    for line in data:
        tube = tubes_ordered[int(line[0])-1]
        well = plate.wells()[int(line[1])-1]
        if len(line) >= 3 and line[3]:
            vol = float(line[3])
        else:
            vol = replacement_vol

        # remove contents of well
        p300.pick_up_tip()
        ctx.max_speeds['A'] = 100  # slow descent
        ctx.max_speeds['Z'] = 100  # slow descent

        p300.aspirate(vol, well.bottom())
        del ctx.max_speeds['A']  # reset to default
        del ctx.max_speeds['Z']  # reset to default
        p300.drop_tip()

        # transfer tube to well
        p300.transfer(replacement_vol, tube, well.top(-1))
