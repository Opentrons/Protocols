from opentrons import containers, instruments

trough = containers.load('trough-12row', 'A1')

trash = containers.load('trash-box', 'B1')

tiprack = containers.load('tiprack-200ul', 'C1')

plate1 = containers.load('96-deep-well', 'D1')
plate2 = containers.load('96-deep-well', 'E1')
plate3 = containers.load('96-deep-well', 'A2')
plate4 = containers.load('96-deep-well', 'B2')
plate5 = containers.load('96-deep-well', 'C2')
plate6 = containers.load('96-deep-well', 'D2')
plate7 = containers.load('96-deep-well', 'E2')

all_plates = [plate1, plate2, plate3, plate4, plate5, plate6]

p50multi = instruments.Pipette(
    axis='a',
    name='p50',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tiprack],
    trash_container=trash)

media = trough.wells(0, length=6)
cells = trough.wells('A8')


def run_custom_protocol(number_of_plates: int=6):
    plates = all_plates[0:number_of_plates]

    tube_vol = 20000
    media_vol = 80
    media_vol_per_plate = 96*media_vol
    media_tube = 0
    cell_vol = 20

    p50multi.pick_up_tip()
    for plate in plates:
        tube_vol = tube_vol - 7680

        if tube_vol <= media_vol_per_plate:
            tube_vol = 20000
            media_tube += 1

        p50multi.distribute(
            media_vol,
            media[media_tube],
            plate.rows(),
            new_tip='never')
    p50multi.drop_tip()

    p50multi.pick_up_tip()
    p50multi.mix(5, p50multi.max_volume)

    for plate in plates:
        p50multi.distribute(
            cell_vol,
            cells,
            plate.rows(), new_tip='never')

    p50multi.drop_tip()
