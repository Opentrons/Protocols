from opentrons import labware, instruments, modules, robot

# labware setup
strips = labware.load('PCR-strip-tall', '3')
cold_block = labware.load('tempdeck', '2')
cold_strips = labware.load('PCR-strip-tall', '2', share=True)

tipracks = [labware.load('opentrons-tiprack-300ul', slot)
            for slot in ['4', '5']]

trough = labware.load('trough-12row', '6')

mag_deck = modules.load('magdeck', '9')
mag_plate = labware.load('biorad-hardshell-96-PCR', '9', share=True)

heat_block = modules.load('tempdeck', '11')
heat_strips = labware.load('PCR-strip-tall', '11', share=True)

# instruments setup
m50 = instruments.P50_Multi(
    mount='left',
    tip_racks=tipracks)
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks)

# reagent setup
EDTA = strips.cols('2')
ampure_beads1 = strips.cols('3')
ampure_beads2 = strips.cols('4')
trisHCl = strips.cols('5')
ligation_beads = strips.cols('6')
cleanup_buffer1 = strips.cols('7')
cleanup_buffer2 = strips.cols('8')
water = strips.cols('9')
NaOH = strips.cols('10')
ethanol = trough.wells('A1')
trash_loc = m300.trash_container.top()

"""
Fragmentation
"""

heat_block.set_temperature(37)
heat_block.wait_for_temp()

m300.pick_up_tip()
m300.transfer(50, strips.cols('1'), cold_strips.cols('1'), new_tip='never')
m300.mix(5, 50, cold_strips.cols('2'))
m300.transfer(50, cold_strips.cols('1'), heat_strips.cols('1'),
              new_tip='never')
m300.drop_tip()

m300.delay(minutes=12)

m50.pick_up_tip(tipracks[0].cols('2'))
m50.transfer(10, EDTA, heat_strips.cols('1'), new_tip='never')
m50.mix(5, 50, heat_strips.cols('1'))
m50.drop_tip()

m300.start_at_tip(tipracks[0].cols('3'))
m300.pick_up_tip()
m300.transfer(60, heat_strips.cols('1'), cold_strips.cols('2'),
              new_tip='never')
heat_block.set_temperature(25)
m300.delay(minutes=5)
heat_block.wait_for_temp()
m300.aspirate(60, cold_strips.cols('2'))
m300.dispense(50, mag_plate.cols('1'))
m300.drop_tip()

m300.pick_up_tip()
m300.mix(5, 100, ampure_beads1)
m300.transfer(150, ampure_beads1, mag_plate.cols('1'), new_tip='never')
m300.delay(minutes=5)
mag_deck.engage()
m300.delay(minutes=4)
m300.transfer(210, mag_plate.cols('1'), trash_loc, new_tip='never')
m300.drop_tip()

for index in range(2):
    m300.pick_up_tip()
    m300.transfer(200, ethanol, mag_plate.cols('1'), new_tip='never')
    m300.delay(seconds=30)
    m300.transfer(210, mag_plate.cols('1'), trash_loc, new_tip='never')
    if index == 1:
        m300.transfer(50, mag_plate.cols('1'), trash_loc, new_tip='never')
    m300.drop_tip()

m300.delay(minutes=5)
mag_deck.disengage()

m300.pick_up_tip()
col_edge = (mag_plate.cols('1')[0],
            mag_plate.cols('1')[0].from_center(r=1, h=0.5, theta=0))
m300.transfer(52, trisHCl, col_edge, new_tip='never')
m300.mix(10, 50, mag_plate.cols('1'))
mag_deck.engage()
m300.delay(minutes=2)
m300.transfer(50, mag_plate.cols('1'), cold_strips.cols('3'), new_tip='never')
mag_deck.disengage()

"""
End Repair
"""
m300.mix(5, 50, cold_strips.cols('3'))
heat_block.wait_for_temp()
m300.transfer(50, cold_strips.cols('3'), heat_strips.cols('2'), new_tip='never')
m300.delay(minutes=30)
m300.transfer(50, heat_strips.cols('2'), mag_plate.cols('2'), new_tip='never')
m300.drop_tip()

heat_block.set_temperature(37)
heat_block.wait_for_temp()

m300.pick_up_tip()
m300.mix(5, 50, ampure_beads2)
m300.transfer(125, ampure_beads2, mag_plate.cols('2'), new_tip='never')
m300.mix(5, 100, mag_plate.cols('2'))
m300.delay(minutes=5)
mag_deck.engage()
m300.delay(minutes=4)
m300.transfer(250, mag_plate.cols('2'), trash_loc, new_tip='never')
m300.drop_tip()

for index in range(2):
    m300.pick_up_tip()
    m300.transfer(200, ethanol, mag_plate.cols('1'), new_tip='never')
    m300.delay(seconds=30)
    m300.transfer(210, mag_plate.cols('1'), trash_loc, new_tip='never')
    if index == 1:
        m300.transfer(50, mag_plate.cols('1'), trash_loc, new_tip='never')
    m300.drop_tip()

m300.delay(minutes=5)
mag_deck.disengage()

m300.pick_up_tip()
col_edge = (mag_plate.cols('2')[0],
            mag_plate.cols('2')[0].from_center(r=1, h=0.5, theta=0))
m300.transfer(22, trisHCl, col_edge, new_tip='never')
m300.mix(10, 20, mag_plate.cols('2'))
mag_deck.engage()
m300.delay(minutes=2)
m300.transfer(20, mag_plate.cols('2'), cold_strips.cols('4'), new_tip='never')
m300.drop_tip()
mag_deck.disengage()

