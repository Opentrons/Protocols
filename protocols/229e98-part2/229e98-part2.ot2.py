from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'BioFluid Mix and Transfer - Part 2/2',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# custom labware creation
vial_container = 'custom_agilent_samplevial_container'
if vial_container not in labware.list():
    labware.create(
        vial_container,
        grid=(5, 10),
        spacing=(18.3, 18.3),
        diameter=12,
        depth=32,
        volume=250
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

nano_container = 'custom_nanosep_tube_container'
if nano_container not in labware.list():
    labware.create(
        nano_container,
        grid=(8, 12),
        spacing=(9, 9),
        diameter=10,
        depth=10,
        volume=500
    )

sampvials = labware.load(vial_container, '3')
centtubes = labware.load(centr_container, '2')
ultratubes = labware.load(nano_container, '1')

tipracks = labware.load('opentrons_96_tiprack_300ul', '11', 'Tiprack 50/300ul')


def run_custom_protocol(
        p50_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('right', 'left') = 'right'
):

    # create pipette

    pip50 = instruments.P50_Single(mount=p50_mount)
    pip300 = instruments.P300_Single(mount=p300_mount)

    tip_max = 96
    tip_count = 0

    def pick_up(pip):
        nonlocal tip_count

        if tip_count == tip_max:
            robot.pause(
                'Replace 50/300ul tiprack in slot 11. \
                When ready, click RESUME.')
            pip50.reset()
            tip_count = 0
        if pip == pip50:
            pip50.pick_up_tip(tipracks.wells(tip_count))
        else:
            pip300.pick_up_tip(tipracks.wells(tip_count))
        tip_count += 1

    # Step 5

    for l in range(50):
        pick_up(pip50)
        pip50.transfer(20, ultratubes.wells(l), sampvials.wells(l),
                       new_tip='never')
        pip50.blow_out(sampvials.wells(l).top())
        pip50.drop_tip()

    robot.pause("Samples have been transferred to sample vial. Replace the \
    centrifuge tubes in slots 2/5/8 and when ready, click RESUME.")

    for p in range(50):
        pick_up(pip300)
        pip300.transfer(180, ultratubes.wells(p), centtubes.wells(p),
                        new_tip='never')
        pip300.blow_out(centtubes.wells(p).top())
        pip300.drop_tip()

    robot.comment("Part 2 complete, protocol is now finished.")
