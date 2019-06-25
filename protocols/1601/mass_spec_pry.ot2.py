from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Mass Spec Sample Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
rack_name_1 = '5x10-false-bottom-3ml'
if rack_name_1 not in labware.list():
    labware.create(
        rack_name_1,
        grid=(10, 5),
        spacing=(18.5, 18.5),
        diameter=11,
        depth=50,
        volume=3000
    )

rack_name_2 = '5x10-filter-vial'
if rack_name_2 not in labware.list():
    labware.create(
        rack_name_2,
        grid=(10, 5),
        spacing=(18.5, 18.5),
        diameter=6.25,
        depth=24,
        volume=450
    )

tips_name = 'Globe-Scientific-tiprack-200ul'
if tips_name not in labware.list():
    labware.create(
        tips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60
    )

# load labware
trough = labware.load('trough-12row', '1', 'reagent trough')
tips = labware.load(tips_name, '4')
urine_samples = labware.load(rack_name_1, '8', 'urine sample tubes')
destination_vials = labware.load(rack_name_2, '9', 'filter vials')


def run_custom_protocol(
        P300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 50,
        pre_incubation_steps: StringSelection('yes', 'no') = 'yes',
        post_incubation_steps: StringSelection('yes', 'no') = 'no'
):

    # check inputs
    if number_of_samples > 50 or number_of_samples < 1:
        raise Exception('Please enter a valid number of samples (1-50)')

    # pipette
    p300 = instruments.P300_Single(mount=P300_mount, tip_racks=[tips])

    # sample setup
    vials = destination_vials.wells()[0:number_of_samples]
    urine = urine_samples.wells()[0:number_of_samples]
    mm = trough.wells('A1')
    diluent = trough.wells('A2')

    if pre_incubation_steps == 'yes':

        # transfer mstermix to each destination vial
        p300.pick_up_tip()
        for dest in vials:
            p300.transfer(
                50,
                mm,
                dest.top(),
                blow_out=True,
                new_tip='never'
            )
        p300.drop_tip()

        # transfer urine samples to corresponding destination vial
        p300.transfer(
            50,
            urine,
            vials,
            blow_out=True,
            new_tip='always'
        )

        robot.pause('Incubate filter vials now containing mastermix and sample\
s. Reload the rack in slot 8 before resuming.')

    if post_incubation_steps == 'yes':
        # transfer diluent to each destination vial
        p300.pick_up_tip()
        for dest in vials:
            p300.transfer(
                300,
                diluent,
                dest,
                blow_out=True,
                new_tip='never'
            )
        p300.drop_tip()
