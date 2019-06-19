from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

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
reagent_tubes = labware.load('opentrons-tuberack-15ml', '1', 'reagent tubes')
tips = labware.load(tips_name, '4')
urine_samples = labware.load(rack_name_1, '8', 'urine sample tubes')
destination_vials = labware.load(rack_name_2, '9', 'filter vials')


def run_custom_protocol(
        P300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 50
        ):

    # check inputs
    if number_of_samples > 50 or number_of_samples < 1:
        raise Exception('Please enter a valid number of samples (1-50)')

    # pipette
    p300 = instruments.P300_Single(mount=P300_mount, tip_racks=[tips])

    # sample setup
    vials = destination_vials.wells()[0:number_of_samples]
    urine = urine_samples.wells()[0:number_of_samples]
    mm = reagent_tubes.wells('A1')
    diluent = reagent_tubes.wells('B1')

    # height track and transfer mm to each destination vial
    h = {
        'mm': -35,
        'diluent': -35
        }
    r_cyl = 7.4

    def h_track(vol, reagent):
        nonlocal h
        dh = vol/(math.pi*(r_cyl**2))
        h[reagent] -= dh

    p300.pick_up_tip()
    for dest in vials:
        h_track(50, 'mm')
        p300.transfer(
            50,
            mm.top(h['mm']),
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

    robot.pause('Incubate filter vials now containing mastermix and samples. '
                'Reload the rack in slot 8 before resuming.')

    # height track and transfer diluent to each destination vial
    p300.pick_up_tip()
    for dest in vials:
        h_track(300, 'diluent')
        p300.transfer(
            300,
            diluent.top(h['diluent']),
            dest,
            blow_out=True,
            new_tip='never'
        )
    p300.drop_tip()
