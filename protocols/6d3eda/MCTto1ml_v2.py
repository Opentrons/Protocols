from opentrons import labware, instruments, robot

# customization
sample_number = 8   # must be between 10 and 48
enzyme_disp_depth = 27 # enzyme dispense height from top of 2 mL tube (unit = mm)
is_disp_depth = 19 # internal standard dispense height from top of 2 mL tube (unit = mm)
sample_asp_depth = 60 # sample aspirate depth from top of 7 mL tube (unit = mm)
sample_disp_depth = 10 # sample dispense depth from top of MCT tube (unit = mm)
MCT_disp_depth = 10 # 1 mL MCT tube dispense depth from bottom of tuberack (unit = mm)
option = 'touch' # options are 'touch' (include touch tip) or 'speed' (increase speed of dispense)

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
rack_15_50 = labware.load('opentrons-tuberack-15_50ml', '9')
tiprack2_p300 = labware.load('tiprack-200ul', '10')
tiprack2_p50 = labware.load('tiprack-200ul', '11')

# variable and reagents setup
buffer_loc = rack_15_50.wells('A1')
enzyme_loc = rack_15_50.wells('A2')
is_loc = rack_15_50.wells('B1')
diluent_loc = rack_15_50.wells('A3')

init_sample_loc = sample_rack1.cols() + sample_rack2.cols()

# adding .top() .bottom() aspiration/dispense height specifications to wells
sample_loc = []
for col in init_sample_loc:
    for well in col:
        sample_loc.append(well.top(-sample_asp_depth))

MCT_tube_loc = MCT_rack1.wells() + MCT_rack2.wells()
buff_MCT_tube_loc = []
for well in MCT_tube_loc:
    buff_MCT_tube_loc.append(well.top(-10))
	
is_MCT_tube_loc = []
for well in MCT_tube_loc:
    is_MCT_tube_loc.append(well.top(-is_disp_depth))


enzyme_MCT_tube_loc = []
for well in MCT_tube_loc:
    enzyme_MCT_tube_loc.append(well.top(-enzyme_disp_depth))

init_autosampler_loc = autosampler_rack1.cols() + autosampler_rack2.cols()
autosampler_loc = []
for col in init_autosampler_loc:
	for well in col:
		autosampler_loc.append(well)


# adjusting lists based on sample number
sample_loc = sample_loc[0:sample_number]
buff_MCT_tube_loc = buff_MCT_tube_loc[0:sample_number]
is_MCT_tube_loc = is_MCT_tube_loc[0:sample_number]
enzyme_MCT_tube_loc = enzyme_MCT_tube_loc[0:sample_number]
MCT_tube_loc = MCT_tube_loc[0:sample_number]
autosampler_loc = autosampler_loc[0:sample_number]

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack1_p50, tiprack2_p50])

p300 = instruments.P300_Single(
    tip_racks=[tiprack1_p300, tiprack2_p300],
    mount='right')

def distrib_touch_tip(pip, mix_vol, disp_vol, start, dest, top_dest):
	remain = sample_number

	if pip == p300:
		pip_vol = 300
	elif pip == p50:
		pip_vol = 50

	pip.pick_up_tip()
	pip.mix(1, mix_vol, start)
	max_trans = pip_vol/disp_vol
	well_ind = 0
	while remain != 0:
		if max_trans < remain:
			aspirations = int(max_trans)
		else:
			aspirations = int(remain)
		pip.aspirate(aspirations*disp_vol, start)
		for _ in range (aspirations):
			if option == 'touch':
				pip.dispense(disp_vol, dest[well_ind])
				pip.touch_tip(top_dest[well_ind])  
			elif option == 'speed':
				if pip == p300:
					pip.set_flow_rate(aspirate = 150, dispense = 400)
				elif pip == p50:
					pip.set_flow_rate(aspirate = 25, dispense = 75)
				pip.dispense(disp_vol, dest[well_ind])
			well_ind = well_ind + 1
		pip.blow_out(dest[well_ind-1])

		remain = remain - aspirations

	pip.drop_tip()

	if option == 'speed':
		if pip == p300:
			pip.set_flow_rate(aspirate = 150, dispense = 300)
		elif pip == p50:
			pip.set_flow_rate(aspirate = 25, dispense = 50)



robot.pause()

# # Transfer supernatent
# # aspirate 27 mmfrom top, 1 cm from bottom to dispense
for well_a, well_m in zip(autosampler_loc, MCT_tube_loc):
    p300.pick_up_tip()
    p300.transfer(300, well_m.top(-27), well_a.bottom(14), new_tip='never', blow_out=True)
    p300.blow_out(well_a.top())
    p300.drop_tip()

for c in robot.commands():
	print(c)