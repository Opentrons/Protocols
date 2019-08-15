from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'ELISA',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_plate_name = 'VWR-96-deepwell-1ml-tubes'
if deep_plate_name not in labware.list():
    labware.create(
        deep_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=39,
        volume=2000
    )

elisa_plate_name = 'NUNC-MaxiSorp-ELISA-96'
if elisa_plate_name not in labware.list():
    labware.create(
        elisa_plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=11.3,
        volume=350
    )

# load labware
elisa_plates = [
    labware.load(elisa_plate_name, str(slot), 'elisa plate ' + str(slot))
    for slot in range(1, 9)
]
dilution_plate = labware.load(
    deep_plate_name, '9', 'dilution plate with tubes')
accessory_tuberack = labware.load(deep_plate_name, '10', 'accessory tuberack')
tips300 = labware.load('opentrons-tiprack-300ul', '11')

# tube setup
accessory_tubes = [tube for tube in accessory_tuberack.columns('1')]


def run_custom_protocol(
        p300_single_mount: StringSelection('left', 'right') = 'left',
        p300_multi_mount: StringSelection('right', 'left') = 'right'
):
    # check
    if p300_multi_mount == p300_single_mount:
        raise Exception('Input different mount sides for pipettes.')

    # pipettes
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=[tips300])
    m300 = instruments.P300_Multi(
        mount=p300_multi_mount, tip_racks=[tips300])

    # perform dilution on deepwell plate
    m300.pick_up_tip()
    for source, dest in zip(
            dilution_plate.rows('A')[0:11], dilution_plate.rows('A')[1:12]):
        m300.transfer(450, source, dest.top(), new_tip='never')
        m300.blow_out(dest.top())
        m300.mix(5, 200, dest)
        m300.blow_out(dest.top())

    # transfer last dilution to accessory tubes in first column of rack in
    # slot 10
    m300.transfer(
        231.5,
        dilution_plate.wells('A12'),
        accessory_tubes[0],
        new_tip='never'
    )
    m300.blow_out(accessory_tubes[0].top())
    m300.drop_tip()

    p300.start_at_tip(tips300.wells('A2'))

    """ add sample """

    # plates 1-3
    for i, row in enumerate('ABCD'):
        p300.pick_up_tip()
        for col in range(1, 12):
            source = dilution_plate.wells(row+str(col))
            dest_name = 'ACEG'[i] + str(col)
            dests = [well for plate in elisa_plates[0:3]
                     for well in plate.wells(dest_name, length=2)]
            for d in dests:
                p300.transfer(
                    100,
                    source,
                    d,
                    new_tip='never'
                )
                p300.blow_out(d.top())
        p300.drop_tip()

    # plate 4
    for i, row in enumerate('ABCD'):
        p300.pick_up_tip()
        for source_col, dest_col in zip(range(3, 13), range(1, 11)):
            source = dilution_plate.wells(row+str(source_col))
            dest_name = 'ACEG'[i] + str(dest_col)
            dests = [
                well for well in elisa_plates[3].wells(dest_name, length=2)]
            for d in dests:
                p300.transfer(
                    100,
                    source,
                    d,
                    new_tip='never'
                )
                p300.blow_out(d.top())
        acc_source = accessory_tubes[i]
        acc_dests = elisa_plates[3].columns('11')[i*2:i*2+2]
        for d in acc_dests:
            p300.transfer(
                100,
                acc_source,
                d,
                new_tip='never'
            )
            p300.blow_out(d.top())
        p300.drop_tip()

    # plates 5-7
    for i, row in enumerate('EFGH'):
        p300.pick_up_tip()
        for col in range(1, 12):
            source = dilution_plate.wells(row+str(col))
            dest_name = 'ACEG'[i] + str(col)
            dests = [well for plate in elisa_plates[4:7]
                     for well in plate.wells(dest_name, length=2)]
            for d in dests:
                p300.transfer(
                    100,
                    source,
                    d,
                    new_tip='never'
                )
                p300.blow_out(d.top())
        p300.drop_tip()

    # plate 8
    for i, row in enumerate('EFGH'):
        p300.pick_up_tip()
        for source_col, dest_col in zip(range(3, 13), range(1, 11)):
            source = dilution_plate.wells(row+str(source_col))
            dest_name = 'ACEG'[i] + str(dest_col)
            dests = [
                well for well in elisa_plates[7].wells(dest_name, length=2)]
            for d in dests:
                p300.transfer(
                    100,
                    source,
                    d,
                    new_tip='never'
                )
                p300.blow_out(d.top())
        acc_source = accessory_tubes[i+4]
        acc_dests = elisa_plates[7].columns('11')[i*2:i*2+2]
        for d in acc_dests:
            p300.transfer(
                100,
                acc_source,
                d,
                new_tip='never'
            )
            p300.blow_out(d.top())
        p300.drop_tip()
