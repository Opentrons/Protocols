from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'NGS Library Prep Part 1/4: M1 First Strand cDNA Synthesis \
- High RNA Input and M2 RNA Removal',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom plate
plate_name = 'Abgene-MIDI-96-800ul'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=27,
        volume=800
    )

# load modules and labware
trough = labware.load('usascientific_12_reservoir_22ml', '2')
tempdeck = modules.load('tempdeck', '4')
plate_TM = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul', '4', share=True)
tempdeck.set_temperature(42)
tempdeck.wait_for_temp()
reagent_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul', '5', 'reagent plate')
plate_2 = labware.load(
    'biorad_96_wellplate_200ul_pcr', '7')
tips10 = [labware.load('opentrons_96_tiprack_10ul', slot)
          for slot in ['3', '6', '8']]
tips50 = [labware.load('opentrons_96_tiprack_300ul', str(slot))
          for slot in range(9, 12)]


def run_custom_protocol(
        number_of_samples: int = 96,
        p10_multi_mount: StringSelection('right', 'left') = 'right',
        p50_multi_mount: StringSelection('left', 'right') = 'left',
        reagent_starting_column: int = 1
):
    # checks
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples')
    if p10_multi_mount == p50_multi_mount:
        raise Exception('Invalid pipette mount combination')
    if reagent_starting_column > 7:
        raise Exception('Invlaid reagent starting column')

    # pipettes
    m10 = instruments.P10_Multi(mount=p10_multi_mount, tip_racks=tips10)
    m50 = instruments.P50_Multi(mount=p50_multi_mount, tip_racks=tips50)

    # reagent setup
    [fs2e1, fs1, rs, ss1, ss2e2, pcre3] = [
        reagent_plate.rows('A')[ind]
        for ind in range(reagent_starting_column-1, reagent_starting_column+5)
    ]
    [pb, eb, ps] = [trough.wells(ind) for ind in range(3)]

    # sample setup
    num_cols = math.ceil(number_of_samples/8)
    samples_TM = plate_TM.rows('A')[:num_cols]

    # tip check function
    tip10_max = len(tips10)*12
    tip50_max = len(tips50)*12
    tip10_count = 0
    tip50_count = 0

    def tip_check(pipette):
        nonlocal tip10_count
        nonlocal tip50_count
        if pipette == 'p50':
            tip50_count += 1
            if tip50_count > tip50_max:
                m50.reset()
                tip50_count = 1
                robot.pause('Please replace 50ul tipracks before resuming.')
        else:
            tip10_count += 1
            if tip10_count > tip10_max:
                m10.reset()
                tip10_count = 1
                robot.pause('Please replace 10ul tipracks before resuming.')

    """M1 First Strand cDNA Synthesis - High RNA Input"""

    for s in samples_TM:
        tip_check('p10')
        m10.pick_up_tip()
        m10.transfer(5, fs1, s, new_tip='never')
        m10.mix(5, 5, s)
        m10.blow_out(s.bottom(5))
        m10.drop_tip()

    robot.pause('Seal the plate and put on a thermocycler for 3 min at 90°C, \
and hold at 42°C. Remove the plate from the thermocycler and put back on TM1 \
before resuming')

    for s in samples_TM:
        tip_check('p10')
        m10.pick_up_tip()
        m10.transfer(10, fs2e1, s, new_tip='never')
        m10.mix(10, 10, s)
        m10.blow_out(s.bottom(5))
        m10.drop_tip()

    robot.pause('Seal the plate and place back in TM1 before resuming. The \
plate will then incubate for 15 minutes')
    robot._driver.run_flag.wait()
    m10.delay(minutes=15)
    robot._driver.run_flag.wait()
    robot.pause('Remove the seal. The reagent plate in TM2 can now be trashed')

    """M2 RNA Removal"""

    for s in samples_TM:
        tip_check('p10')
        m10.pick_up_tip()
        m10.transfer(5, rs, s, new_tip='never')
        m10.mix(10, 10, s)
        m10.blow_out(s.bottom(5))
        m10.drop_tip()

    tempdeck.set_temperature(25)
    robot._driver.run_flag.wait()
    robot.comment('Seal the plate, put it on a thermocycler for 10 min at 95°C, \
and replace on TM2 once it has reached 25˚C. Proceed with Part 2/4: M3 Second \
Strand Synthesis and M4 DNA Cleanup.')
