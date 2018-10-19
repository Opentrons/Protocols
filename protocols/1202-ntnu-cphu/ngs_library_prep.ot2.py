from opentrons import labware, instruments, modules, robot

# labware setup
cold_block = labware.load('opentrons-aluminum-block-2ml-eppendorf', '1')
sample_plate = labware.load('96-flat', '2')
elution_plate = labware.load('96-flat', '3')
temp_deck = modules.load('tempdeck', '4')
temp_plate = labware.load('96-flat', '4', share=True)
adapter_plate = labware.load('96-flat', '5')
trough = labware.load('trough-12row', '6')
mag_deck = modules.load('magdeck', '7')
mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

tipracks_10 = [labware.load('tiprack-10ul', slot)
               for slot in ['8']]

tipracks_300 = [labware.load('tiprack-200ul', slot)
                for slot in ['9', '10', '11']]

# pipette setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tipracks_10)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_300)

# reagent setup
ER_mastermix = cold_block.wells('A1')
BGI_adapter = cold_block.wells('B1')
Lig_mastermix = cold_block.wells('C1')
Fill_mastermix = cold_block.wells('D1')
SPRI_beads = trough.wells('A1')
ethanol = trough.wells('A2')
elution_buffer = trough.wells('A3')
liquid_trash = trough.wells('A12')

sample_vol = 300

"""
Blund end repair
"""
robot.comment("Blund-end Repair begins. Make sure your sample plate is on \
the Tempdeck.")

p10.transfer(8, ER_mastermix, [well.top() for well in temp_plate.wells()])

temp_deck.set_temperature(20)
temp_deck.wait_for_temp()
m300.delay(minutes=40)
temp_deck.set_temperature(65)
temp_deck.wait_for_temp()
m300.delay(minutes=40)

"""
Adapter Addition
"""
robot.comment("End of Blund-end Repair. Adapter Addition beings.")

p10.distribute(2, BGI_adapter, adapter_plate.wells())

temp_deck.set_temperature(20)

for source, dest in zip(temp_plate.cols(), adapter_plate.cols()):
    m300.transfer(40, source, dest, mix_after=(3, 40))

"""
Ligase
"""
robot.pause("End of Adapter Addition. Ligase beings. Replace the 96-well plate \
on the tempdeck. Resume when finished.")

p10.transfer(10, Lig_mastermix, [well.top() for well in adapter_plate.wells()])

m300.transfer(50, adapter_plate.cols(), temp_plate.cols(), new_tip='always')

m300.delay(minutes=30)
temp_deck.set_temperature(65)
temp_deck.wait_for_temp()
m300.delay(minutes=15)
temp_deck.set_temperature(20)

"""
Fill-in
"""
robot.comment("End of Ligase. Fill-in beings.")

p10.transfer(10, Fill_mastermix, [well.top() for well in temp_plate.wells()])

temp_deck.set_temperature(65)
temp_deck.wait_for_temp()
m300.delay(minutes=20)
temp_deck.set_temperature(80)
temp_deck.wait_for_temp()
m300.delay(minutes=20)

"""
Purification
"""
robot.comment("End of Fill-in. Purification beings.")

m300.transfer(60, temp_plate.cols(), mag_plate.cols(), new_tip='always')

robot.pause("The 300 uL tips have run out. Please replace tipracks. Resume \
when the tips are replenished.")
m300.reset_tip_tracking()

for index, dest in enumerate(mag_plate.cols()):
    m300.pick_up_tip()
    if index == 0:
        tip_loc = m300.current_tip()
    m300.transfer(
        108, SPRI_beads, dest, mix_after=(5, 108), trash=False)

m300.delay(minutes=5)

mag_deck.engage()
m300.delay(minutes=2)

m300.start_at_tip(tip_loc)
m300.transfer(170, mag_plate.cols(), liquid_trash, new_tip='always')

m300.pick_up_tip()
tip_loc = m300.current_tip()
for col in mag_plate.cols():
    m300.transfer(200, ethanol, col.top(), new_tip='never')
m300.return_tip()

m300.delay(minutes=3)

m300.start_at_tip(tip_loc)
m300.transfer(200, mag_plate.cols(), liquid_trash, new_tip='always')

mag_deck.disengage()

m300.pick_up_tip()
tip_loc = m300.current_tip()
for col in mag_plate.cols():
    m300.transfer(50, elution_buffer, col.top(), new_tip='never')
m300.return_tip()

m300.delay(minutes=10)

mag_deck.engage()
m300.delay(minutes=2)

m300.start_at_tip(tip_loc)
m300.transfer(45, mag_plate.cols(), elution_plate.cols(), new_tip='always')
