from opentrons import labware, instruments

metadata = {
    'protocolName': 'Cell Culture Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
res_name = 'sorenson_1_reservoir'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=70,
        depth=36,
        volume=200000
    )

# load labware
media = labware.load(res_name, '7', 'media').wells(0)
tips300 = labware.load('opentrons_96_tiprack_300ul', '10')
waste = labware.load(res_name, '11', 'waste').wells(0).top()

# pipettes
m300l = instruments.P300_Multi(mount='left')
m300r = instruments.P300_Multi(mount='right')


def run_custom_protocol(
        number_of_plates: int = 8
):
    # check
    if number_of_plates > 8 or number_of_plates < 1:
        raise Exception('Invalid number of plates.')

    slots = [str(i) for i in range(9, 0, -1)]
    slots.remove('7')
    plates = [
        labware.load(
            'corning_96_wellplate_360ul_flat',
            slot,
            'plate ' + str(i+1)
        )
        for i, slot in enumerate(slots)
    ][:number_of_plates]

    loc_sets_l = [
        plate.rows('A')[i*6:i*6+3]
        for plate in plates
        for i in range(2)
    ]
    loc_sets_r = [
        plate.rows('A')[i*6+3:i*6+6]
        for plate in plates
        for i in range(2)
    ]

    m300l.pick_up_tip(tips300.wells('A1'))
    m300r.pick_up_tip(tips300.wells('A2'))
    for set_l, set_r in zip(loc_sets_l, loc_sets_r):
        for well in set_l:
            m300l.aspirate(100, well)
        for well in set_r:
            m300r.aspirate(100, well)
        m300l.dispense(300, waste)
        m300l.blow_out()
        m300r.dispense(300, waste)
        m300r.blow_out()
    m300l.drop_tip()
    m300r.drop_tip()

    m300l.pick_up_tip(tips300.wells('A3'))
    m300r.pick_up_tip(tips300.wells('A4'))
    for set_l, set_r in zip(loc_sets_l, loc_sets_r):
        m300l.aspirate(300, media)
        m300r.aspirate(300, media)
        for well in set_l:
            m300l.dispense(100, well.top())
        for well in set_r:
            m300r.dispense(100, well.top())
        m300l.blow_out(waste)
        m300r.blow_out(waste)
    m300l.drop_tip()
    m300r.drop_tip()