"""
Ligation Step 1
"""
m50.pick_up_tip(tipracks[0].cols('12'))
m50.mix(5, 20, cold_strips.cols('4'))
heat_block.wait_for_temp()
m50.transfer(20, cold_strips.cols('4'), heat_strips.cols('3'), new_tip='never')
m50.delay(minutes=15)
m50.transfer(20, heat_strips.cols('3'), cold_strips.cols('5'), new_tip='never')
heat_block.set_temperature(22)
m50.delay(minutes=5)
heat_block.wait_for_temp()
m50.transfer(20, cold_strips.cols('5'), mag_plate.cols('3'), new_tip='never')
m50.drop_tip()

m300.start_at_tip(tipracks[1].cols('1'))
m300.pick_up_tip()
m300.mix(5, 50, ampure_beads2)
m300.transfer(50, ampure_beads2, mag_plate.cols('3'), new_tip='never')
m300.mix(5, 100, mag_plate.cols('3'))
m300.delay(minutes=5)
mag_deck.engage()
m300.delay(minutes=4)
m300.transfer(250, mag_plate.cols('3'), trash_loc, new_tip='never')
m300.drop_tip()

for index in range(2):
    m300.pick_up_tip()
    m300.transfer(200, ethanol, mag_plate.cols('3'), new_tip='never')
    m300.delay(seconds=30)
    m300.transfer(210, mag_plate.cols('3'), trash_loc, new_tip='never')
    if index == 1:
        m300.transfer(50, mag_plate.cols('3'), trash_loc, new_tip='never')
    m300.drop_tip()

m300.delay(minutes=5)
mag_deck.disengage()

m300.pick_up_tip()
m300.transfer(42, trisHCl, mag_plate.cols('3'), new_tip='never')
m300.mix(10, 40, mag_plate.cols('3'))
mag_deck.engage()
m300.delay(minutes=2)
m300.transfer(40, mag_plate.cols('3'), cold_strips.cols('6'), new_tip='never')
mag_deck.disengage()

"""
MBC Adapter Incorporation
"""
m300.mix(5, 40, cold_strips.cols('6'))

"""
Ligation Step 2
"""
m300.transfer(50, cold_strips.cols('6'), cold_strips.cols('7'), new_tip='never')
m300.mix(5, 50, cold_strips.cols('7'))
heat_block.wait_for_temp()
m300.transfer(50, cold_strips.cols('7'), heat_strips.cols('4'), new_tip='never')
m300.delay(minutes=5)
m300.transfer(50, heat_strips.cols('4'), cold_strips.cols('8'), new_tip='never')
m300.delay(minutes=4)
m300.drop_tip()

"""
Cleanup after Ligation Step 2
"""
m300.pick_up_tip()
m300.mix(5, 40, ligation_beads)
m300.transfer(50, ligation_beads, mag_plate.cols('4'), new_tip='never')
mag_deck.engage()
m300.delay(minutes=1)
m300.transfer(110, mag_plate.cols('4'), trash_loc, new_tip='never')
m300.drop_tip()
mag_deck.disengage()

m300.pick_up_tip()
col_edge = (mag_plate.cols('4')[0],
            mag_plate.cols('4')[0].from_center(r=1, h=0.5, theta=0))
m300.transfer(50, cleanup_buffer1, col_edge, new_tip='never')
m300.mix(10, 50, mag_plate.cols('4'))
m300.drop_tip()

m300.pick_up_tip()
m300.transfer(50, cold_strips.cols('8'), mag_plate.cols('4'), new_tip='never')
m300.mix(10, 50, mag_plate.cols('4'))
m300.delay(minutes=5)
m300.mix(10, 50, mag_plate.cols('4'))
m300.delay(minutes=5)
mag_deck.engage()
m300.delay(minutes=1)
m300.transfer(110, mag_plate.cols('4'), trash_loc, new_tip='never')
m300.drop_tip()
mag_deck.disengage()

m300.pick_up_tip()
m300.transfer(200, cleanup_buffer1, col_edge, new_tip='never')
m300.mix(10, 50, mag_plate.cols('4'))
mag_deck.engage()
m300.delay(minutes=1)
m300.transfer(210, mag_plate.cols('4'), trash_loc, new_tip='never')
m300.drop_tip()
mag_deck.disengage()

m300.pick_up_tip()
m300.transfer(200, cleanup_buffer2, col_edge, new_tip='never')
m300.mix(10, 50, mag_plate.cols('4'))
mag_deck.engage()
m300.delay(minutes=1)
m300.transfer(210, mag_plate.cols('4'), trash_loc, new_tip='never')
m300.drop_tip()
mag_deck.disengage()

m300.pick_up_tip()
m300.transfer(200, water, col_edge, new_tip='never')
m300.mix(10, 50, mag_plate.cols('4'))
mag_deck.engage()
m300.delay(minutes=1)
m300.transfer(210, mag_plate.cols('4'), trash_loc, new_tip='never')
m300.drop_tip()

m300.transfer(50, mag_plate.cols('4'), trash_loc)
mag_deck.disengage()

m300.pick_up_tip()
m300.transfer(32, NaOH, col_edge, new_tip='never')
m300.transfer(32, mag_plate.cols('4'), cold_strips.cols('9'), new_tip='never')
m300.drop_tip()
