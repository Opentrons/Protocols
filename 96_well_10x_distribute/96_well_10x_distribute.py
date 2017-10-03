from opentrons import containers, instruments

# Be careful not to calibrate the leftmost containers ('A' slots)
# too far to the left. The touch_tip action may make the head hit
# the leftmost limit switch.
#
# Also, you must calibrate carefully to the center well of each plate,
# or the repeated touch_tip action may eventually knock off the tips.

# from 1 to 12 destination plates are supported for full-deck models,
# or 1 to 7 for hood models
num_dest_plates = 10

transfer_volume = 10

# Set to False for OT Hood Model it has less slots for plates
full_deck_model = True

# Set up deck
dest_plates_locations = [
        'A1', 'B1', 'C1', 'D1',
        'A2', 'B2', 'D2', 'E2',
        'A3', 'B3', 'C3', 'D3', 'E3'
    ] if full_deck_model else [
        'A1', 'B1', 'C1', 'D1',
        'A2', 'B2', 'D2', 'E2'
    ]

dest_plates = []

for loc in dest_plates_locations[:num_dest_plates]:
    new_plate = containers.load('96-flat', loc)
    dest_plates.append(new_plate)

source_plate = containers.load('96-flat', 'C2')

trash = containers.load('point', 'E2')

tip_rack = containers.load('tiprack-200ul', 'E1')

p50multi = instruments.Pipette(
    axis='a',
    channels=8,
    max_volume=50,
    min_volume=5,
    tip_racks=[tip_rack],
    trash_container=trash,
)

# Distribute

row_count = len(dest_plates[0].rows())
for row_index in range(row_count):
    # List of WellSeries
    dest_wells = [plate.rows(row_index) for plate in dest_plates]
    p50multi.distribute(
        transfer_volume,
        source_plate.rows(row_index),
        dest_wells,
        touch_tip=True,
        disposal_vol=0
    )
