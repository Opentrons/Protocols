
from opentrons import containers, instruments

trough = containers.load('trough-12row', 'A1')

trash = containers.load('trash-box', 'B1')

tiprack = containers.load('tiprack-200ul', 'D2')

plate1 = containers.load('96-deep-well', 'A2')
plate2 = containers.load('96-deep-well', 'B2')
plate3 = containers.load('96-deep-well', 'C2')
plate4 = containers.load('96-deep-well', 'A3')
plate5 = containers.load('96-deep-well', 'B3')
plate6 = containers.load('96-deep-well', 'C3')
plate7 = containers.load('96-deep-well', 'D3')

all_plates = [plate1, plate2, plate3, plate4, plate5, plate6, plate7]

p200multi = instruments.Pipette(
    axis='a',
    name='p200',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=trash)

media = trough.wells(0, length=6)
cells = trough.wells('A8')


def run_custom_protocol(number_of_plates: int=7):
    plates = all_plates[0:number_of_plates]

    tube_vol = 20000
    media_vol = 80
    media_vol_per_plate = 96*media_vol
    media_tube = 0
    cell_vol = 20

    p200multi.pick_up_tip()
    for plate in plates:
        tube_vol = tube_vol - 7680

        if tube_vol <= media_vol_per_plate:
            tube_vol = 20000
            media_tube += 1

        p200multi.distribute(
            media_vol,
            media[media_tube],
            plate.rows(),
            new_tip='never')
    p200multi.drop_tip()

    for plate in plates:
        p200multi.distribute(
            cell_vol,
            cells,
            plate.rows(),
            mix_before=(5, p200multi.max_volume))
