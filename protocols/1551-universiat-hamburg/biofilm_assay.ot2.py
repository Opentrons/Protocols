from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Biofilm Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'custom-24-well-plate'
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
plate = labware.load('custom-24-well-plate', '4', share=True)
if not robot.is_simulating():
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

if not robot.is_simulating():
    robot.comment("The protocol will pause for 60 minutes for the wells to "
                  "dry at 60˚C before resuming. After resuming, the "
                  "temperature module will decrease to 22˚C before the "
                  "protocol continues.")
    robot.delay(minutes=60)
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
              [well for well in plate.wells()],
              tubes_50.wells('A1'),
              new_tip='always')

for _ in range(3):
    # distribute water to all wells
    p300.transfer(750, water, [well.top() for well in plate.wells()])

    for well in plate.wells():
        # mix contents of all wells
        p300.pick_up_tip()
        p300.mix(300, 10, well)

        # transfer out water to 50ml tube
        p300.transfer(750,
                      [well for well in plate.wells()],
                      tubes_50.wells('A2'),
                      new_tip='never')
        p300.drop_tip()

tempdeck.set_temperature(37)
tempdeck.wait_for_temp()

# incubate for 30 minutes
p300.delay(minutes=30)

# distribute acetic acid to all wells
p300.transfer(750,
              acetic_acid,
              [well.top() for well in plate.wells()])
