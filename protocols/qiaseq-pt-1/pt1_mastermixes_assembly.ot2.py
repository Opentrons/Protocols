from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'QIAseq Targeted DNA Panel for Illumina Instruments Part 1:\
 Mastermixes Assembly',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load modules and labware
tempdeck = modules.load('tempdeck', '1')
rxn_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    '1',
    'reaction plate',
    share=True
)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
reagent_tuberack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap',
    '2',
    'reagent tuberack (pre-chilled)'
)
strips = labware.load(
    'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '3', 'strips')
tips50 = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in ['4', '5']]
tips10 = [
    labware.load('opentrons_96_tiprack_10ul', str(slot))
    for slot in range(6, 10)
]

# reagents
frag_buffer = reagent_tuberack.wells('A1')
fera = reagent_tuberack.wells('B1')
nuc_free_water = reagent_tuberack.wells('C1')
frag_enzyme_mix = reagent_tuberack.wells('D1')
frag_mastermix_tube = reagent_tuberack.wells('A2')


def run_custom_protocol(
        number_of_samples: int = 96,
        volume_of_DNA_in_UL: float = 10,
        volume_of_nuclease_free_water: float = 5,
        p10_mount: StringSelection('left', 'right') = 'left',
        p50_mount: StringSelection('right', 'left') = 'right'
):
    # check
    if p10_mount == p50_mount:
        raise Exception('Input different mounts for pipettes.')

    # pipettes
    p50 = instruments.P50_Single(
        mount='right',
        tip_racks=tips50
    )

    # create mix for fragmentation, end-repair, and A-addition
    number_of_samples_for_mix = number_of_samples + 4
    p50.transfer(
        2.5*number_of_samples_for_mix,
        frag_buffer,
        frag_mastermix_tube,
        blow_out=True
    )
    p50.transfer(
        0.75*number_of_samples_for_mix,
        fera,
        frag_mastermix_tube.top(-5),
        blow_out=True
        )
    p50.pick_up_tip()
    p50.transfer(
        volume_of_nuclease_free_water*number_of_samples_for_mix,
        nuc_free_water,
        frag_mastermix_tube.top(-5),
        new_tip='never'
    )
    p50.mix(7, 40, frag_mastermix_tube)
    p50.blow_out(frag_mastermix_tube.top())

    if number_of_samples == 12:
        pip10 = instruments.P10_Single(
            mount='left',
            tip_racks=tips10
        )
        dests = rxn_plate.wells()[:number_of_samples]
        for d in dests:
            pip10.pick_up_tip()
            pip10.transfer(
                5,
                frag_mastermix_tube,
                d.top(),
                new_tip='never'
            )
            pip10.mix(7, 9, d)
            pip10.blow_out(d.top())
            pip10.drop_tip()
    else:
        num_cols = math.ceil(number_of_samples/8)
        for well in strips.cols('1'):
            p50.transfer(
                (20-volume_of_DNA_in_UL)*number_of_samples_for_mix/8,
                frag_mastermix_tube,
                well,
                new_tip='never'
                )
            p50.blow_out(well.top())

        pip10 = instruments.P10_Multi(
                mount='left',
                tip_racks=tips10
            )
        dests = rxn_plate.rows('A')[:num_cols]
        for d in dests:
            pip10.pick_up_tip()
            pip10.transfer(
                5,
                strips.wells('A1'),
                d.top(),
                new_tip='never',
            )
            pip10.mix(7, 9, d)
            pip10.blow_out(d.top()),
            pip10.drop_tip()
    p50.drop_tip()

    robot.pause('Briefly centrifuge the reaction plate and place back on the \
temperature module.')

    for d in dests:
        pip10.pick_up_tip()
        pip10.mix(7, 9, d)
        pip10.drop_tip()

    robot.pause('Briefly centrifuge the reaction plate and place back on the \
temperature module.')

    # add Fragmentation Enzyme Mix and mix
    rxn_samples = rxn_plate.wells()[:number_of_samples]
    p50.pick_up_tip()
    p50.transfer(
        5, frag_enzyme_mix, rxn_samples, new_tip='always')

    robot.pause('Briefly centrifuge the reaction plate and place back on the \
temperature module.')

    for d in dests:
        pip10.pick_up_tip()
        pip10.transfer(5, frag_enzyme_mix, d, new_tip='never')
        pip10.mix(7, 9, d)
        pip10.blow_out(d.top())
        pip10.drop_tip()

    robot.comment('Briefly centrifuge the reaction plate and place back on the \
temperature module. Program the thermal cycler according to the parameters \
prescribed in the manual. Ensure the thermal cycler is pre-chilled ot 4˚C \
before transferring the reaction plate off the temperature module. Upon \
completion, allow the thermal cycler to return to 4°C and proceed to part 2: \
adapter ligation.')
