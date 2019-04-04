from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'CSV Plate Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = '24-well-plate'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(6, 4),
        spacing=(20, 20),
        diameter=16,
        depth=14,
        volume=1000
    )

# labware
trough = labware.load('trough-12row', '3')
tips300 = [labware.load('opentrons-tiprack-300ul', slot)
           for slot in ['6', '9']]
tubes_50 = labware.load('opentrons-tuberack-50ml', '11')

# modules
tempdeck = modules.load('tempdeck', '4')
plate = labware.load('24-well-plate', '4', share=True)
tempdeck.set_temperature(60)
tempdeck.wait_for_temp()

# pipette
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=tips300
)

# reagent setup
water = trough.wells('A1')
crystal_violet = trough.wells('A2')
acetic_acid = trough.wells('A3')


def run_custom_protocol():
    robot.pause("Place the 24-well plate on the tempdeck. Wait 60 minutes "
                "for the wells to dry at 60˚C before resuming. After resuming "
                "the tempdeck will decrease to 22˚C before the protocol "
                "continues.")

    tempdeck.set_temperature(22)
    tempdeck.wait_for_temp()

    # distribute crystal violet to all wells
    p300.distribute(250,
                    crystal_violet,
                    [well.top() for well in plate.wells()])

    # incubate for 5 minutes
    p300.delay(minutes=5)

    # transfer out crystal violet to 50ml tube
    p300.transfer(250,
                  [well.bottom(1) for well in plate.wells()],
                  tubes_50.wells('A1'),
                  new_tip='always')

    for _ in range(3):
        # distribute water to all wells
        p300.distribute(750, water, [well.top() for well in plate.wells()])

        for well in plate.wells():
            # mix contents of all wells
            p300.pick_up_tip()
            p300.mix(300, 10, well)

            # transfer out water to 50ml tube
            p300.transfer(750,
                          [well.bottom(1) for well in plate.wells()],
                          tubes_50.wells('A2'),
                          new_tip='never')
            p300.drop_tip()

    tempdeck.set_temperature(37)
    tempdeck.wait_for_temp()

    # incubate for 30 minutes
    p300.delay(minutes=30)

    # distribute acetic acid to all wells
    p300.distribute(750,
                    acetic_acid,
                    [well.top() for well in plate.wells()])
