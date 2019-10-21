from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'BioFluid Transfer (Step 1)',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# custom labware creation
cryo_container = 'custom_agilent_cryovial_container'
if cryo_container not in labware.list():
    labware.create(
        cryo_container,
        grid=(5, 10),
        spacing=(18.3, 18.3),
        diameter=12,
        depth=48,
        volume=6000
    )

centr_container = 'custom_centrifuge_tube_container'
if centr_container not in labware.list():
    labware.create(
        centr_container,
        grid=(8, 12),
        spacing=(9, 9),
        diameter=7.5,
        depth=30.5,
        volume=500
    )

cryovials = labware.load(cryo_container, '3')  # slots 3/6/9
centtubes = labware.load(centr_container, '2')  # slots # 2/5/8

tslots = ['1', '4', '7', '10', '11']
tipracks = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in tslots
]


def run_custom_protocol(
        p300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 50
):

    # create pipette
    pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tipracks)

    tip_max = len(tipracks)*96
    tip_count = 0

    def pick_up():
        nonlocal tip_count

        if tip_count == tip_max:
            robot.pause(
                'Replace 300ul tipracks in slots \
                1, 4, 7, 10, and 11 before resuming.')
            pip300.reset()
            tip_count = 0
        pip300.pick_up_tip()
        tip_count += 1

    for i in range(number_of_samples):
        wellno = i % 50
        pick_up()
        pip300.mix(5, 50, cryovials.wells(wellno))
        pip300.blow_out(cryovials.wells(wellno).top())
        pip300.transfer(50, cryovials.wells(wellno), centtubes.wells(wellno),
                        new_tip='never')
        pip300.blow_out(centtubes.wells(wellno).top())
        pip300.drop_tip()
        if i == number_of_samples-1:
            robot.comment('Sample transfer is now complete.')
        elif wellno == 49:
            robot.pause('Please remove cryovials and centrifuge tubes and \
            replace with new cryovials and centrifuge tubes. Press "resume" \
            when ready to continue.')
