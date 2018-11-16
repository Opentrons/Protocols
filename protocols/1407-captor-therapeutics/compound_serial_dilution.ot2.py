from opentrons import labware, instruments
from otcustomizers import StringSelection

# labware setup
trough = labware.load('trough-12row', '1')
plate = labware.load('96-flat', '2')
tiprack = labware.load('opentrons-tiprack-300ul', '5')


# pipette setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])

p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack])

# reagent setup
buffer = trough.wells('A1')


def run_custom_protocol(
        sample_container: StringSelection(
            'opentrons-tuberack-2ml-eppendorf',
            'opentrons-tuberack-2ml-screwcap',
            'opentrons-tuberack-15ml',
            'trough-12row')='opentrons-tuberack-2ml-eppendorf'):

    sample_container = labware.load(sample_container, '3')

    # define volumes and distribute buffer
    vol = [90 if index == 10 else 50 for index in range(len(plate.cols()))]
    m300.distribute(vol, buffer, plate.cols())

    # transfer samples to column 11
    p50.start_at_tip(tiprack.wells('A2'))
    for index, well in enumerate(plate.cols('11')):
        p50.transfer(
            10,
            sample_container.wells(index),
            well,
            mix_after=(5, 50))

    # serial dilution from column 11 to column 1
    m300.start_at_tip(tiprack.cols('3'))
    m300.pick_up_tip()
    m300.transfer(
        50,
        plate.cols[10:0:-1],
        plate.cols[9::-1],
        mix_after=(5, 50),
        new_tip='never')
    m300.transfer(
        50,
        plate.cols('1'),
        m300.trash_container.top(),
        new_tip='never')
    m300.drop_tip()
