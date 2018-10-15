from opentrons import labware, instruments, modules, robot

# labware setup
block = labware.load('opentrons-aluminum-block-96-PCR-plate', '4')
rt_plate = labware.load('96-flat', '5')
temp_module = modules.load('tempdeck', '6')
temp_plate = labware.load('96-flat', '6', share=True)
mag_module = modules.load('magdeck', '7')
mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)
tuberack = labware.load('opentrons-tuberack-15_50ml', '8')

# reagent setup
DNA = block.wells('A1')
repair_1_mm = block.wells('B1')
repair_2_mm = block.wells('C1')
reagent_g1 = block.wells('D1')
reagent_g2 = block.wells('E1')
ligation_mm = block.wells('F1')
aline_beads = rt_plate.wells('A1')
PEG_NaCl = rt_plate.wells('B1')
EDTA_TE = rt_plate.wells('C1')
EtOH = tuberack.wells('A1')

tiprack_10 = labware.load('tiprack-10ul', '10')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '11')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack_300])

"""
Repair I
"""
# define location
repair_I_mix_loc = rt_plate.wells('A3')
repair_I_temp_loc = temp_plate.wells('A1')
repair_I_mag_loc = mag_plate.wells('A1')

# set Temperature Module to 37°C
temp_module.set_temperature(37)

p50.transfer(40, DNA, repair_I_mix_loc)
p50.transfer(20, repair_1_mm, repair_I_mix_loc)
robot.pause("Flick the plate to mix.")

temp_module.wait_for_temp()
p50.transfer(60, repair_I_mix_loc, repair_I_temp_loc)
p50.delay(minutes=15)

p50.transfer(60, repair_I_temp_loc, repair_I_mag_loc)

"""
Clean Up I
"""
p50.transfer(30, aline_beads, repair_I_mag_loc)
robot.pause("Flick the plate to mix. Incubate for 20 minutes with shaking \
off robot. Put the plate back on the Magnetic Module.")

mag_module.engage()
p50.delay(minutes=5)

"""
set aspirate and dispense speed
"""
p50.transfer(95, repair_I_mag_loc.bottom(1), p50.trash_container.top())
p50.transfer(200, EtOH, repair_I_mag_loc)
p50.delay(seconds=30)
p50.transfer(200, repair_I_mag_loc.bottom(1), p50.trash_container.top())
p50.transfer(200, EtOH, repair_I_mag_loc)
p50.delay(seconds=30)
p50.transfer(200, repair_I_mag_loc.bottom(1), p50.trash_container.top())

p10.transfer(10, repair_I_mag_loc, p10.trash_container.top())

"""
Repair II
"""
# define location
repair_II_mix_loc = rt_plate.wells('B3')
repair_II_temp_loc = temp_plate.wells('B1')
repair_II_mag_loc = mag_plate.wells('B1')

mag_module.disengage()
p50.transfer(50, repair_2_mm, repair_I_mag_loc)
robot.pause("Flick the plate to mix.")
p50.transfer(55, repair_I_mag_loc, repair_II_temp_loc)

temp_module.set_temperature(35)
temp_module.wait_for_temp()
p50.delay(minutes=65)
temp_module.set_temperature(25)
temp_module.wait_for_temp()
p50.delay(minutes=5)

p50.transfer(55, repair_II_temp_loc, repair_II_mix_loc)
p50.delay(minutes=5)
p10.transfer(1, reagent_g1, repair_II_mix_loc)
p10.transfer(2, reagent_g2, repair_II_mix_loc)
robot.pause("Flick the plate to mix. Incubate for 20 minutes in RT.")

"""
Clean Up II
"""
p50.transfer(57, repair_II_mix_loc, repair_II_mag_loc)
p50.transfer(31, PEG_NaCl, repair_II_mag_loc)
robot.pause("Flick the plate to mix. Incubate for 20 minutes with shaking. \
Place the plate back on the Magnetic Module.")

mag_module.engage()
p50.delay(minutes=5)

"""
set aspirate and dispense speed
"""
p50.transfer(57, repair_II_mag_loc.bottom(1), p50.trash_container.top())
p50.transfer(200, EtOH, repair_II_mag_loc)
p50.delay(seconds=30)
p50.transfer(200, repair_II_mag_loc.bottom(1), p50.trash_container.top())
p50.transfer(200, EtOH, repair_II_mag_loc)
p50.delay(seconds=30)
p50.transfer(200, repair_II_mag_loc.bottom(1), p50.trash_container.top())
p10.transfer(10, repair_II_mag_loc.bottom(1), p10.trash_container.top())

"""
Ligation
"""
# define location
ligation_temp_loc = temp_plate.wells('C1')
ligation_mag_loc = mag_plate.wells('C1')

mag_module.disengage()
p50.transfer(50, ligation_mm, repair_II_mag_loc)
robot.pause("Flick the plate to mix.")
p50.transfer(55, repair_II_mag_loc, ligation_temp_loc)

temp_module.set_temperature(25)
temp_module.wait_for_temp()
p50.delay(minutes=35)

"""
Clean Up III
"""
p50.transfer(55, ligation_temp_loc, ligation_mag_loc)
p50.transfer(18, PEG_NaCl, ligation_mag_loc)
robot.pause("Flick the plate to mix. Incubate for 20 minutes with shaking. \
Place the plate back on the Magnetic Module.")

mag_module.engage()
p50.delay(minutes=5)

"""
set aspirate and dispense speed
"""
p50.transfer(80, ligation_mag_loc.bottom(1), p50.trash_container.top())
p50.transfer(200, EtOH, ligation_mag_loc)
p50.delay(seconds=30)
p50.transfer(200, ligation_mag_loc.bottom(1), p50.trash_container.top())
p50.transfer(200, EtOH, ligation_mag_loc)
p50.delay(seconds=30)
p50.transfer(200, ligation_mag_loc.bottom(1), p50.trash_container.top())
p10.transfer(10, ligation_mag_loc.bottom(1), p10.trash_container.top())

"""
Elute
"""
# define finished library location
finished_lib = block.wells('D4')

mag_module.disengage()

p50.transfer(30, EDTA_TE, ligation_mag_loc)
robot.pause("Flick the plate to mix. Incubate for 2 minutes with shaking. \
Place the plate back on the Magnetic Module.")

mag_module.engage()
p50.delay(minutes=2)

p50.transfer(30, ligation_mag_loc, finished_lib)
