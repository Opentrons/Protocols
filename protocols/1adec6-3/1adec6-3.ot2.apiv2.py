metadata = {
    'protocolName': 'Transfer Small Molecules [3/7]',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):
    [mnt20, numPlates] = get_values(  # noqa: F821
     'mnt20', 'numPlates')

    # load labware
    tips = [
        protocol.load_labware(
            'opentrons_96_tiprack_20ul', s) for s in [4, 7, 10]
            ]

    m20 = protocol.load_instrument('p20_multi_gen2', mnt20, tip_racks=tips)

    srcPlate = protocol.load_labware('thermofast_96_wellplate_200ul', '5')
    finalPlates = [
        protocol.load_labware(
            'spl_96_wellplate_200ul_flat', s) for s in [1, 2, 3]
        ][:numPlates]

    for plate in finalPlates:
        for src, dest in zip(srcPlate.rows()[0][:10], plate.rows()[0][:10]):
            m20.transfer(1, src, dest, mix_before=(5, 10))
