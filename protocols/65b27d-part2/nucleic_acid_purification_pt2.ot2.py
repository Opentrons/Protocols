from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Zymo Zyppy-96 Plasmid MagPrep Kit: Part 2/3 [Steps 25-60 \
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
collection_plate = labware.load(
    collection_name, '1', 'collection plate', share=True)
deep_block = labware.load(block_name, '2', '96-well block')
[reagent_res1, reagent_res2] = [
    labware.load(
        'usascientific_12_reservoir_22ml',
        slot,
        'reagent reservoir ' + str(ind+1)
    )
    for ind, slot in enumerate(['3', '6'])
]
liquid_waste = labware.load(
    'agilent_1_reservoir_290ml',
    '4',
    'liquid waste (loaded empty)'
).wells(0).top()
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

    waste_vol = 0

    def waste_check(vol):
        nonlocal waste_vol
        waste_vol += vol
        if waste_vol > 280000:
            robot.pause('Empty liquid waste reservoir before resuming to avoid \
overflow.')
            waste_vol = 0
            print('OVERFLOW')

    def reagent_addition(
            reagent, trans_vol, mix_vol, mix_time, samples, disp_loc='top'):
        t_disp = mix_vol/300
        t_asp = mix_vol/150
        t_mix = t_disp+t_asp
        mix_reps = math.ceil(mix_time/t_mix)

        for i, s in enumerate(samples):
            tip_check()
            reagent_ind = math.floor((i/len(samples))*len(reagent))
            m300.pick_up_tip()
            if disp_loc == 'top':
                dest = s.top()
            else:
                dest = s.bottom(10)
            m300.transfer(
                trans_vol,
                reagent[reagent_ind],
                dest,
                new_tip='never'
            )
            m300.mix(mix_reps, mix_vol, s)
            m300.blow_out(s.top())
            m300.drop_tip()

    magdeck.engage(height=18)
    m300.delay(minutes=5)

    # discard supernatant
    m300.set_flow_rate(aspirate=30)
    for c in collection_samples:
        tip_check()
        waste_check(800)
        m300.transfer(800, c, liquid_waste, blow_out=True)
    m300.set_flow_rate(aspirate=150)

    magdeck.disengage()

    # distribute endo-wash buffer and mix
    reagent_addition(endo_wash_buffer, 200, 100, 10, collection_samples)

    magdeck.engage(height=18)
    m300.delay(minutes=5)

    # discard supernatant
    m300.set_flow_rate(aspirate=30)
    for c in collection_samples:
        tip_check()
        waste_check(210)
        m300.transfer(210, c, liquid_waste, blow_out=True)
    m300.set_flow_rate(aspirate=150)

    magdeck.disengage()

    for wash in range(2):
        # distribute zyppy wash buffer and mix
        reagent_addition(zyppy_wash_buffer, 400, 250, 10, collection_samples)

        magdeck.engage(height=18)
        m300.delay(minutes=5)

        # discard supernatant
        m300.set_flow_rate(aspirate=30)
        for c in collection_samples:
            tip_check()
            waste_check(420)
            m300.transfer(420, c, liquid_waste, blow_out=True)
        m300.set_flow_rate(aspirate=150)

        if wash == 0:
            magdeck.disengage()

    robot.pause('Dry MagBeads on magnetic stand by incubating at room \
temperature for 10 minutes or until beads are fully dry (but not overdried).')

    magdeck.disengage()

    # distribue zyppy elution buffer and mix
    reagent_addition(
        zyppy_elution_buffer, 40, 20, 300, deepwell_samples, disp_loc='bottom')

    robot.comment('Replace empty tip racks, and proceed to Part 3')
