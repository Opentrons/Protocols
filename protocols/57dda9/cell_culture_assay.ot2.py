from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Cell Culture Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
round_name = 'greiner_cellstar_96_round'
if round_name not in labware.list():
    labware.create(
        round_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.85,
        depth=10.76,
        volume=320
    )

culture_name = 'falcon_culture_96_flat'
if culture_name not in labware.list():
    labware.create(
        culture_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.85,
        depth=10.76,
        volume=370
    )

deep_name = 'axygen_24_deepwell'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(6, 4),
        spacing=(17, 17),
        diameter=16,
        depth=40,
        volume=10000
    )

res_name = 'vwr_reservoir_6'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(6, 1),
        spacing=(17, 0),
        diameter=16,
        depth=40,
        volume=40000
    )

# load labware
deep_plates = [
    labware.load(deep_name, slot, 'deepwell plate ' + str(slot))
    for slot in range(1, 5)
]
res = labware.load(res_name, '7', '6-channel reservoir')
tips1000 = labware.load('opentrons_96_tiprack_1000ul', '10')
tips300 = labware.load('opentrons_96_tiprack_300ul', '11')

# pipettes
p1000 = instruments.P1000_Single(mount='left', tip_racks=[tips1000])
m300 = instruments.P300_Multi(mount='right', tip_racks=[tips300])

# reagents
media = [chan for chan in res.wells()[0:4]]


def run_custom_protocol(
        well_plate_96_type: StringSelection('flat', 'round') = 'flat'
):
    plate_type = culture_name if well_plate_96_type == 'flat' else round
    cell_plates = [
        labware.load(plate_type, slot, 'cell plate ' + str(i+1))
        for i, slot in enumerate(['8', '9', '5', '6'])
    ]

    """         Part A: Aliquot Media          """
    for m, plate in zip(media, deep_plates):
        p1000.pick_up_tip()
        p1000.transfer(
            1000,
            m,
            [d.top() for d in plate.columns('1')],
            new_tip='never'
        )
        p1000.transfer(
            900,
            m,
            [d.top() for col in plate.columns()[1:] for d in col],
            new_tip='never'
        )
        p1000.drop_tip()

    robot.pause('Manually add drugs into the first column of each 24-deep \
well plate')

    """         Part B: Serial Dilutions          """
    for plate in deep_plates:
        m300.pick_up_tip()
        source = plate.rows('A')[:5]
        dests = plate.rows('A')[1:]
        for s, d in zip(source, dests):
            m300.mix(5, 250, s)
            m300.blow_out(s.top())
            m300.transfer(50, s, d, new_tip='never')
        m300.mix(5, 250, dests[-1])
        m300.blow_out(dests[-1].top())
        m300.drop_tip()

    robot.pause('Place inside OT-2 the 96-well plates containing the tumor \
cells.')

    """         Part C: Cell Treatment          """
    for plate_ind, plate in enumerate(deep_plates):
        sources = [well for well in plate.rows('A')[::-1]]

        # determine destination plates and wells
        dest_plates = cell_plates[:2] if plate_ind < 2 else cell_plates[2:]
        if plate_ind % 2 == 0:
            dest_sets = [[well for well in plate.rows('A')[5::-1]]
                         for plate in dest_plates]
        else:
            dest_sets = [[well for well in plate.rows('A')[11:5:-1]]
                         for plate in dest_plates]

        m300.pick_up_tip()
        for i, s in enumerate(sources):
            m300.mix(1, 250, s)
            m300.blow_out(s.top())
            m300.distribute(
                50,
                s,
                [d[i] for d in dest_sets],
                new_tip='never',
                disposal_vol=0
            )
        m300.drop_tip()
