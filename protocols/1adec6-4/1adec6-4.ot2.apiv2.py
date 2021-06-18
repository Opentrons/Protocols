metadata = {
    'protocolName': 'Transfer Small Molecules - CSV Input [4/7]',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):
    [mnt20, transferCSV] = get_values(  # noqa: F821
     'mnt20', 'transferCSV')

    # Load Labware
    tips = [
        protocol.load_labware(
            'opentrons_96_tiprack_20ul', s) for s in [4, 7, 10]
            ]

    p20 = protocol.load_instrument('p20_single_gen2', mnt20, tip_racks=tips)

    srcPlate = protocol.load_labware('thermofast_96_wellplate_200ul', '1')
    destPlate = protocol.load_labware('spl_96_wellplate_200ul_flat', '2')

    # Parse CSV; Each line should be --> Src Well, Vol, Dest Well
    data = [r.split(',') for r in transferCSV.strip().splitlines() if r][1:]

    # Make transfers based on CSV
    for line in data:
        src, vol, dest = line
        p20.transfer(
            float(vol), srcPlate[src], destPlate[dest], mix_before=(5, 15))
