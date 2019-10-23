from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'QIAseq Targeted DNA Panel for Illumina Instruments Part 6:\
 Universal PCR',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create high profile plate
plate_name = 'opentrons_96_aluminumblock_biorad_wellplate_350ul'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=19.85,
        volume=350
    )

# load modules and labware
rxn_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr',
    '1',
    'reaction plate'
)
reagent_tuberack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap', '2', 'reagent tuberack')
strips = labware.load(
    'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '3', 'strips')
index_plate = labware.load(
    plate_name, '4', 'index plate')
tips50 = [labware.load('opentrons_96_tiprack_300ul', slot)
          for slot in ['5', '6']]
tips10 = [labware.load('opentrons_96_tiprack_10ul', slot)
          for slot in ['10', '11']]


def run_custom_protocol(
        number_of_samples: int = 96,
        p10_mount: StringSelection('left', 'right') = 'left',
        p50_mount: StringSelection('right', 'left') = 'right',
        index_set: StringSelection(
            '12-index I',
            '96-index I Set A, B, C, or D') = '96-index I Set A, B, C, or D',
        index_start_column: int = 1
):
    # check
    if p10_mount == p50_mount:
        raise Exception('Input different mounts for pipettes.')

    num_samples = int(number_of_samples)
    samples = rxn_plate.wells()[:num_samples]
    num_sample_cols = math.ceil(num_samples/8)
    samples_multi = rxn_plate.rows('A')[:num_sample_cols]
    if num_sample_cols + index_start_column > 13:
        raise Exception('Invalid combination of sample number and index start \
column.')

    # pipettes
    p50 = instruments.P50_Single(
        mount=p50_mount,
        tip_racks=tips50
    )

    # reagents
    upcr_buff = reagent_tuberack.wells('A1')
    dna_pol = reagent_tuberack.wells('B1')

    if index_set == '12-index I':
        m10 = instruments.P10_Multi(
            mount=p10_mount,
            tip_racks=tips10
        )

        mix_tube = reagent_tuberack.wells('A2')
        il_universal_primer = reagent_tuberack.wells('C1')

        # create and distribute mix to samples
        num_samples_for_mix = num_samples + 4
        p50.transfer(
            4*num_samples_for_mix,
            upcr_buff,
            mix_tube,
            blow_out=True
        )
        p50.transfer(
            0.8*num_samples_for_mix,
            il_universal_primer,
            mix_tube,
            blow_out=True
        )
        p50.pick_up_tip()
        p50.transfer(
            1*num_samples_for_mix,
            dna_pol,
            mix_tube,
            new_tip='never'
        )
        p50.mix(5, 40, mix_tube)
        p50.distribute(
            5.8,
            mix_tube,
            [s.top() for s in samples],
            blow_out=True
        )

        indices = [index_plate.rows('A')[index_start_column-1:
                                         index_start_column-1+num_sample_cols]]
        for index, s in zip(indices, samples_multi):
            m10.pick_up_tip()
            m10.transfer(
                0.8,
                index,
                s,
                new_tip='never'
            )
            m10.mix(7, 9, s)
            m10.blow_out(s.top())
            m10.drop_tip()

        robot.pause('Briefly centrifuge the reaction plate and place back on the \
OT-2 deck.')

        for s in samples_multi:
            m10.pick_up_tip()
            m10.mix(7, 9, s)
            m10.blow_out(s.top())
            m10.drop_tip()

        robot.comment('Briefly centrifuge the index plate and thermocycle \
according to parameters prescribed in the user manual. Once complete, place \
the reactions on ice and proceed to Cleanup of Universal PCR. Alternatively, \
the samples can be stored at –20°C in a constant-temperature freezer for up \
to 3 days.')

    else:
        nuc_free_water = reagent_tuberack.wells('C1')
        p10 = instruments.P10_Single(mount='left', tip_racks=tips10)
        all_indexes = index_plate.wells()[:num_samples]
        p10.distribute(
            4,
            upcr_buff,
            [i.top() for i in all_indexes],
            disposal_vol=0,
            blow_out=True
        )
        p10.distribute(
            1.6,
            nuc_free_water,
            [i.top() for i in all_indexes],
            disposal_vol=0,
            blow_out=True
        )
        indices = [index_plate.wells(
                        'A'+str(index_start_column), length=num_samples)]
        for s, index in zip(samples, indices):
            p50.pick_up_tip()
            p50.transfer(
                13.4,
                s,
                index,
                new_tip='never'
            )
            p50.mix(7, 15, s)
            p50.blow_out(s.top())
            p50.drop_tip()

        robot.pause('Briefly centrifuge the index plate and place back on the \
OT-2 deck.')

        for s in indices:
            p50.pick_up_tip()
            p50.mix(7, 15, s)
            p50.blow_out(s.top())
            p50.drop_tip()

        robot.comment('Briefly centrifuge the index plate and thermocycle \
according to parameters prescribed in the user manual. Once complete, place \
the reactions on ice and proceed to Cleanup of Universal PCR. Alternatively, \
the samples can be stored at –20°C in a constant-temperature freezer for up \
to 3 days.')
