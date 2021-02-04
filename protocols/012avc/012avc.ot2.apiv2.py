metadata = {
    'protocolName': 'Example',
    'author': 'Sakib <sakib.hossain@opentrons.com>',
    'description': 'Custom Protocol Request',
    'apiLevel': '2.8'
}


def run(protocol):

    [p1000_mount] = get_values(  # noqa: F821
        "p1000_mount")

    # Load Tip Racks
    tipracks_1000ul = [protocol.load_labware(
        'opentrons_96_filtertiprack_1000ul', slot) for slot in ['2']]

    # Load Plates
    plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1)

    # Load Instruments
    p1000 = protocol.load_instrument('p1000_single_gen2', p1000_mount,
                                     tip_racks=tipracks_1000ul)

    p1000.transfer(100, plate['A1'], plate['A2'])
