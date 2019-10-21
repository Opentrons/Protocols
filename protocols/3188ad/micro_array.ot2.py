from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Micro Array: 96-well to 384-well plate',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plates_96 = [
    labware.load(
        'biorad_96_wellplate_200ul_pcr',
        str(slot),
        '96-well source plate #' + str(slot))
    for slot in range(1, 5)
]
plate_384 = labware.load(
    'corning_384_wellplate_112ul_flat', '5', '384-well destination plate')


def run_custom_protocol(
        p50_multi_mount: StringSelection('right', 'left') = 'right',
        transfer_volume_in_ul: float = 5,
        tip_strategy: StringSelection('same tip', 'new tips') = 'same tip',
        tip_column: int = 1
):
    # check
    if tip_column < 1 or tip_column > 12:
        raise Exception('Invalid tip column')

    # pipette and tipracks
    if tip_strategy == 'same tip':
        tipracks = labware.load('opentrons_96_tiprack_300ul', '6')
        m50 = instruments.P50_Multi(mount=p50_multi_mount)
    else:
        tipracks = [
            labware.load('opentrons_96_tiprack_300ul', str(slot))
            for slot in range(6, 10)
        ]
        m50 = instruments.P50_Multi(mount=p50_multi_mount, tip_racks=tipracks)

    # setup sources and destinations
    sources = [well for plate in plates_96 for well in plate.rows('A')]
    dests = [well for row in ['A', 'B'] for well in plate_384.rows(row)]

    # perform transfers
    if tip_strategy == 'same tip':
        m50.pick_up_tip(tipracks.rows('A')[tip_column])
    for s, d in zip(sources, dests):
        if tip_strategy == 'new tips':
            m50.pick_up_tip()
        m50.transfer(transfer_volume_in_ul, s, d.bottom(2), new_tip='never')
        m50.blow_out()
        if tip_strategy == 'new tips':
            m50.return_tip()
    if m50.tip_attached:
        m50.return_tip()
