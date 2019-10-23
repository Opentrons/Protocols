from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'NGS Library Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        number_of_columns: int=12,
        p50_tiprack_type: StringSelection(
            'opentrons_96_tiprack_300ul',
            'fisherbrand-filter-tiprack-200ul',
            'phenix-filter-tiprack-300ul')='opentrons_96_tiprack_300ul',
        p300_tiprack_type: StringSelection(
            'opentrons_96_tiprack_300ul',
            'fisherbrand-filter-tiprack-200ul',
            'phenix-filter-tiprack-300ul')='opentrons_96_tiprack_300ul',):

    for tiprack_type in [p50_tiprack_type, p300_tiprack_type]:
        if tiprack_type not in labware.list():
            labware.create(
                tiprack_type,
                grid=(12, 8),
                spacing=(9, 9),
                diameter=5,
                depth=60)

    # labware setup
    mag_module = modules.load('magdeck', '4')
    mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
    deep_plate = labware.load('96-deep-well', '7')
    trough = labware.load('trough-12row', '8')

    tipracks_300 = [labware.load(p300_tiprack_type, slot)
                    for slot in ['6', '9', '10', '11']]
    tipracks_50 = [labware.load(p50_tiprack_type, slot)
                   for slot in ['2', '3', ]]

    # instruments setup
    m300 = instruments.P300_Multi(
        mount='right',
        tip_racks=tipracks_300)
    m50 = instruments.P50_Multi(
        mount='left',
        tip_racks=tipracks_50)

    # reagent setup
    speedbeads = deep_plate.cols('1')
    ethanol = trough.wells('A1')
    tle = trough.wells('A2')

    # define sample columns
    sample_cols = mag_plate.cols('1', length=number_of_columns)

    for well in sample_cols:
        m50.transfer(32.3, speedbeads, well, mix_after=(5, 30))

    m50.delay(minutes=5)
    mag_module.engage()
    m50.delay(minutes=2)

    for well in sample_cols:
        m300.transfer(100, well, m300.trash_container.top())
        for _ in range(2):
            m300.pick_up_tip()
            m300.transfer(100, ethanol, well, new_tip='never')
            m300.delay(seconds=1)
            m300.transfer(
                120, well, m300.trash_container.top(), new_tip='never')
            m300.drop_tip()
        mag_module.disengage()
        m50.transfer(17.5, tle, well, mix_after=(3, 10))
        mag_module.engage()
        m50.delay(minutes=2)
