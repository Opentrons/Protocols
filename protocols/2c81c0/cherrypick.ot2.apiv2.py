# metadata
metadata = {
    'protocolName': 'Cherrypicking from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}


def run(ctx):

    csv_input, p10_mount, labware_type = get_values(  # noqa: F821
        'csv_input', 'p10_mount', 'labware_type')
    # csv_input, p10_mount = [
    #     'source plate ,well,volume,destination plate ,well,height \n,,,,\
    #        ,\n1,A2,7,5,A4,-4',
    #     'left'
    # ]

    # labware
    tiprack10 = ctx.load_labware('biotix_96_filtertiprack_10ul', '4')

    # pipette
    p10 = ctx.load_instrument(
        'p10_single', p10_mount, tip_racks=[tiprack10])

    # parse
    data = [
        [val.strip().upper() for val in line.split(',')]
        for line in csv_input.splitlines()
        if line and line.split(',')[0].strip()][1:]

    # loop and perform transfers
    for d in data:
        s_slot, s_well, vol, d_slot, d_well, h_offset = d
        vol, h_offset = float(vol), float(h_offset)
        if int(s_slot) not in ctx.loaded_labwares:
            ctx.load_labware(
                labware_type, s_slot, 'source plate ' + s_slot)
        if int(d_slot) not in ctx.loaded_labwares:
            ctx.load_labware(
                labware_type, d_slot, 'destination plate ' + d_slot)
        source = ctx.loaded_labwares[int(s_slot)].wells_by_name()[s_well]
        dest = ctx.loaded_labwares[int(d_slot)].wells_by_name()[d_well]
        if h_offset > source._depth:
            ctx.pause('Warning: Specified height may result in crashing. \
Press resume to ignore.')

        p10.pick_up_tip()
        p10.transfer(
            vol,
            source.top(h_offset),
            dest.bottom(3),
            new_tip='never'
        )
        p10.blow_out(dest.top(-2))
        p10.drop_tip()
