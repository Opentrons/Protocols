"""
Social.Links@usask.ca

Todo: change rest position to x-axis home above garbage

Change garbage @ DNA binding mix?

Need to dispense the DNA binding mix at the bottom of the well

How can we do some of the < 30 ul transfers with the multichannel?

The deck on the OT-2 looks like this:

[10] [11] [trash]
[7]  [8]  [9]
[4]  [5]  [6]
[1]  [2]  [3]

and for this protocol, the labware is arranged like so:

[tip_rack3]     [tip_rack4]       [trash]
[tip_rack1]     [tip_rack2]       [empty]
[sample_plate]  [reagent_trough]  [elution_plate]
[wash_plate1]   [wash_plate2A]    [wash_plate2B]

"""

from opentrons import labware, instruments, robot

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

# we need 5 x tip racks

# for the multichannel these need empty deck locations to their immediate
# left so that the single channel does not collide
tip_rack1 = labware.load('tipone_96_tiprack_200ul', '7', 'tip rack 1')
tip_rack2 = labware.load('tipone_96_tiprack_200ul', '8', 'tip rack 2')
tip_rack3 = labware.load('tipone_96_tiprack_200ul', '10', 'tip rack 3')
tip_rack4 = labware.load('tipone_96_tiprack_200ul', '11', 'tip rack 4')

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

# trash container
# trash = containers.load('trash-box', 'D3') - not needed

# add a multichannel p50

p50m = instruments.P50_Multi(
    mount='left',
    tip_racks=[tip_rack1, tip_rack2, tip_rack3, tip_rack4]
    )


def run_custom_protocol(elution_volume: float = 100):
    # watch out for volume being larger than the max supported by the pipette

    # initialize the robot - do we need in v2?
    # robot.connect('Virtual Smoothie')

    # Prepare the plates prior to touching any sample
    robot.comment("MESSAGE: the robot will now assemble the wash plates and \
    do the first transfer to the elution plate.")

    # Wash plate 1
    robot.comment("MESSAGE: creating wash plate 1.")
    p50m.transfer(150, wash_sol1, wash_plate1.cols())

    # Wash plate 2A
    robot.comment("MESSAGE: creating wash plate 2A.")
    p50m.transfer(150, wash_sol2a, wash_plate2A.cols())
    # Wash plate 2B
    robot.comment("MESSAGE: creating wash plate 2B.")
    p50m.transfer(150, wash_sol2b, wash_plate2B.cols())
    # Elution plate 1st buffer
    robot.comment("MESSAGE: transferring first buffer to elution plate.")
    p50m.transfer(elution_volume/2, elu_buff1, elution_plate.cols())

    robot.home()
    robot.comment("MESSAGE: initial plate creation should now be complete.")

    # BREAK POINT #
    # this is when the user should add the sample plate
    """
    robot.pause("USER ACTION: Add sample plate to position A2. Empty the trash. \
When the sample plate has been unsealed and placed at A2 please click PAUSE \
and then RESUME on the OT App")

    # Step 1 - Add Isopropanol to samples
    # don't bother mixing?
    robot.comment("MESSAGE: adding isopropanol to each sample")
    p50m.transfer(160, isopropanol, sample_plate, new_tip='always')

    robot.home()
    robot.comment("USER ACTION: Empty the trash.")

    robot.comment("USER ACTION: Remove the sample plate from position A2, \
seal the plate using a MicroAmp Clear Adhesive Film, then shake the sealed \
plate for 3 minutes at speed 7 on plate shaker. When shaking is complete \
remove the clear film and replace the plate in position A2")

    robot.pause("USER ACTION: Vortex the DNA binding bead mix and load into \
    well A1 of the reagent trough. When you are ready please click RESUME on \
    the OT App")

    # Step 2 - Add DNA Binding Bead Mix
    robot.comment("MESSAGE: adding DNA Binding Bead mix to each sample")
    # should this mix before aspirating?
    p50m.transfer(
        20,
        bead_mix,
        sample_plate,
        new_tip='always',
        mix_before=(2, 50),
        mix_after=(5, 50),
        blow_out=True
    )

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
    p50m.transfer(
        int(elution_volume/2),
        elu_buff2,
        elution_plate,
        new_tip='always'
    )

    robot.home()
    robot.comment("USER ACTION: Remove the elution plate from '6'. \
    Using the magnetic pin tool, collect the beads from the elution plate and \
    discard the beads. Seal the elution plate for storage. Ensure the \
    elution plate is properly marked. Congratulations, you are done.")
    """
