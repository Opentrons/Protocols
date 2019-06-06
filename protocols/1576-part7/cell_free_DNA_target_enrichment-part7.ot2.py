from opentrons import labware, instruments, modules, robot

metadata = {
    'protocolName': 'Cell3 Target: Cell Free DNA Target Enrichment Part 7',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
plate = labware.load('biorad-hardshell-96-PCR', '1')
mag_module = modules.load('magdeck', '4')
mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
trough = labware.load('trough-12row', '5')
temp_module = modules.load('tempdeck', '7')
temp_plate = labware.load(
    'opentrons-aluminum-block-96-PCR-plate', '7', share=True)
tiprack_50 = labware.load('opentrons-tiprack-300ul', '2')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '3')

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])
p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
reaction_mix = plate.wells('A1')
rt_wash_buffer = plate.wells('A2', length=3)
nuclease_free_water = plate.wells('A3')
wash_buffer = temp_plate.wells('A1')
stringent_wash_buffer = temp_plate.wells('B1', length=2)

temp_module.set_temperature(65)
temp_module.wait_for_temp()

# transfer hybridization reaction mix to dynabeads
sample_dest = mag_plate.wells('A1')
p50.pick_up_tip()
p50.transfer(17, reaction_mix, sample_dest, new_tip='never')
p50.mix(10, 15, sample_dest)
p50.blow_out(sample_dest)
p50.drop_tip()

robot.pause('Transfer the PCR tube to the thermocycler set to 65°C and \
incubate for 45 minutes. Vortex the tube for 3 seconds every 12 minutes during\
 the incubation. Place the tube back on the Magnetic Module and resume the \
 protocol.')

# add and mix wash_buffer
p300.pick_up_tip()
p300.transfer(100, wash_buffer, sample_dest, new_tip='never')
p300.mix(10, 80, sample_dest)
p300.blow_out(sample_dest)
p300.drop_tip()

mag_module.engage()
p300.delay(seconds=15)

# remove supernatant
p300.transfer(130, sample_dest, p300.trash_container)

mag_module.disengage()

for wash_index in range(2):
    # add and mix Stringent Wash Buffer
    p300.pick_up_tip()
    p300.transfer(
        200, stringent_wash_buffer[wash_index], sample_dest, new_tip='never')
    p300.mix(10, 150, sample_dest)
    p300.blow_out(sample_dest)
    p300.drop_tip()

    robot.pause('Transfer the PCR tube to the thermocycler set to 65°C and \
    incubate for 5 minutes. Place the tube back on the Magnetic Module before \
    resuming the protocol.')

    mag_module.engage()
    p300.delay(seconds=15)

    # remove supernatant
    p300.transfer(300, sample_dest, p300.trash_container)

    mag_module.disengage()

for rt_wash_index in range(3):
    # add room temperature wash buffer
    p300.transfer(200, rt_wash_buffer[rt_wash_index], sample_dest)

    robot.pause('Vortex thoroughly for '+['2', '1', '0.5'][rt_wash_index]
                + ' minutes before returning to the Magnetic Module.')

    mag_module.engage()
    if rt_wash_index < 2:
        p300.delay(seconds=30)
    else:
        p300.delay(minutes=2)

    # remove supernatant
    p300.transfer(230, sample_dest, p300.trash_container)

    mag_module.disengage()

# add and mix nuclease-free water
p50.pick_up_tip()
p50.transfer(24, nuclease_free_water, sample_dest, new_tip='never')
p50.mix(15, 15, sample_dest)
p50.blow_out(sample_dest)
p50.drop_tip()
