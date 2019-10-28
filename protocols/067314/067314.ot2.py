from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Mass Spec Sample Prep',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create labware

res = 'analytical_1_reservoir_170ml'
if res not in labware.list():
    labware.create(
        res,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=106,
        depth=20,
        volume=170000
    )
meoh = labware.load(res, '2', 'MeOH')
formic = labware.load(res, '3', '0.1% Formic Acid')
meoh5 = labware.load(res, '4', '5% MeOH in H2O')
tfa = labware.load(res, '5', '26mM TFA in ACN')

elution_plate = 'oasis_96_elutionplate'
if elution_plate not in labware.list():
    labware.create(
        elution_plate,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.1,
        depth=15,
        volume=500
    )
elution = labware.load(elution_plate, '1', 'Elution Plate')

deep_plate = 'usascientific_96_wellplate_2.4ml_deep'


def run_custom_protocol(
        pipette_type: StringSelection(
            'P300_Multi', 'P50_Multi',
            'P1000_Single', 'P300_Single', 'P50_Single') = 'P300_Multi',
        pipette_mount: StringSelection('left', 'right') = 'left',
        number_of_samples: int = 96
):

    # Sample Check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Number of Samples should be between 1 and 96.')

    # Create pipettes
    pipsm = pipette_type.split('_')[1]

    if pipsm == 'Multi':
        num_cols = math.ceil(number_of_samples/8)
        samps = elution.rows('A')[:num_cols]
    else:
        samps = elution.wells()[:number_of_samples]

    tips = [labware.load('opentrons_96_tiprack_300ul', str(slot))
            for slot in range(7, 12)]

    if pipette_type == 'P1000_Single':
        tips = [labware.load('opentrons_96_tiprack_1000ul', str(slot))
                for slot in range(7, 12)]
        pip = instruments.P1000_Single(mount=pipette_mount, tip_racks=tips)
    elif pipette_type == 'P300_Single':
        pip = instruments.P300_Single(mount=pipette_mount, tip_racks=tips)
    elif pipette_type == 'P300_Multi':
        pip = instruments.P300_Multi(mount=pipette_mount, tip_racks=tips)
    elif pipette_type == 'P50_Single':
        pip = instruments.P50_Single(mount=pipette_mount, tip_racks=tips)
    elif pipette_type == 'P50_Multi':
        pip = instruments.P50_Multi(mount=pipette_mount, tip_racks=tips)

    def fntransfer(src, vol):
        for s in samps:
            pip.pick_up_tip()
            pip.transfer(vol, src, s, new_tip='never', air_gap=20)
            pip.blow_out(s.top())
            pip.drop_tip()

    fntransfer(meoh, 200)
    robot.pause('Remove plate from OT-2 and allow to pass through into waste \
    collection container. Use mild pressure as needed to facilitate movement. \
    When ready to continue, replace the plate in the OT-2 and click RESUME.')

    fntransfer(formic, 200)
    robot.pause('Remove plate from OT-2 and allow to pass through into waste \
    collection container. Use mild pressure as needed to facilitate movement. \
    When ready to continue, replace the plate in the OT-2 and click RESUME.')

    fntransfer(meoh5, 200)
    robot.pause('Remove plate from OT-2 and allow to pass through into waste \
    collection container. Use mild pressure as needed to facilitate movement. \
    When ready to continue, replace the plate in the OT-2 and click RESUME.')

    fntransfer(tfa, 500)
    robot.pause('Remove plate from OT-2 and allow to pass through into waste \
    collection container. Use mild pressure as needed to facilitate movement. \
    After drying sample offline, replace the plate and click RESUME.')

    fntransfer(formic, 200)
    robot.comment('You have successfully completed this protocol.')
