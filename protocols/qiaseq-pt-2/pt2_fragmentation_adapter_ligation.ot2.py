from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'QIAseq Targeted DNA Panel for Illumina Instruments Part 2:\
 Adapter Ligation',
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
tempdeck = modules.load('tempdeck', '4')
rxn_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    '4',
    'reaction plate',
    share=True
)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
index_plates = [labware.load(
    plate_name,
    slot,
    'index plate ' + str(i))
                for i, slot in enumerate(['1', '2'])]
strips = labware.load(
    'opentrons_96_aluminumblock_generic_pcr_strip_200ul', '3', 'strips')
reagent_tuberack = labware.load(
    'opentrons_24_aluminumblock_generic_2ml_screwcap', '6', 'reagent tuberack')
tips50 = [labware.load('opentrons_96_tiprack_300ul', slot)
          for slot in ['5', '7']]
tips10 = [labware.load('opentrons_96_tiprack_10ul', slot)
          for slot in ['8', '9', '10', '11']]

# reagents
ligation_buff = reagent_tuberack.wells('A1')
dna_ligase = reagent_tuberack.wells('B1')
ligation_sol = reagent_tuberack.wells('C1')
adapter_ligation_mm_tube = reagent_tuberack.wells('A2')


def run_custom_protocol(
        number_of_samples: int = 96,
        index_start_column: int = 1,
        p10_mount: StringSelection('left', 'right') = 'left',
        p50_mount: StringSelection('right', 'left') = 'right'
):
    # check
    if p10_mount == p50_mount:
        raise Exception('Input different mounts for pipettes.')

    num_sample_cols = math.ceil(number_of_samples/8)
    if num_sample_cols + index_start_column > 13:
        raise Exception('Invalid combination of sample number and index start \
column.')

    # pipettes
    p50 = instruments.P50_Single(
        mount=p50_mount,
        tip_racks=tips50
    )
    m10 = instruments.P10_Multi(
        mount=p10_mount,
        tip_racks=tips10
    )

    # create adapter ligation mastermix
    num_samples_for_mix = number_of_samples + 4
    p50.transfer(
        10*num_samples_for_mix,
        ligation_buff,
        adapter_ligation_mm_tube.bottom(),
        blow_out=True,
        new_tip='always'
    )
    p50.pick_up_tip()
    p50.transfer(
        5*num_samples_for_mix,
        dna_ligase,
        adapter_ligation_mm_tube.top(),
        new_tip='never',
        blow_out=True
        )
    p50.mix(7, 40, adapter_ligation_mm_tube)
    p50.blow_out(adapter_ligation_mm_tube.top())

    # transfer indices
    num_trans = math.ceil(number_of_samples/4)
    index_sources = [
        plate.columns(col)[0]
        for col in range(index_start_column-1, 12)
        for plate in index_plates][:num_trans]
    index_dests = [
        well
        for col in rxn_plate.columns()[:num_sample_cols]
        for well in [col[0], col[4]]][:num_trans]
    for s, d in zip(index_sources, index_dests):
        m10.pick_up_tip()
        m10.transfer(
            2.8,
            s,
            d,
            new_tip='never'
        )
        m10.blow_out()
        m10.drop_tip()

    single_dests = rxn_plate.wells()[:number_of_samples]
    if number_of_samples == 12:
        p50.distribute(
            15,
            adapter_ligation_mm_tube,
            [d.top() for d in single_dests],
            disposal_vol=0
        )
    else:
        # transfer to strip and then samples
        if not p50.tip_attached:
            p50.pick_up_tip()
        for well in strips.cols('1'):
            p50.transfer(
                15*num_samples_for_mix/8,
                adapter_ligation_mm_tube,
                well,
                new_tip='never'
                )
            p50.blow_out(well.top())
        p50.drop_tip()
        m10.transfer(
            15,
            strips.wells('A1'),
            [well.top() for well in rxn_plate.rows('A')[:num_sample_cols]]
        )

    # transfer ligation solution according to high viscosity
    p50.set_flow_rate(aspirate=5, dispense=10)
    for d in single_dests:
        p50.pick_up_tip()
        p50.aspirate(7.2, ligation_sol)
        p50.delay(seconds=5)
        p50.touch_tip(ligation_sol)
        p50.dispense(d)
        p50.blow_out()
        p50.touch_tip(d)
        p50.drop_tip()
    p50.set_flow_rate(aspirate=25, dispense=50)
    p50.pick_up_tip()

    robot.pause('Briefly centrifuge the reaction plate and place back on the \
temperature module.')

    for well in rxn_plate.rows('A')[:num_sample_cols]:
        m10.set_flow_rate(aspirate=1, dispense=2)
        m10.pick_up_tip()
        m10.mix(10, 8, well)
        m10.set_flow_rate(aspirate=5, dispense=2)
        m10.blow_out(well.top())
        m10.drop_tip()

    robot.comment('Briefly centrifuge the reaction plate and place back on the \
temperature module. Program a thermal cycler to 20°C and incubate the \
reactions for 15 min. Proceed to part 3: cleanup of adapter-ligated DNA.')
