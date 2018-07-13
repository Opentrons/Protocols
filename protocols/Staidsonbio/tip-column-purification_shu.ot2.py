from opentrons import instruments, containers, robot

# customization
num_plates = 2 # adjust based on number of 96 well plates with clone samples (1 - 4 plates)
pip_aspirate_speed = 200 # adjust based on appropriate aspirate speed
pip_dispense_speed = 7 # adjust based on appropriate dispense speed
phytip_vol = 1000 # adjust based on max volume of phytip
eq_vol = 1000 # adjust based on appropriate equilibration volume (20 - 1000 uL)
cap_vol = 500 # adjust based on appropriate capture volume (20 - 1000 uL)
wash1_vol = 1000 # adjust based on appropriate wash #1 volume (20 - 1000 uL)
wash2_vol = 1000 # adjust based on appropriate wash #2 volume (20 - 1000 uL)
elute_vol = 200 # adjust based on appropriate elution volume (20 - 200 uL)

# column A
sample1 = containers.load('96-PCR-flat', 'A1')
output1 = containers.load('96-PCR-flat', 'A2')
if phytip_vol > 300:
    tips1_1000 = containers.load('tiprack-1000ul','A3')
else:
    tips1_300 = containers.load('tiprack-200ul','A3')

# column B
sample2 = containers.load('96-PCR-flat', 'B1')
output2 = containers.load('96-PCR-flat', 'B2')
if phytip_vol > 300:
    tips2_1000 = containers.load('tiprack-1000ul','B3')
else:
    tips2_300 = containers.load('tiprack-200ul','B3')

# column C
sample3 = containers.load('96-PCR-flat', 'C1')
output3 = containers.load('96-PCR-flat', 'C2')
if phytip_vol > 300:
    tips3_1000 = containers.load('tiprack-1000ul','C3')
else:
    tips3_300 = containers.load('tiprack-200ul','C3')

# column D
sample4 = containers.load('96-PCR-flat', 'D1')
output4 = containers.load('96-PCR-flat', 'D2')
if phytip_vol > 300:
    tips4_1000 = containers.load('tiprack-1000ul','D3')
else:
    tips4_300 = containers.load('tiprack-200ul','D3')

# column E
trough2 = containers.load('trough-12row', 'E1')
trough = containers.load('trough-12row', 'E2')
trash = containers.load('trash-box','E3')

# instruments
if phytip_vol > 300:
    p1000 = instruments.Pipette(
        name = 'p1000',
        max_volume = 1000,
        min_volume = 100,
        channels = 1,
        tip_racks = [tips1_1000, tips2_1000, tips3_1000, tips4_1000],
        trash_container = trash,
        axis='a',
        aspirate_speed=pip_aspirate_speed,
        dispense_speed=pip_dispense_speed)
else:
    p300 = instruments.Pipette(
        name = 'p300',
        max_volume = 300,
        min_volume = 20,
        channels = 8,
        tip_racks = [tips1_300, tips2_300, tips3_300, tips4_300],
        trash_container = trash,
        axis='b', 
        aspirate_speed=pip_aspirate_speed,
        dispense_speed=pip_dispense_speed)

# variables and reagents setup
if phytip_vol > 300:
    pip = p1000
else:
    pip = p300

eq_buff = trough.wells('A1')
wash1 = trough.wells('A2')
wash2 = trough.wells('A3')
elute_buff = trough.wells('A4')

def cycle(sample_well, elute_well):
    pip.pick_up_tip()
    
    for i in range(2): # equilibration
        pip.aspirate(eq_vol, eq_buff.bottom(1)).delay(60)
        pip.dispense(eq_vol, eq_buff.bottom(1)).delay(60)
        
    for i in range(4): # capture
        pip.aspirate(cap_vol, sample_well.bottom(1)).delay(60)
        pip.dispense(cap_vol, sample_well.bottom(1)).delay(60)
        
    for i in range(2): # wash1
        pip.aspirate(wash1_vol, wash1.bottom(1)).delay(60)
        pip.dispense(wash1_vol, wash1.bottom(1)).delay(60)
        
    for i in range(2): # wash2
        pip.aspirate(wash2_vol, wash2.bottom(1)).delay(60)
        pip.dispense(wash2_vol, wash2.bottom(1)).delay(60)
        
    for i in range (5): # elution
        pip.aspirate(elute_vol, elute_buff.bottom(1)).delay(60)
        pip.dispense(elute_vol, elute_well.bottom(1)).delay(60)
        
    pip.drop_tip()

# make list of all sample and output plates
if pip == p1000:
    if num_plates == 1:
        all_samples = [sample1]
        all_outputs = [output1]
    elif num_plates == 2:
        all_samples = [sample1, sample2]
        all_outputs = [output1, output2]
    elif num_plates == 3:
        all_samples = [sample1, sample2, sample3]
        all_outputs = [output1, output2, output3]
    else:
        all_samples = [sample1, sample2, sample3, sample4]
        all_outputs = [output1, output2, output3, output4]
else:
    if num_plates == 1:
        all_samples = [sample1.cols('A')]
        all_outputs = [output1.cols('A')]
    elif num_plates == 2:
        all_samples = [sample1.cols('A'), sample2.cols('A')]
        all_outputs = [output1.cols('A'), output2.cols('A')]
    elif num_plates == 3:
        all_samples = [sample1.cols('A'), sample2.cols('A'), sample3.cols('A')]
        all_outputs = [output1.cols('A'), output2.cols('A'), output3.cols('A')]
    else:
        all_samples = [sample1.cols('A'), sample2.cols('A'), sample3.cols('A'), sample4.cols('A')]
        all_outputs = [output1.cols('A'), output2.cols('A'), output3.cols('A'), output4.cols('A')]

# sets volume in elution buffer well in trough
if pip == p300:
    elute_buff_vol = 20000/8
else:
    elute_buff_vol = 20000

# loop to cycle through wells in sample and output plates and to cycle through elution buffer locations in troughs
for sample_plate, output_plate in zip(all_samples, all_outputs):
    for sample_well, output_well in zip(sample_plate, output_plate):
        if elute_buff_vol - 5*elute_vol <= 0: # tracks volume in elution buffer well in trough
            try:
                elute_buff = next(elute_buff) # moves to next well in trough if volume too low
            except IndexError:
                elute_buff = trough2.wells('A1') # if out of wells in first trough, goes to second trough
            if pip == p300: # resets elution buffer volume in trough
                elute_buff_vol = 20000/8
            else:
                elute_buff_vol = 20000
        cycle(sample_well, output_well) 
        elute_buff_vol = elute_buff_vol - 5*elute_vol # adjusts buffer volume based on how much was used in cycle

print(robot.commands())

