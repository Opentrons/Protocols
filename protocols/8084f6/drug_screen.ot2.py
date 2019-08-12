from opentrons import labware, instruments

metadata = {
    'protocolName': 'Drug Screening',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
strips_name = 'SSI-PCR-strips-200ul'
if strips_name not in labware.list():
    labware.create(
        strips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.6,
        depth=20.3,
        volume=200
    )

plate_name_96 = 'Biostrategy-96-PCR'
if plate_name_96 not in labware.list():
    labware.create(
        plate_name_96,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.2,
        depth=20.45,
        volume=200
    )

plate_name_384 = 'Biostrategy-384-NX'
if plate_name_384 not in labware.list():
    labware.create(
        plate_name_384,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.18,
        depth=9.25,
        volume=30
    )

# load labware
plates96 = [labware.load(plate_name_96, str(slot), 'PCR plate ' + str(slot))
            for slot in range(1, 5)]
plate384 = labware.load(plate_name_384, '5', '384-well destination plate')
strips = labware.load(strips_name, '6', 'mastermix strip')
tips10 = [labware.load('opentrons_96_tiprack_10ul', str(slot))
          for slot in range(7, 12)]

# pipette
m10 = instruments.P10_Multi(mount='right', tip_racks=tips10)


def run_custom_protocol(
        volume_of_mastermix_in_ul: float = 4,
        volume_of_sample_in_ul: float = 1,
        mastermix_strip_column: int = 1
):
    # check
    if mastermix_strip_column > 12 or mastermix_strip_column < 1:
        raise Exception('Invalid column for mastermix strip.')

    # reagents
    mm = strips.rows('A')[mastermix_strip_column-1]

    # mastermix distribution
    mm_dests = [well for row in plate384.rows()[0:2] for well in row]
    m10.pick_up_tip()
    for d in mm_dests:
        m10.transfer(
            volume_of_mastermix_in_ul,
            mm.bottom(),
            d.bottom(),
            new_tip='never'
        )
        m10.blow_out()
    m10.drop_tip()

    # 1-to-1 DNA transfer
    dna_sources = [well for plate in plates96 for well in plate.rows('A')]
    dna_dests1 = [well for row in plate384.rows()[0:2]
                  for well in row[:12]]
    dna_destst2 = [well for row in plate384.rows()[0:2]
                   for well in row[12:]]
    dna_dests = dna_dests1 + dna_destst2

    for s, d in zip(dna_sources, dna_dests):
        m10.pick_up_tip()
        m10.transfer(
            volume_of_sample_in_ul,
            s,
            d.bottom(),
            new_tip='never'
        )
        m10.blow_out()
        m10.drop_tip()
