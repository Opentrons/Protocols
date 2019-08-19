from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Zymo Zyppy-96 Plasmid MagPrep Kit: Part 1/3 [Steps 1-24 \
of automation manual]',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
collection_name = 'zymo_96_wellplate_1.2ml_collection'
if collection_name not in labware.list():
    labware.create(
        collection_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=28,
        volume=1200
    )

block_name = 'zymo_96_deepwellplate_2ml'
if block_name not in labware.list():
    labware.create(
        block_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=40,
        volume=2000
    )

# load modules and labware
magdeck = modules.load('magdeck', '1')
deep_block = labware.load(block_name, '1', '96-well block', share=True)
collection_plate = labware.load(collection_name, '2', 'collection plate')
[reagent_res1, reagent_res2] = [
    labware.load(
        'usascientific_12_reservoir_22ml',
        slot,
        'reagent reservoir ' + str(ind+1)
    )
    for ind, slot in enumerate(['3', '6'])
]
tips300 = [labware.load('opentrons_96_tiprack_300ul', str(slot))
           for slot in ['5', '7', '8', '9', '10', '11']]

# reagents
deep_blue_lysis_buffer = reagent_res1.wells()[:2]
neutralization_buffer = reagent_res1.wells()[2:7]
endo_wash_buffer = reagent_res1.wells()[7:10]
zyppy_wash_buffer = reagent_res2.wells()[:3]
zyppy_elution_buffer = reagent_res2.wells()[3:5]
magclearing_beads = [reagent_res2.wells()[5]]
magbinding_beads = [reagent_res2.wells()[6]]


def run_custom_protocol(
        number_of_samples: int = 96,
        pipette_mount: StringSelection('right', 'left') = 'right'
):
    # checks
    if number_of_samples < 1 or number_of_samples > 96:
        raise Exception('Invalid number of samples.')

    # pipettes
    m300 = instruments.P300_Single(mount=pipette_mount, tip_racks=tips300)

    # setup
    num_cols = math.ceil(number_of_samples/8)
    collection_samples = collection_plate.rows('A')[:num_cols]
    deepwell_samples = deep_block.rows('A')[:num_cols]

    tip_count = 0
    tip_max = len(tips300)*12

    def tip_check():
        nonlocal tip_count
        if tip_count == tip_max:
            robot.pause('Replace 300ul tip racks before resuming.')
            m300.reset()
            tip_count = 0
        tip_count += 1

    def reagent_addition(reagent, trans_vol, mix_vol, mix_time, samples):
        t_disp = mix_vol/300
        t_asp = mix_vol/150
        t_mix = t_disp+t_asp
        mix_reps = math.ceil(mix_time/t_mix)

        for i, s in enumerate(samples):
            tip_check()
            reagent_ind = math.floor((i/len(samples))*len(reagent))
            m300.pick_up_tip()
            m300.transfer(
                trans_vol,
                reagent[reagent_ind],
                s.top(),
                new_tip='never'
            )
            m300.mix(mix_reps, mix_vol, s)
            m300.blow_out(s.top())
            m300.drop_tip()

    # distribute deep blue lysis buffer and mix
    reagent_addition(deep_blue_lysis_buffer, 100, 100, 10, deepwell_samples)

    m300.delay(minutes=5)

    # distribute neutralization buffer and mix
    reagent_addition(neutralization_buffer, 450, 250, 45, deepwell_samples)

    # distribute magclearing beads and mix
    reagent_addition(magclearing_beads, 50, 250, 30, deepwell_samples)

    magdeck.engage(height=18)
    m300.delay(minutes=5)

    # transfer supernatant to collection plate
    for s, d in zip(deepwell_samples, collection_samples):
        m300.transfer(750, s.bottom(20), d.top())

    # distribute magbinding beads and mix
    reagent_addition(magbinding_beads, 30, 200, 60, collection_samples)

    robot.comment('Replace empty tip racks and proceed to Part 2')
