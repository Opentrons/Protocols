from opentrons import labware, instruments, robot

# labware setup
plate = labware.load('96-flat', '4')
trough1 = labware.load('trough-12row', '5')
trough2 = labware.load('trough-12row', '6')
tiprack = labware.load('tiprack-200ul', '1')

# reagent setup
osmium = plate.cols('1')
uranyl_acetate = plate.cols('4')
fix_rince_1 = trough1.wells('A1')
fix_rince_2 = trough1.wells('A2')
os_rince_1 = trough1.wells('A3')
os_rince_2 = trough1.wells('A4')
etoh_30 = trough1.wells('A5')
etoh_50 = trough1.wells('A6')
etoh_70 = trough1.wells('A7')
etoh_90 = trough1.wells('A8')
etoh_100_1 = trough1.wells('A9')
etoh_100_2 = trough1.wells('A10')
aceton_100_1 = trough1.wells('A11')
aceton_100_2 = trough1.wells('A12')
durcupan_25 = trough2.wells('A1')
durcupan_50 = trough2.wells('A2')
durcupan_75 = trough2.wells('A3')
durcupan_100_1 = trough2.wells('A4')
durcupan_100_2 = trough2.wells('A5')
durcupan_100_3 = trough2.wells('A6')
durcupan_100_4 = trough2.wells('A7')

# instrument setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])

target = (200, 90, 180)
m300.move_to((robot.deck, target))
robot.pause()

m300.set_flow_rate(aspirate=120, dispense=130)
m300.pick_up_tip()

m300.mix(60, 100, fix_rince_1)

m300.mix(60, 100, fix_rince_2)

m300.mix(600, 100, osmium)

m300.mix(60, 100, os_rince_1)

m300.mix(60, 100, os_rince_2)

m300.mix(60, 100, etoh_30)

m300.mix(60, 100, etoh_50)

m300.mix(600, 100, uranyl_acetate)

m300.mix(60, 100, etoh_70)

m300.mix(60, 100, etoh_90)

m300.mix(240, 100, etoh_100_1)

m300.mix(240, 100, etoh_100_2)

m300.mix(240, 100, aceton_100_1)

m300.mix(240, 100, aceton_100_2)

m300.mix(600, 100, durcupan_25)

m300.mix(600, 100, durcupan_50)

m300.mix(600, 100, durcupan_75)

m300.mix(600, 100, durcupan_100_1)

m300.mix(600, 100, durcupan_100_2)

m300.mix(600, 100, durcupan_100_3)

m300.aspirate(100, durcupan_100_4)

m300.move_to((robot.deck, target))
