from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'QIAseq Targeted DNA Panel for Illumina Instruments Part 4:\
 Target enrichment',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load modules and labware
rxn_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    '1',
    'reaction plate'
)
reagent_tuberack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap',
    '2',
    'reagent tuberack (pre-chilled)'
)
strips = labware.load(
    'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '3', 'strips')
tips50_single = labware.load('opentrons_96_tiprack_300ul', '4')
tips_50_multi = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in ['5', '6']
]

tepcr = reagent_tuberack.wells('A3')
dna_panel = reagent_tuberack.wells('B3')
il_forward_primer = reagent_tuberack.wells('C3')
dna_pol = reagent_tuberack.wells('D3')
targ_enrich_mix_tube = reagent_tuberack.wells('A4')


def run_custom_protocol(
        number_of_samples: int = 96,
        p50_single_mount: StringSelection('right', 'left') = 'right',
        p50_multi_mount: StringSelection('left', 'right') = 'left'
):
    # check
    if p50_single_mount == p50_multi_mount:
        raise Exception('Input different mounts for pipettes.')

    num_cols = math.ceil(number_of_samples/8)
    samples_single = rxn_plate.wells()[:number_of_samples]
    samples_multi = rxn_plate.rows('A')[:num_cols]

    # pipettes
    p50 = instruments.P50_Single(
        mount=p50_single_mount,
        tip_racks=[tips50_single]
    )

    m50 = instruments.P50_Multi(
        mount=p50_multi_mount,
        tip_racks=tips_50_multi
    )

    # create mix for target enrichment
    number_of_samples_for_mix = number_of_samples + 4
    p50.transfer(
        4*number_of_samples_for_mix,
        tepcr,
        targ_enrich_mix_tube,
        blow_out=True
    )
    p50.transfer(
        5*number_of_samples_for_mix,
        dna_panel,
        targ_enrich_mix_tube.top(5),
        blow_out=True
    )
    p50.transfer(
        0.8*number_of_samples_for_mix,
        il_forward_primer,
        targ_enrich_mix_tube.top(5),
        blow_out=True
    )
    p50.pick_up_tip()
    p50.transfer(
        0.8*number_of_samples_for_mix,
        dna_pol,
        targ_enrich_mix_tube.top(5),
        blow_out=True,
        new_tip='never'
    )
    p50.mix(5, 50, targ_enrich_mix_tube)
    p50.drop_tip()

    if number_of_samples <= 16:
        p50.transfer(
            11.6,
            targ_enrich_mix_tube,
            [s for s in samples_single],
            new_tip='always'
        )
    else:
        p50.distribute(
            11.6*number_of_samples_for_mix/8,
            targ_enrich_mix_tube,
            [well for well in strips.columns('1')],
            disposal_vol=0,
            blow_out=True
        )
        m50.transfer(
            11.6,
            strips.wells('A1'),
            [s for s in samples_multi],
            new_tip='always'
        )

    robot.pause('Briefly centrifuge reaction plate and replace in slot 1')

    for s in samples_multi:
        m50.pick_up_tip()
        m50.mix(7, 10, s)
        m50.blow_out(s.top())
        m50.drop_tip()

    robot.comment('Briefly centrifuge again. Program the thermal cycler \
according to the parameters prescribed in the manual, and thermocycle the \
reaction plate. After the reaction is complete, place the reactions on ice \
and proceed with “Cleanup of target enrichment”, below. Alternatively, the \
samples can be stored at –20°C in a constant-temperature freezer for up to 3 \
days.')
