from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Spheroid Transfer',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_96_name = 'inspheroakura_96_wellplate'
if plate_96_name not in labware.list():
    labware.create(
        plate_96_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=9.3,
        volume=70
    )

plate_384_name = 'inspheroakura_384_wellplate'
if plate_384_name not in labware.list():
    labware.create(
        plate_384_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=1.6,
        depth=1.3,
        volume=2
    )

# load labware
akura_96 = [
    labware.load(plate_96_name, slot, 'Akura 96 plate ' + str(i+1))
    for i, slot in enumerate(['1', '4', '7', '10'])
]
akura_384 = [
    labware.load(plate_384_name, slot, 'Akura 384 flow plate ' + str(i+1))
    for i, slot in enumerate(['2', '5', '8', '11'])
]
prep_res = labware.load(plate_96_name, '6', 'prep reservoir')
tips300 = labware.load('opentrons_96_tiprack_300ul', '9')

# reagents
serum = prep_res.wells('A1')
wash_buff = prep_res.wells('A2')


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        aspirate_speed_in_ul_per_sec: float = 150,
        dispense_speed_in_ul_per_sec: float = 300,
        spheroid_release_waiting_time_in_seconds: int = 30
):
    # pipette
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=[tips300])
    m300.set_flow_rate(
        aspirate=aspirate_speed_in_ul_per_sec,
        dispense=dispense_speed_in_ul_per_sec
    )

    # spheroid transfer
    for s_plate, d_plate in zip(akura_96, akura_384):
        m300.pick_up_tip()

        # tip coating
        m300.mix(3, 70, serum)
        m300.blow_out(serum.top())

        # tip washing
        m300.mix(3, 70, wash_buff)
        m300.blow_out(wash_buff.top())

        # plate location setup
        aspirate_locs = [well for well in s_plate.rows('A')]
        dispense_locs = [
            well for set in [
                d_plate.rows(row)[ind:ind+1] for ind in [1, 2, 7, 13, 14, 19]
                for row in ['B', 'C']
            ]
            for well in set
        ]

        for a, d in zip(aspirate_locs, dispense_locs):
            m300.aspirate(40, a.bottom(1))
            m300.move_to(d.bottom(3))
            m300.delay(seconds=spheroid_release_waiting_time_in_seconds)
            m300.blow_out(a.top())

        m300.drop_tip()
