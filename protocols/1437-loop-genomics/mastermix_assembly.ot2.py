from opentrons import labware, instruments, robot

custom_deep_plate = '96-deep-well-1.2ml'
if custom_deep_plate not in labware.list():
    labware.create(
        custom_deep_plate,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.4,
        depth=33.5)


# labware setup
tuberack1 = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
tuberack2 = labware.load('opentrons-tuberack-2ml-eppendorf', '2')
deep_well3 = labware.load(custom_deep_plate, '3')
pcr4 = labware.load('PCR-strip-tall', '4')
pcr5 = labware.load('PCR-strip-tall', '5')
deep_well6 = labware.load(custom_deep_plate, '6')
pcr7 = labware.load('PCR-strip-tall', '7')
pcr8 = labware.load('PCR-strip-tall', '8')
tiprack = labware.load('tiprack-200ul', '9')
pcr10 = labware.load('PCR-strip-tall', '10')
pcr11 = labware.load('PCR-strip-tall', '11')

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack])
m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tiprack])

for index in range(3):
    m50.pick_up_tip()
    m50.transfer(
        40, deep_well6.cols(index), deep_well3.cols(index), new_tip='never')
    m50.mix(5, 50, deep_well3.cols(index))
    m50.drop_tip()

    m50.pick_up_tip()
    m50.transfer(
        40, deep_well6.cols(index), deep_well3.cols(index), new_tip='never')
    m50.mix(5, 50, deep_well3.cols(index))
    dest1 = [plate.cols(index) for plate in [pcr10, pcr11, pcr7]]
    m50.distribute(15, deep_well3.cols(index), dest1, new_tip='never')
    dest2 = [plate.cols(index) for plate in [pcr8, pcr4, pcr5]]
    m50.distribute(15, deep_well3.cols(index), dest2, new_tip='never')
    m50.drop_tip()

robot.pause("Swap out the PCR plates in position 4, 5, 7, 8, 10, 11.")

for index in range(3):
    m50.pick_up_tip()
    dest1 = [plate.cols(index) for plate in [pcr10, pcr11, pcr7]]
    m50.distribute(15, deep_well3.cols(index), dest1, new_tip='never')
    dest2 = [plate.cols(index) for plate in [pcr8, pcr4, pcr5]]
    m50.distribute(15, deep_well3.cols(index), dest2, new_tip='never')
    m50.drop_tip()

robot.pause("Swap out the PCR plates in position 4, 5, 7, 8, 10, 11.")

p50.start_at_tip(tiprack.wells('A10'))

p50.set_flow_rate(aspirate=12.5, dispense=25)
p50.transfer(18, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.set_flow_rate(aspirate=25, dispense=50)
p50.transfer(36, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))

robot.pause("Remove tubes in position 2 and restock with new tubes.")

p50.set_flow_rate(aspirate=12.5, dispense=25)
p50.transfer(5, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.set_flow_rate(aspirate=25, dispense=50)
p50.transfer(88, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))

robot.pause("Remove tubes in position 2 and restock with new tubes.")

p50.set_flow_rate(aspirate=12.5, dispense=25)
p50.transfer(5, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.transfer(5, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))

robot.pause("Remove tubes in position 2 and restock with new tubes.")

p50.transfer(25, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.transfer(13, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))

robot.pause("Remove tubes in position 2 and restock with new tubes.")

p50.transfer(46, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.transfer(13, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))

robot.pause("Remove tubes in position 2 and restock with new tubes.")

p50.transfer(30, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.set_flow_rate(aspirate=25, dispense=50)
p50.transfer(18, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))

robot.pause("Remove tubes in position 2 and restock with new tubes.")

p50.transfer(18, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.transfer(18, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))

robot.pause("Remove tubes in position 2 and restock with new tubes.")

p50.transfer(18, tuberack1.wells('A1'), tuberack1.wells('B1', to='D6'))

robot.pause("Remove tubes in position 1 and restock with new tubes.")

p50.transfer(36, tuberack2.wells('A1'), tuberack2.wells('B1', to='D6'))
