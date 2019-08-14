from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Zymo Zyppy-96 Plasmid MagPrep Kit: Part 3/3 [Steps 61-67 \
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

elution_name = 'zymo_96_wellplate_90ul_elution'
if elution_name not in labware.list():
    labware.create(
        elution_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=13.5,
        volume=90
    )

# load modules and labware
magdeck = modules.load('magdeck', '1')
deep_block = labware.load(block_name, '1', '96-well block', share=True)
elution_plate = labware.load(elution_name, '5', 'elution plate')
tips300 = labware.load('opentrons_96_tiprack_300ul', '7')


def run_custom_protocol(
        number_of_samples: int = 96,
        pipette_mount: StringSelection('right', 'left') = 'right'
):
    # checks
    if number_of_samples < 1 or number_of_samples > 96:
        raise Exception('Invalid number of samples.')

    # pipettes
    m300 = instruments.P300_Single(mount=pipette_mount, tip_racks=[tips300])

    # setup
    num_cols = math.ceil(number_of_samples/8)
    deepwell_samples = deep_block.rows('A')[:num_cols]
    elution_samples = elution_plate.rows('A')[:num_cols]

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

    magdeck.engage(height=18)
    m300.delay(minutes=5)

    # transfer supernatant to elution plate
    m300.set_flow_rate(aspirate=30)
    for s, d in zip(deepwell_samples, elution_samples):
        m300.pick_up_tip()
        m300.transfer(50, s, d.top(-2), new_tip='never')
        m300.blow_out(d.top(-1))
        m300.drop_tip()

    magdeck.disengage()

    robot.comment('The eluted DNA can be used immediately for molecular based \
applications or stored ≤-20oC for future use.')
