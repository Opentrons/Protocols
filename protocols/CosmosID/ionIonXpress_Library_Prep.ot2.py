from opentrons import labware, instruments, robot

sample_num = 1

reagent_rack = labware.load('tube-rack-2ml', '4')
water = labware.load('tube-rack-15_50ml', '1').wells('A1')
dilution_plate = labware.load('PCR-strip-tall', '2')
plate = labware.load('96-PCR-flat', '3')

qPCR_mix = reagent_rack.wells('A1')
q_assay = reagent_rack.wells('B1')
masterMix = reagent_rack.wells('C1')
control_lib = reagent_rack.wells('D1')
sample_lib = reagent_rack.wells('A2', length=sample_num)

tiprack_10 = labware.load('tiprack-10ul', '6')
tiprack_200 = labware.load('tiprack-200ul', '7')

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack_200])

masterMix_num = sample_num*3 + 18

"""
Prepare Control Libary
"""
# define control library dilution locations
control_dil_loc = dilution_plate.cols('1')[0:5]

# add water to PCR strip wells A1-E1 for control dilutions
p50.transfer(45, water, control_dil_loc)

# transfer control library to PCR strip wells A1
p10.pick_up_tip()
p10.transfer(5, control_lib, control_dil_loc[0], mix_after=(10, 10),
			 new_tip='never')

# dilute control library serially
p10.transfer(5, control_dil_loc[0:4], control_dil_loc[1:5],
			 mix_after=(10, 10), new_tip='never')
p10.drop_tip()


"""
Prepare Sample Library
"""
# define sample library dilution locations
# where every sample dilution series occupies a different column
sample_dil_loc = [col[0:3]
                  for col in dilution_plate.cols(1, length=sample_num)
                 ]

# add water to PCR strip wells A-C for each sample library
p50.pick_up_tip()
for each_dil_series in sample_dil_loc:
    p50.transfer([19, 99, 45], water, each_dil_series, new_tip='never')
p50.drop_tip()

# Transfer sample library to microcentrifuge tube 1
for sample_source, each_dil_series in zip(sample_lib, sample_dil_loc):
    p10.pick_up_tip()

    # transfer sample library to well 1
    p10.transfer(1, sample_source, each_dil_series[0], mix_after=(10, 10),
                 new_tip='never')

    # serial diltion
    p10.transfer((1,5), each_dil_series[0:2], each_dil_series[1:3],
                 mix_after=(10, 10), new_tip='never')
    p10.drop_tip()


# robot.pause()

"""
Prepare masterMix
"""

p50.transfer(masterMix_num*10, qPCR_mix, masterMix)

p50.transfer(masterMix_num*1, q_assay, masterMix)

p50.transfer(masterMix_num*4, water, masterMix)

"""
Define locations on the PCR plate
"""

# control library: Column 1-3, wells A1-E3
control_lib_loc = [well for row in plate.rows[0:5] for well in row[0:3]]

# non-template control: Column 4, wells A4-C4
ntc_loc = [well for well in plate.cols[3][0:3]]

# sample library: Column 5 onward, wells A-C
sample_lib_loc = [well
                  for row in plate.rows[0:3]
                  for well in row[4:4+sample_num*2]
                  ]

"""
Transfer masterMix and appropriate reagents to all locations defined above
"""

# transfer masterMix for 3 replicates each reaction
p50.transfer(15, masterMix, control_lib_loc+ntc_loc+sample_lib_loc)


# transfer 5 uL control library dilutions to control_lib_loc
p10.transfer(5, control_dil_loc, control_lib_loc)

# transfer 5 uL water to non-template control 
p10.transfer(5, water, ntc_loc)

# re-define sample library by grouping each column
sample_lib_loc = [col[0:3] for col in plate.cols[4:4+sample_num*2]]

# transfer 5 uL sample library dilutions to sample_lib_loc
for index, sample in enumerate(sample_dil_loc):
    p10.pick_up_tip()
    for sample_dest in sample_lib_loc[index*2:index*2+2]:
        p10.transfer(5, sample, sample_dest, new_tip='never')
    p10.drop_tip()
