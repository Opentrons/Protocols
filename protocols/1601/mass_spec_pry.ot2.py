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
        grid=(5, 10),
        spacing=(18.5, 18.5),
        diameter=11,
        depth=50,
        volume=3000
    )

rack_name_2 = '5x10-filter-vial'
if rack_name_2 not in labware.list():
    labware.create(
        rack_name_2,
        grid=(5, 10),
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

max_speed_per_axis = {
    'x': 600, 'y': 400, 'z': 125, 'a': 125, 'b': 50, 'c': 50
}
robot.head_speed(
    combined_speed=max(max_speed_per_axis.values()),
    **max_speed_per_axis
)


def run_custom_protocol(
        P300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 50,
        mastermix_distribution: StringSelection('yes', 'no') = 'yes',
        sample_transfer: StringSelection('yes', 'no') = 'yes',
        post_incubation_dilution: StringSelection('yes', 'no') = 'no'
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

    if mastermix_distribution == 'yes':

        # transfer mastermix to each destination vial
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

    if sample_transfer == 'yes':

        # transfer urine samples to corresponding destination vial
        for source, dest in zip(urine, vials):
            offset1 = (source, source.from_center(r=0, theta=90, h=3.0))
            offset2 = (source, source.from_center(r=0.84, theta=90, h=3.0))
            offset3 = (dest, dest.from_center(r=1.5, theta=90, h=6.25))
            p300.pick_up_tip()
            p300.aspirate(50, source)
            p300.move_to(offset1)
            p300.move_to(offset2)
            p300.move_to(offset3)
            p300.dispense(50, dest.top())
            p300.blow_out(dest.top())
            p300.drop_tip()

    if post_incubation_dilution == 'yes':

        if mastermix_distribution == 'yes' or sample_transfer == 'yes':
            robot.pause('Incubate filter vials now containing mastermix and \
samples. Reload the rack in slot 8 before resuming.')

        # transfer diluent to each destination vial
        p300.pick_up_tip()
        for dest in vials:
            p300.transfer(
                300,
                diluent,
                dest.top(),
                blow_out=True,
                new_tip='never'
            )
        p300.drop_tip()
