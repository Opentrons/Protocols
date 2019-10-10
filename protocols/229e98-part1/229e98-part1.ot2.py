from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'BioFluid Mix and Transfer - Part 1/2',
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

cryovials = labware.load(cryo_container, '3')
centtubes = labware.load(centr_container, '2')
ultratubes = labware.load(nano_container, '1')
tempdeck = modules.load('tempdeck', '10')

track = 'opentrons_24_aluminumblock_nest_1.5ml_snapcap'
if track not in labware.list():
    labware.create(
        track,
        grid=(6, 4),
        spacing=(17.25, 17.25),
        diameter=10.20,
        depth=37.9,
        volume=1500
    )
temprack = labware.load(track, '10',
                        share=True)
tempdeck.set_temperature(4)
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

    # Step 1 - mix bio-fluid and transfer 50uL

    for i in range(50):
        pick_up(pip300)
        pip300.mix(5, 50, cryovials.wells(i))
        pip300.blow_out(cryovials.wells(i).top())
        pip300.transfer(50, cryovials.wells(i), centtubes.wells(i),
                        new_tip='never')
        pip300.blow_out(centtubes.wells(i).top())
        pip300.drop_tip()

    # Step 2 - transfer 20ul aliquot of solution
    tempdeck.wait_for_temp()

    for j in range(50):
        pick_up(pip50)
        pip50.transfer(20, temprack.wells(0), centtubes.wells(j),
                       new_tip='never')
        pip50.mix(3, 35, centtubes.wells(j))
        pip50.blow_out(centtubes.wells(j).top())
        pip50.drop_tip()

    # Step 3 + 4 transfer 130ul solution then transfer 200 to nanosep tubes

    for k in range(50):
        m = (k//10) + 1
        pick_up(pip300)
        pip300.transfer(130, temprack.wells(m), centtubes.wells(k),
                        new_tip='never')
        pip300.mix(3, 150, centtubes.wells(k))
        pip300.blow_out(centtubes.wells(k).top())
        pip300.transfer(200, centtubes.wells(k), ultratubes.wells(k),
                        new_tip='never')
        pip300.blow_out(ultratubes.wells(k).top())
        pip300.drop_tip()

    robot.comment("Part 1 is now complete. Please remove samples from OT-2 for \
    centrifugation. After centrifugation, replace samples on the deck and run \
    Part 2. Be sure to replace the cryovials in slots 3/6/9 with sample \
    vials. Lastly, replace the tiprack in slot 11 with a full rack.")
