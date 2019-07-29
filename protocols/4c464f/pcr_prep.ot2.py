from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Preparation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom plate
pcr_name = 'biorad_96_wellplate_350ul'
if pcr_name not in labware.list():
    labware.create(
        pcr_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=19.85,
        volume=350
    )

# load modules and labware
tempdeck = modules.load('tempdeck', '1')
pcr_plate = labware.load(
    pcr_name,
    '1',
    'PCR plate',
    share=True
)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
mm_tubes = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap',
    '2',
    'mastermix tuberack').rows('A')[:2]
oligo_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    '4',
    'oligo plate'
)
tips50_single = labware.load('opentrons_96_tiprack_300ul', '5')
tips50_multi = labware.load('opentrons_96_tiprack_300ul', '6')


def run_custom_protocol(
        P50_Single_mount: StringSelection('right', 'left') = 'right',
        P50_Multi_mount: StringSelection('left', 'right') = 'left'
):
    # pipettes
    p50 = instruments.P50_Single(
        mount=P50_Single_mount, tip_racks=[tips50_single])
    m50 = instruments.P50_Multi(
        mount=P50_Multi_mount, tip_racks=[tips50_multi])

    # distribute mastermix to all wells
    mm = mm_tubes[0]
    p50.pick_up_tip()
    for i in range(48):
        p50.distribute(
            20,
            mm,
            [well.top() for well in pcr_plate.wells(i*2, length=2)],
            new_tip='never',
            blow_out=True
        )
        if i == 23:
            p50.transfer(
                200,
                mm,
                mm_tubes[1],
                new_tip='never',
                blow_out=True
            )
            mm = mm_tubes[1]
    p50.drop_tip()

    for oligo, dest in zip(oligo_plate.rows('A'), pcr_plate.rows('A')):
        m50.pick_up_tip()
        m50.transfer(
            5,
            oligo,
            dest,
            new_tip='never'
        )
        m50.blow_out(dest)
        m50.drop_tip()
