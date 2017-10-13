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
plate_type = '24-well-plate'

plate_1 = containers.load(plate_type, 'A2')
plate_2 = containers.load(plate_type, 'B1')
plate_3 = containers.load(plate_type, 'C2')
plate_4 = containers.load(plate_type, 'D1')
plate_5 = containers.load(plate_type, 'E2')
plate_6 = containers.load(plate_type, 'E1')

tiprack = containers.load('tiprack-1000ul', 'A1')
tiprack2 = containers.load('tiprack-1000ul', 'B2')
tiprack3 = containers.load('tiprack-1000ul', 'C1')

tuberack = containers.load('tube-rack-15_50ml', 'D2')


def run_protocol(number_of_plates: int=6):
    plates = [plate_1, plate_2, plate_3, plate_4, plate_5, plate_6]

    plates = plates[0:number_of_plates]

    trash = tuberack.rows('1', to='2')
    media = tuberack.rows('3', to='4')

    i = 0
    j = 0
    for plate in plates:

        if j == 3:
            j = 0
            i = 1
        pipette.consolidate(350, plate.rows(), trash[i][j], new_tip='always')
        j += 1

    i = 0
    j = 0

    tube_vol = 50
    for plate in plates:
        tube_vol = tube_vol - 9.6

        if tube_vol <= 0:
            tube_vol = 50
            if j == 2:
                i = 1
                j = 0
            else:
                j += 1
        pipette.distribute(400, media[i][j], plate.rows())
