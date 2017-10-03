from opentrons import containers, instruments
import json

# User input
user_input_raw = """
{"volumes_matrix":[
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[2.5,3,1.7,4.2,0,0,0,0],
[1.7,2.2,3.8,2.7,0,0,0,0],
[3.2,2.9,1.9,2.2,0,0,0,0],
[1.5,1.3,2.6,3.7,0,0,0,0],
[2.2,2.6,3.3,4.8,0,0,0,0],
[5.1,2.8,2.5,3.2,0,0,0,0]]}
"""
user_input = json.loads(user_input_raw)

if 'volumes_matrix' not in user_input:
    raise ValueError('Expected user input for volumes_matrix')

volumes_matrix = user_input['volumes_matrix']

trash = containers.load('point', 'A3')
sample_plate = containers.load('96-PCR-flat', 'C1')
water = containers.load('trough-12row', 'C3')
tip_rack = containers.load('tiprack-10ul', 'A1')
sample_rack = containers.load('tube-rack-2ml', 'C2')

p10 = instruments.Pipette(
    name="p10",
    axis="b",
    max_volume=10,
    min_volume=0.5,
    tip_racks=[tip_rack],
    trash_container=trash
)

water_source = water.wells('A1')
total_vol = 10
num_samples = len([num for row in volumes_matrix for num in row if num])
water_vol = [
    (total_vol - vol)
    for row in reversed(volumes_matrix)
    for vol in row if vol]

sample_vol = [vol for row in reversed(volumes_matrix) for vol in row if vol]

sample_src = [well.bottom() for well in sample_rack.wells()][:num_samples]

sample_dest = [
    well.bottom()
    for col in sample_plate.columns()
    for well in col][:num_samples]

# distribute H2O (10 - sample volume) to specified wells
p10.distribute(
    water_vol,
    water_source,
    sample_dest,
    new_tip='once'
)

# distribute sample volume to specified wells
p10.transfer(
    sample_vol,
    sample_src,
    sample_dest,
    new_tip='always',
    mix_after=(3, 10)
)
