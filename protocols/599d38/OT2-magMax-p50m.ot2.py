"""
Social.Links@usask.ca

The deck on the OT-2 looks like this:

[10] [11] [trash]
[7]  [8]  [9]
[4]  [5]  [6]
[1]  [2]  [3]

and for this protocol, the labware is arranged like so:

[tip_racks]     [tip_racks]       [trash]
[tip_racks]     [tip_racks]       [tip_racks]
[sample_plate]  [reagent_trough]  [elution_plate]
[wash_plate1]   [wash_plate2A]    [wash_plate2B]

"""

from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Mag Max',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}


# our 96 samples
# this should be capable of holding large volumes ( 800uLs)
sample_name = '96-square-well-plate'
if sample_name not in labware.list():
    labware.create(
        sample_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.86,
        depth=20.72
    )

sample_plate = labware.load(sample_name, '4', 'sample plate')


# wash plates... are the > 300uLs
wash_plate1 = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'wash plate 1')
wash_plate2A = labware.load(
    'biorad_96_wellplate_200ul_pcr', '2', 'wash plate 2A')
wash_plate2B = labware.load(
    'biorad_96_wellplate_200ul_pcr', '3', 'wash plate 2B')

# where the purified samples will end up
# this only has to hold 50-100 uLs / well
# use a LoBind plate from Eppendorf
elution_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '6', 'elution plate')

# we need a reagent trough
# A1 - Bead Mix, premixed and vortexed: 2020 uLs loaded !!! do not add yet
# A2 - EMPTY
# A3 - 100% Isopropanol - 17,000 uLs loaded
# A4 - EMPTY
# A5 - Wash Solution #1 - 15,500 uLs loaded
# A6 - EMPTY
# A7 - Wash Solution #2 - 15,500 uLs loaded
# A8 - Wash Solution #2 - 15,500 uLs loaded
# A9 - EMPTY
# A10 - DNA Elution Buffer 1 - 5150 uLs loaded
# A11 - EMPTY
# A12 - DNA Elution Buffer 2 - 5150 uLs loaded

reagent_trough = labware.load(
    'usascientific_12_reservoir_22ml', '5', 'reagent trough')

bead_mix = reagent_trough.wells(0)
isopropanol = reagent_trough.wells(2)
wash_sol1 = reagent_trough.wells(4)
wash_sol2a = reagent_trough.wells(6)
wash_sol2b = reagent_trough.wells(7)
elu_buff1 = reagent_trough.wells(9)
elu_buff2 = reagent_trough.wells(11)

# creates the necessary tipracks for the remaining slots
slots50 = [str(slot) for slot in range(7, 10)]
tips50 = [labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots50]
slots300 = [str(slot) for slot in range(10, 12)]
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots300]


