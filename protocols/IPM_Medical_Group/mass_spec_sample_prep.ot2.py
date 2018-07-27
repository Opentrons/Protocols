from opentrons import labware, instruments, robot

# customization 
sample_number = 48  # must be between 10 and 48
incubation_time = 1 # in minutes
centrifuge_time = 1 # in minutes

labware.create('custom-tuberack-7ml',
				grid=(4, 6),
				spacing=(20, 20),
				diameter=10,
				depth=72)

labware.create('autosampler-rack-1ml',
				grid=(6, 10),
				spacing=(12.3, 11.5),
				diameter=8.53,
				depth=72)

# labware setup
MCT_rack1 = labware.load('tube-rack-2ml', 1)
MCT_rack2 = labware.load('tube-rack-2ml', 2)
autosampler_rack1 = labware.load('autosampler-rack-1ml', 3)
sample_rack1 = labware.load('custom-tuberack-7ml', 4)
sample_rack2 = labware.load('custom-tuberack-7ml', 5)
autosampler_rack2 = labware.load('autosampler-rack-1ml', 6)
tiprack1_p300 = labware.load('tiprack-200ul', 7)
tiprack1_p50 = labware.load('tiprack-200ul', 8)
trough = labware.load('trough-12row', 9)
tiprack2_p300 = labware.load('tiprack-200ul', 10)
tiprack2_p50 = labware.load('tiprack-200ul', 11)

# variable and reagents setup
buffer_loc = trough.wells('A1')
enzyme_loc = trough.wells('A2')
is_loc = trough.wells('A3')
diluent_loc = trough.wells('A4')

sample_loc = sample_rack1.wells() + sample_rack2.wells()
MCT_tube_loc = MCT_rack1.wells() + MCT_rack2.wells()
autosampler_loc = autosampler_rack1.wells() + autosampler_rack2.wells()

sample_loc = sample_loc[0:sample_number]
MCT_tube_loc = MCT_tube_loc[0:sample_number]
autosampler_loc = autosampler_loc[0:sample_number]

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack1_p50, tiprack2_p50])

p300 = instruments.P300_Single(
    tip_racks = [tiprack1_p300, tiprack2_p300],
    mount = 'right')


p50.pick_up_tip()
p50.mix(3, 50, buffer_loc)
p50.transfer(30, buffer_loc, MCT_tube_loc)

p50.pick_up_tip()
p50.mix(3, 50, enzyme_loc)
p50.transfer(20, enzyme_loc, MCT_tube_loc)

p50.pick_up_tip()
p50.mix(3, 50, is_loc)
p50.transfer(50, is_loc, MCT_tube_loc)

p300.transfer(100, sample_loc, MCT_tube_loc, new_tip='always', mix_before=(3, 300))

p300.delay(minutes=incubation_time)

p300.pick_up_tip()
p300.mix(3, 300, diluent_loc)
p300.transfer(350, diluent_loc, MCT_tube_loc)

p300.delay(minutes=centrifuge_time)

for well_a, well_m in zip(autosampler_loc, MCT_tube_loc):
    p300.transfer(400, well_m, well_a.bottom(14), new_tip='always')
