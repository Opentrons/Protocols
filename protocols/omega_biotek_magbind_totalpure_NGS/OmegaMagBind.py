from opentrons import labware, instruments, modules

# from otcustomizers import StringSelection

from opentrons import robot


mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
output_plate = labware.load('96-PCR-tall', '2')


 def run_custom_protocol(
        pipette_type: StringSelection(
            'p10_Single', 'p50_Single', 'p300_Single', 'p1000_Single',
            'p10_Multi', 'p50_Multi', 'p300_Multi'
            )='p300_Multi',
        pipette_mount: StringSelection('left', 'right')='left',
        sample_number: int=16,
        PCR_volume: float=20,
        bead_ratio: float=1.8,
        elution_buffer_volume: float=200):

incubation_time = 300
settling_time = 50
drying_time = 5
total_tips = sample_number*8
tiprack_num = total_tips//96 + (1 if total_tips % 96 > 0 else 0)
slots = ['3', '5', '6', '8', '9', '10', '11'][:tiprack_num]


if pipette_type == 'p1000_Single':
    tipracks = [labware.load('tiprack-1000ul', slot) for slot in slots]
    pipette = instruments.P1000_Single(
        mount=pipette_axis,
        tip_racks=tipracks)

elif pipette_type == 'p300_Single':
    tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
    pipette = instruments.P300_Single(
        mount=pipette_axis,
        tip_racks=tipracks)

elif pipette_type == 'p50_Single':
    tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
    pipette = instruments.P50_Single(
        mount=pipette_axis,
        tip_racks=tipracks)

elif pipette_type == 'p10_Single':
    tipracks = [labware.load('tiprack-10ul', slot) for slot in slots]
    pipette = instruments.P10_Single(
        mount=pipette_axis,
        tip_racks=tipracks)

elif pipette_type == 'p10_Multi':
    tipracks = [labware.load('tiprack-10ul', slot) for slot in slots]
    pipette = instruments.P10_Multi(
        mount=pipette_axis,
        tip_racks=tipracks)

elif pipette_type == 'p50_Multi':
    tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
    pipette = instruments.P50_Multi(
        mount=pipette_axis,
        tip_racks=tipracks)

elif pipette_type == 'p300_Multi':
    tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
    pipette = instruments.P300_Multi(
        mount=pipette_axis,
        tip_racks=tipracks)

mode = pipette_type.split('_')[1]
if mode == 'Single':
    if sample_number <= 5:
        reagent_container = labware.load('tube-rack-2ml', '7')
        liquid_waste = labware.load('trough-12row', '5').wells('A12')

    else:
        reagent_container = labware.load('trough-12row', '7')
        liquid_waste = reagent_container.wells('A12')
    samples = [well for well in mag_plate.wells()[:sample_number]]
    samples_top = [well.top() for sample in samples]
    output = [well for well in output_plate.wells()[:sample_number]]


else:
    reagent_container = labware.load('trough-12row', '7')
    liquid_waste = reagent_container.wells('A12')
    col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
    samples = [col for col in mag_plate.cols()[:col_num]]
    samples_top = [well.top() for well in mag_plate.rows(0)[:col_num]]
    output = [col for col in output_plate.cols()[:col_num]]


# Define reagents and liquid waste
beads = reagent_container.wells(0)
ethanol = reagent_container.wells(1)
elution_buffer = reagent_container.wells(2)


# Define bead and mix volume
bead_volume = PCR_volume*bead_ratio
if bead_volume/2 > pipette.max_volume:
    mix_vol = 280
else:
    mix_vol = 280
total_vol = bead_volume + PCR_volume + 15
mix_voltarget = PCR_volume + 10


# Disengage MagDeck
mag_deck.disengage()

# Mix Speed
pipette.set_flow_rate(aspirate=180, dispense=180)

# Mix beads and PCR samples
for target in samples:
    pipette.set_flow_rate(aspirate=180, dispense=180)
    pipette.pick_up_tip()
    #Slow down head speed 0.5X for bead handling 
    pipette.mix(25, mix_vol, beads)
    max_speed_per_axis = {
    'x': (50), 'y': (50), 'z':(50) , 'a': (10), 'b': (10), 'c': (10)}
    robot.head_speed(
        combined_speed=max(max_speed_per_axis.values()),
        **max_speed_per_axis)

    pipette.set_flow_rate(aspirate=10, dispense=10)
    pipette.transfer(bead_volume, beads, target, air_gap=0, new_tip='never')
    pipette.set_flow_rate(aspirate=50, dispense=50)
    pipette.mix(40, mix_voltarget, target)
    pipette.blow_out()
    max_speed_per_axis = {
    'x': (600), 'y': (400), 'z':(100) , 'a': (100), 'b': (40), 'c': (40)}
    robot.head_speed(
        combined_speed=max(max_speed_per_axis.values()),
        **max_speed_per_axis)

    pipette.drop_tip()

#Return robot head speed to the defaults for all axes
    max_speed_per_axis = {
    'x': (600), 'y': (400), 'z':(100) , 'a': (100), 'b': (40), 'c': (40)}
    robot.head_speed(
        combined_speed=max(max_speed_per_axis.values()),
        **max_speed_per_axis)

# Incubate beads and PCR product at RT for 5 minutes
pipette.delay(seconds=incubation_time)

# Engage MagDeck and Magnetize
mag_deck.engage()
pipette.delay(seconds=settling_time)


# Remove supernatant from magnetic beads
pipette.set_flow_rate(aspirate=25, dispense=120)
for target in samples:
    pipette.transfer(total_vol, target.bottom(0.7), liquid_waste.top(), blow_out=True)


# Wash beads twice with 70% ethanol

air_vol = pipette.max_volume*0.1

for cycle in range(2):
    pipette.pick_up_tip()
    for target in samples_top:
        pipette.transfer(185, ethanol, target, air_gap=air_vol, new_tip='never')
    pipette.delay(seconds=17)
    for target in samples:
        if not pipette.tip_attached:
            pipette.pick_up_tip()
        pipette.transfer(195, target.bottom(0.7), liquid_waste.top(), air_gap=air_vol,
                         new_tip='never')
        pipette.drop_tip()



# Dry at RT
pipette.delay(minutes=drying_time)
# Disengage MagDeck

mag_deck.disengage()

# Mix beads with elution buffer

if elution_buffer_volume/2 > pipette.max_volume:
    mix_vol = pipette.max_volume
else:
    mix_vol = elution_buffer_volume/2
for target in samples:
    pipette.pick_up_tip()
    pipette.transfer(
        elution_buffer_volume, elution_buffer, target, new_tip='never')
    pipette.mix(45, mix_vol, target)
    pipette.drop_tip()

# Incubate at RT for 3 minutes
pipette.delay(minutes=3)

# Engage MagDeck for 1 minute and remain engaged for DNA elution

mag_deck.engage()
pipette.delay(seconds=settling_time)
# Transfer clean PCR product to a new well
for target, dest in zip(samples, output):
    pipette.transfer(elution_buffer_volume, target.bottom(1), dest.top(), blow_out=True)

# Disengage MagDeck
mag_deck.disengage()