def run_custom_protocol(
        p50_type: StringSelection('single', 'multi') = 'multi',
        p300_type: StringSelection('single', 'multi') = 'multi',
        p50_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('left', 'right') = 'right',
        elution_volume: float = 100,
        number_of_samples_to_process: int = 96
        ):
    # check:
    if p50_mount == p300_mount:
        raise Exception('Input different mounts for P50 and P300 pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
        1 and 96).')
    if elution_volume > 100 or elution_volume < 10:
        raise Exception('Invalid elution volume (must be between \
        10uL and 100uL)')

    # create pipettes
    num_cols = math.ceil(number_of_samples_to_process/8)

    if p50_type == 'multi':
        pip50 = instruments.P50_Multi(mount=p50_mount, tip_racks=tips50)
        [samples50, elution] = [
            plate.rows('A')[:num_cols] for plate in [
                sample_plate, elution_plate
            ]
        ]
    else:
        pip50 = instruments.P50_Single(mount=p50_mount, tip_racks=tips50)
        [samples50, elution] = [
            plate.wells()[:number_of_samples_to_process] for plate in [
                sample_plate, elution_plate
            ]
        ]
    if p300_type == 'multi':
        pip300 = instruments.P300_Multi(mount=p300_mount, tip_racks=tips300)
        [samples300, plate1, plate2A, plate2B] = [
            plate.rows('A')[:num_cols] for plate in [
                sample_plate, wash_plate1, wash_plate2A, wash_plate2B
            ]
        ]
    else:
        pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)
        [samples300, plate1, plate2A, plate2B] = [
            plate.wells()[:number_of_samples_to_process] for plate in [
                sample_plate, wash_plate1, wash_plate2A, wash_plate2B
            ]
        ]

    def slot_parse(slots):
        slot_str = ''
        for i, s in enumerate(slots):
            if i < len(slots)-1:
                slot_str += s + ', '
            else:
                slot_str += s
        return slot_str

    slot_str50 = slot_parse(slots50)
    slot_str300 = slot_parse(slots300)

    tip50_max = len(tips50)*12 if p50_type == 'multi' else len(tips50)*96
    tip300_max = len(tips300)*12 if p300_type == 'multi' else len(tips300)*96
    tip50_count = 0
    tip300_count = 0

    def pick_up(pip):
        nonlocal tip50_count
        nonlocal tip300_count

        if pip == 'pip50':
            if tip50_count == tip50_max:
                robot.pause('Replace 300ul tipracks in slots \
' + slot_str50 + ' before resuming.')
                pip50.reset()
                tip50_count = 0
            pip50.pick_up_tip()
            tip50_count += 1
        else:
            if tip300_count == tip300_max:
                robot.pause('Replace 300ul tipracks in slots \
' + slot_str300 + ' before resuming.')
                pip300.reset()
                tip300_count = 0
            pip300.pick_up_tip()
            tip300_count += 1

    # Prepare the plates prior to touching any sample
    robot.comment("MESSAGE: the robot will now assemble the wash plates and \
    do the first transfer to the elution plate.")

    # Transfer 150uL of wash solution #1 to wash plate 1
    robot.comment("MESSAGE: creating wash plate 1.")
    pick_up('pip300')
    for dest in plate1:
        pip300.transfer(150, wash_sol1, dest, new_tip='never')
        pip300.blow_out(dest.top())
    pip300.drop_tip()

    # Transfer 150 uL of wash solution #2 to wash plate 2A
    robot.comment("MESSAGE: creating wash plate 2A.")
    pick_up('pip300')
    for dest in plate2A:
        pip300.transfer(150, wash_sol2a, dest, new_tip='never')
        pip300.blow_out(dest.top())
    pip300.drop_tip()

    # Wash plate 2B
    robot.comment("MESSAGE: creating wash plate 2B.")
    pick_up('pip300')
    for dest in plate2B:
        pip300.transfer(150, wash_sol2b, dest, new_tip='never')
        pip300.blow_out(dest.top())
    pip300.drop_tip()

    # Elution plate 1st buffer
    robot.comment("MESSAGE: transferring first buffer to elution plate.")
    pick_up('pip50')
    for dest in elution:
        pip50.transfer(elution_volume/2, elu_buff1, dest, new_tip='never')
        pip50.blow_out(dest.top())
    pip50.drop_tip()

    robot.home()
    robot.comment("MESSAGE: initial plate creation should now be complete.")

    # BREAK POINT #
    # this is when the user should add the sample plate

    robot.pause("USER ACTION: Add sample plate to position '4'. Empty the trash. \
When the sample plate has been unsealed and placed at '4'' please click PAUSE \
and then RESUME on the OT App")

    # Step 1 - Add Isopropanol to samples
    robot.comment("MESSAGE: adding isopropanol to each sample")
    for dest in samples300:
        pick_up('pip300')
        pip300.transfer(160, isopropanol, dest, new_tip='never')
        pip300.mix(5, 160, dest)  # Chaz question: do we need to specify dest?
        pip300.blow_out(dest.top())
        pip300.touch_tip()
        pip300.drop_tip()

    robot.home()
    robot.comment("USER ACTION: Empty the trash.")

    robot.comment("USER ACTION: Remove the sample plate from position '4'', \
seal the plate using a MicroAmp Clear Adhesive Film, then shake the sealed \
plate for 3 minutes at speed 7 on plate shaker. When shaking is complete \
remove the clear film and replace the plate in position '4'")

    robot.pause("USER ACTION: Vortex the DNA binding bead mix and load into \
    well A1 of the reagent trough. When you are ready please click RESUME on \
    the OT App")

    # Step 2 - Add DNA Binding Bead Mix
    robot.comment("MESSAGE: adding DNA Binding Bead mix to each sample")

    for dest in samples50:
        pick_up('pip50')
        pip50.mix(3, 40, bead_mix)
        pip50.blow_out(bead_mix.top())
        pip50.transfer(20, bead_mix, dest, new_tip='never')
        pip50.mix(5, 40, dest)
        pip50.blow_out(dest.top())
        pip50.touch_tip()
        pip50.drop_tip()

    # Step 3 - binding incubation
    robot.home()

    robot.comment("USER ACTION: Remove sample plate from '4'. The plate needs to \
    be sealed and placed on the plate shaker @ speed 7 for 3 mins.")

    # Step 4 - Wash 1
    robot.comment("USER ACTION: Unseal sample plate. Using the magnetic \
    pin tool, manually transfer beads from the sample plate to wash plate 1 \
    (position 1). Seal wash plate 1 and shake for 1 minute at speed 7 on \
    plate shaker.")

    # Step 5 - Wash 2A
    robot.comment("USER ACTION: Unseal wash plate 1. Using the magnetic pin \
    tool, \
    manually transfer beads from wash plate 1 to wash plate 2A (position 2). \
    Seal wash plate 2A and shake for 1 minute at speed 7 on plate shaker.")

    # Step 5 - Wash 2B
    robot.comment("USER ACTION: Unseal wash plate 2A. Using the magnetic pin \
    tool, \
    manually transfer beads from wash plate 2A to wash plate 2B (position 3). \
    Seal wash plate 2B and shake for 1 minute at speed 7 on plate shaker.")

    # Step 6 - Elution step 1
    robot.comment("USER ACTION: Unseal wash plate 2B. Using the magnetic \
    pin tool, \
    manually transfer beads from wash plate 2B to the elution plate \
    (position 6). Seal the elution plate and shake for 5 minutes at \
    900 rpm on \
    plate shaker at 70C. When you have completed this step unseal the elution \
    plate and place it in position E1.")

    robot.pause("USER ACTION: When you are ready to continue click RESUME \
    on the OT App")

    # Step 7 - Elution step 2
    robot.comment("MESSAGE: adding second elution buffer to \
    release DNA from beads")

    for dest in elution:
        pick_up('pip50')
        pip50.transfer(elution_volume/2, elu_buff2, dest, new_tip='never')
        pip50.mix(10, 40, dest)
        pip50.blow_out(dest.top())
        pip50.touch_tip()
        pip50.drop_tip()

    robot.home()
    robot.comment("USER ACTION: Remove the elution plate from '6'. \
    Using the magnetic pin tool, collect the beads from the elution plate and \
    discard the beads. Seal the elution plate for storage. Ensure the \
    elution plate is properly marked. Congratulations, you are done.")
