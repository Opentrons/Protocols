from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'QIAseq Targeted DNA Panel for Illumina Instruments Part 7:\
 Cleanup of universal PCR',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load modules and labware
magdeck = modules.load('magdeck', '1')
rxn_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr',
    '1',
    'reaction plate',
    share=True
)
elution_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul', '2', 'elution plate')
reagent_reservoir = labware.load(
    'usascientific_12_reservoir_22ml', '3', 'reagent reservoir')

# reagents
nuc_free_water = reagent_reservoir.wells('A1')
beads = reagent_reservoir.wells('A2')
etoh = reagent_reservoir.wells('A3', length=2)
liquid_waste = [
    chan.top() for chan in reagent_reservoir.wells('A10', length=3)
]


def run_custom_protocol(
        number_of_samples: int = 96,
        p50_mount: StringSelection('right', 'left') = 'right',
        p300_mount: StringSelection('left', 'right') = 'left'
):
    # check
    if p50_mount == p300_mount:
        raise Exception('Input different mounts for pipettes.')

    num_sample_cols = math.ceil(number_of_samples/8)
    rxn_samples = rxn_plate.rows('A')[:num_sample_cols]
    elution_samples = elution_plate.rows('A')[:num_sample_cols]

    # pipettes
    tips300 = [labware.load('opentrons_96_tiprack_300ul', slot)
               for slot in ['4', '5', '6', '7']]
    tips50 = [labware.load('opentrons_96_tiprack_300ul', slot)
              for slot in ['8', '9', '10', '11']]

    m300 = instruments.P300_Multi(
        mount='left',
        tip_racks=tips300
    )
    m50 = instruments.P50_Multi(
        mount='right',
        tip_racks=tips50
    )

    tip50_count = 0
    tip300_count = 0
    tip50_max = len(tips50)*12
    tip300_max = len(tips300)*12

    def pick_up(pip):
        nonlocal tip50_count
        nonlocal tip300_count

        if pip == m50:
            if tip50_count == tip50_max:
                robot.pause('Replace 300ul tipracks before resuming.')
                m50.reset()
                tip50_count = 0
            m50.pick_up_tip()
            tip50_count += 1
        else:
            if tip300_count == tip300_max:
                robot.pause('Replace 300ul tipracks before resuming')
                m300.reset()
                tip300_count = 0
            m300.pick_up_tip()
            tip300_count += 1

    # distribute nuclease-free water and beads to each sample
    m300.set_flow_rate(aspirate=100, dispense=250)
    pick_up(m300)
    m300.distribute(
        80,
        nuc_free_water,
        [s.top() for s in rxn_samples],
        new_tip='never'
    )
    for s in rxn_samples:
        if not m300.tip_attached:
            pick_up(m300)
        m300.transfer(100, beads, s, new_tip='never')
        m300.mix(5, 100, s)
        m300.blow_out(s.top())
        m300.drop_tip()

    # incubate
    m300.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    m300.delay(minutes=5)

    # remove supernatant
    for s in rxn_samples:
        pick_up(m300)
        m300.transfer(
            200,
            s,
            liquid_waste[0],
            new_tip='never'
        )
        m300.drop_tip()

    # ethanol washes
    for wash in range(2):
        pick_up(m300)
        for i, s in enumerate(rxn_samples):
            if i != 0:
                m300.dispense(30, etoh[wash].top())
            m300.transfer(
                200,
                etoh[wash],
                s.top(),
                new_tip='never',
                air_gap=10
            )
            if i < len(rxn_samples) - 1:
                m300.aspirate(30)

        # remove supernatant
        for s in rxn_samples:
            if not m300.tip_attached:
                pick_up(m300)
            m300.transfer(210, s, liquid_waste[wash], new_tip='never')
            m300.drop_tip()

    # remove supernatant completely with P50 multi
    for s in rxn_samples:
        pick_up(m50)
        m50.transfer(7, s.bottom(), liquid_waste[0], new_tip='never')
        m50.drop_tip()

    # airdry
    m50.delay(minutes=7)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    for s in rxn_samples:
        pick_up(m50)
        m50.transfer(
            30,
            nuc_free_water,
            s,
            new_tip='never'
        )
        m50.mix(5, 40, s)
        m50.blow_out(s.top())
        m50.drop_tip()

    magdeck.engage(height=18)
    m50.delay(minutes=1)

    # transfer to elution plate
    for s, d in zip(rxn_samples, elution_samples):
        pick_up(m50)
        m50.transfer(28, s, d, new_tip='never')
        m50.drop_tip()

    magdeck.disengage()
