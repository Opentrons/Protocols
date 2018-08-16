from opentrons import labware, instruments, robot

# customization
sample_number = 48   # must be between 10 and 48


if 'custom-tuberack-7ml' not in labware.list():
    labware.create('custom-tuberack-7ml',
                   grid=(6, 4),
                   spacing=(19.1, 17.8),
                   diameter=10,
                   depth=72)

if 'autosampler-rack-1ml' not in labware.list():
    labware.create('autosampler-rack-1ml',
                   grid=(6, 4),
                   spacing=(19.1, 17.8),
                   diameter=7,
                   depth=40)

# labware setup
sample_rack1 = labware.load('custom-tuberack-7ml', '1')
sample_rack2 = labware.load('custom-tuberack-7ml', '4')
MCT_rack1 = labware.load('tube-rack-2ml', '2')
MCT_rack2 = labware.load('tube-rack-2ml', '5')
autosampler_rack1 = labware.load('autosampler-rack-1ml', '3')
autosampler_rack2 = labware.load('autosampler-rack-1ml', '6')
tiprack1_p300 = labware.load('tiprack-200ul', '7')
tiprack1_p50 = labware.load('tiprack-200ul', '8')
rack_15_50 = labware.load('tube-rack-15_50ml', '9')
tiprack2_p300 = labware.load('tiprack-200ul', '10')
tiprack2_p50 = labware.load('tiprack-200ul', '11')

# variable and reagents setup
buffer_loc = rack_15_50.wells('A1')
enzyme_loc = rack_15_50.wells('A2')
is_loc = rack_15_50.wells('B1')
diluent_loc = rack_15_50.wells('A3')

init_sample_loc = sample_rack1.wells() + sample_rack2.wells()

sample_loc = []
for well in init_sample_loc:
    sample_loc.append(well.bottom(well.properties['height']//2))

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
    tip_racks=[tiprack1_p300, tiprack2_p300],
    mount='right')

# Transfer buffer
p50.pick_up_tip()
p50.mix(3, 50, buffer_loc)
p50.transfer(30, buffer_loc, MCT_tube_loc, new_tip='never', blow_out=True)
p50.drop_tip()

# Transfer enzyme
p50.pick_up_tip()
p50.mix(3, 50, enzyme_loc)
p50.transfer(20, enzyme_loc, MCT_tube_loc, new_tip='never', blow_out=True)
p50.drop_tip()
# Transfer internal standards
p50.pick_up_tip()
p50.mix(3, 50, is_loc)
p50.transfer(50, is_loc, MCT_tube_loc, new_tip='never', blow_out=True)
p50.drop_tip()
# Trasnfer sample to MCT tubes
p300.transfer(100, sample_loc, MCT_tube_loc, new_tip='always',
              mix_before=(3, 300), blow_out=True)

robot.pause()

# Transfer diluent
p300.pick_up_tip()
p300.mix(3, 300, diluent_loc)
p300.transfer(350, diluent_loc, MCT_tube_loc, new_tip='never', blow_out=True)
p300.drop_tip()

robot.pause()

# Transfer supernatent
for well_a, well_m in zip(autosampler_loc, MCT_tube_loc):
    p300.transfer(300, well_m, well_a.bottom(14), new_tip='always', blow_out=True)
