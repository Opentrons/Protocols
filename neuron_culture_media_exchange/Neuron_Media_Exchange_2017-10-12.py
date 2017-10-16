from opentrons import containers, instruments

"""
Media exchange
@Author opentrons
@date October 12th, 2017
@robot OT Hood, Pro, S
"""
pipette = instruments.Pipette(
    axis='a',
    name='1000single',
    max_volume=1000,
    min_volume=100,
    channels=1,
    aspirate_speed=200,
    dispense_speed=200)

"""
 DRG primary neuronal culture media exchange
- We are currently using 24 well plates.
I would like to fit do as many plates as possible each time
- maybe 6 plates, 3 tip boxes, 1 tube holder
with media tube/s and waste tube/s.
Also would like to set the flow rate low to avoid cells coming off the plate.
Since multichannels do not fit 24 wells plates,
we could use two p1000 pipettes.
Step 1: Remove 350uL from each well and deposit into waste
(we could do  2 wells with one tip per p1000 and then get new tips)
Step 2:  Add 400uL of media from 50mL conical with media to plates
(we could do  2 wells with one tip per p1000 and then get new tips -
if it is possible to set height slightly
above the media, we could use the same tips)
"""
# plate_type = '24-well-plate'

all_plates = [
    containers.load('24-well-plate', 'A2'),
    containers.load('24-well-plate', 'B1'),
    containers.load('24-well-plate', 'C2'),
    containers.load('24-well-plate', 'D1'),
    containers.load('24-well-plate', 'E2'),
    containers.load('24-well-plate', 'E1')
    ]

tiprack = containers.load('tiprack-1000ul', 'A1')
tiprack2 = containers.load('tiprack-1000ul', 'B2')
tiprack3 = containers.load('tiprack-1000ul', 'C1')

tuberack = containers.load('tube-rack-15_50ml', 'D2')


def run_protocol(number_of_plates: int=6):
    plates = all_plates[:number_of_plates]

    trash = tuberack[:6]  # 15mL tubes (x6)
    media = tuberack[6:]  # 50mL tubes (x4)

    # trash the contents of all the plates
    for plateNo, plate in enumerate(plates):
        pipette.consolidate(
            350, plate, trash[plateNo], new_tip='always')

    # add media from the 50mL tubes to all plates
    tube_vol = 50000
    media_tube_in_use = 0
    transfer_vol = 400
    media_vol_per_plate = 450 * 24  # depends on pipette vol, etc

    for plate in plates:
        tube_vol = tube_vol - media_vol_per_plate

        if tube_vol <= media_vol_per_plate:
            tube_vol = 50000
            media_tube_in_use += 1

        pipette.distribute(
            transfer_vol,
            media[media_tube_in_use],
            plate)
