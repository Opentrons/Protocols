from opentrons import labware, instruments

metadata = {
    'protocolName': 'PCR Preparation',
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

plate_name = 'Lightcycler-384-well'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.13,
        depth=9.0,
        volume=100
    )

strips = labware.load(strips_name, '1', 'primer strips')
plate = labware.load(plate_name, '2', 'Lightcycler plate')
tubes = labware.load(
    'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap',
    '3',
    'cDNA tube rack'
)
tips10 = labware.load('opentrons_96_tiprack_10ul', '4')
tips50 = labware.load('opentrons_96_tiprack_300ul', '5')

# pipettes
p10 = instruments.P10_Single(mount='right', tip_racks=[tips10])
p50 = instruments.P50_Single(mount='left', tip_racks=[tips50])

# reagents
primers = [well for col in strips.columns()[0:2] for well in col]


def run_custom_protocol(
        volume_of_primer_in_ul: float = 4,
        volume_of_cDNA_in_ul: float = 6
):
    # check:
    if volume_of_cDNA_in_ul < 5:
        raise Exception('P50 pipette cannot accommodate distributions for \
volumes less than 5ul.')

    # setup alternating destination rows and distribute primers
    dests1 = [[well for well in row] for row in plate.rows()[0::2]]
    dests2 = [[well for well in row] for row in plate.rows()[1::2]]
    dests = dests1+dests2

    for p, dest_set in zip(primers, dests):
        p10.pick_up_tip()
        for d in dest_set:
            p10.transfer(
                volume_of_primer_in_ul,
                p,
                d.bottom(),
                new_tip='never'
            )
            p10.blow_out()
        p10.drop_tip()

    # distribute cDNA samples and negative
    cdna_tubes = [tubes for tube in tubes.wells('A1', length=8)]
    for i, cdna in enumerate(cdna_tubes):
        dests = plate.wells()[i*48:(i+1)*48]
        p50.distribute(
            volume_of_cDNA_in_ul,
            cdna,
            [d.bottom(2) for d in dests],
            blow_out=True
        )
