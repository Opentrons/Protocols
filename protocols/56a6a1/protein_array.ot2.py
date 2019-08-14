from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Protein Array',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
custom_shaker_name = 'teleshake1536_64_slides_100ul'
if custom_shaker_name not in labware.list():
    labware.create(
        custom_shaker_name,
        grid=(4, 8),
        spacing=(27, 9),
        diameter=7,
        depth=4,
        volume=100
    )

# load modules and labware
res_12 = labware.load(
    'usascientific_12_reservoir_22ml', '3', 'reagent reservoir')
shake_plate = labware.load(
    custom_shaker_name, '4', 'Teleshake with slides mounted')
liquid_trash = labware.load(
    'agilent_1_reservoir_290ml', '6', 'liquid trash').top()

# reagents
super_g_blocking_buffer = res_12.wells('A1')
antibody_2 = res_12.wells('A2')
pbst = res_12.wells('A3', length=2)


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        number_of_slides_to_process: int = 4,
        sample_addition: StringSelection(
            'manually add samples',
            'automatically add samples from PCR plate'
        ) = 'manually add samples'
):
    # checks
    if number_of_slides_to_process > 4 or number_of_slides_to_process < 1:
        raise Exception('Invalid number of slides to process. Please input a \
number between 1 and 4.')

    # pipettes
    if (
        number_of_slides_to_process > 2
        and sample_addition == 'automatically add samples from PCR plate'
    ):
        tip_slots = ['7', '8', '9']
    else:
        tip_slots = ['7', '8']
    tips300 = [labware.load('opentrons_96_tiprack_300ul', slot)
               for slot in tip_slots]
    m300 = instruments.P300_Multi(mount=p300_multi_mount, tip_racks=tips300)

    # setup slide wells
    aspirate_locs = [
        loc for well in shake_plate.rows('A')[:number_of_slides_to_process]
        for loc in [
            well.top(), (well, well.from_center(r=2.571, h=1, theta=0))]
    ]
    dispense_locs = [
        loc for well in shake_plate.rows('A')[:number_of_slides_to_process]
        for loc in [
            well.top(4), (well, well.from_center(r=2.571, h=3, theta=0))]
    ]

    # distribute blockin buffer
    m300.distribute(
        100, super_g_blocking_buffer, dispense_locs, disposal_vol=0)

    robot.pause("Shake for 30 minutes at room temperature on TeleShake before \
resuming.")

    # completely transfer out buffer
    m300.transfer(150, aspirate_locs, liquid_trash, blow_out=True)

    # PBST washes
    for ind in range(2):
        m300.distribute(100, pbst[ind], dispense_locs, disposal_vol=0)
        # incubate
        m300.delay(minutes=5)
        m300.transfer(150, aspirate_locs, liquid_trash, blow_out=True)

    if sample_addition == 'manually add samples':
        pause_str = 'Manually add samples to slides. Incubate the samples by \
gentle agitation for 1 hour using TeleShake before resuming.'
    else:
        sample_plate = labware.load(
            'biorad_96_wellplate_200ul_pcr', '10', 'sample plate')
        samples = sample_plate.rows('A')[:number_of_slides_to_process*2]
        m300.transfer(100, samples, dispense_locs, new_tip='always')
        pause_str = 'Incubate the samples by gentle agitation for 1 hour \
using TeleShake before resuming.'

    robot.pause(pause_str)

    # completely transfer out liquid
    m300.transfer(150, aspirate_locs, liquid_trash, blow_out=True)

    # wash sequence
    def wash(wash_ind, final_aspirate=True):
        m300.distribute(100, pbst[wash_ind], dispense_locs, disposal_vol=0)
        # incubate
        m300.delay(minutes=5)
        m300.transfer(150, aspirate_locs, liquid_trash, blow_out=True)

        m300.distribute(
            100, super_g_blocking_buffer, dispense_locs, disposal_vol=0)
        # incubate
        m300.delay(minutes=5)
        m300.transfer(150, aspirate_locs, liquid_trash, blow_out=True)

        m300.distribute(100, pbst[wash_ind], dispense_locs, disposal_vol=0)
        # incubate
        m300.delay(minutes=5)
        if final_aspirate:
            m300.transfer(150, aspirate_locs, liquid_trash, blow_out=True)

    wash(wash_ind=0)

    m300.distribute(100, antibody_2, dispense_locs, disposal_vol=0)

    robot.pause('Incubate the samples by gentle agitation for 1 hour using \
TeleShake before resuming.')

    m300.transfer(150, aspirate_locs, liquid_trash, blow_out=True)

    wash(wash_ind=1, final_aspirate=False)

    robot.comment('Take off slides from FastFrame and place into 50 ml \
conical tube filled with 45 ml PBS, and wash by agitating on TeleShake for 5 \
minutes. Briefly rinse the slides 2 times using a 50 ml conical tube with \
ddH2O. Spin at 300 rpm using Beckman-Coulter Avant J-E Centrifuge at RT for 4 \
minutes. Scan the slides with GenePix 4400 A.')
