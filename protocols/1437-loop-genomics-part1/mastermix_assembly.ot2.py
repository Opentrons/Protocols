from opentrons import labware, instruments

custom_deep_plate = '96-deep-well-1.2ml'
if custom_deep_plate not in labware.list():
    labware.create(
        custom_deep_plate,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.4,
        depth=33.5)


def run_custom_protocol(
        mastermix_volume: float=80,
        reagent_volume: float=15,
        number_of_plates_to_fill: int=8,
        number_of_columns_to_fill: int=3):

    # labware setup
    pcr_plates = [labware.load('PCR-strip-tall', slot)
                  for slot in ['1', '2', '4', '5', '7', '8', '10', '11']][
                    :number_of_plates_to_fill]

    deep_well3 = labware.load(custom_deep_plate, '3')
    deep_well6 = labware.load(custom_deep_plate, '6')
    tiprack = labware.load('tiprack-200ul', '9')

    # instrument setup
    m50 = instruments.P50_Multi(
        mount='right',
        tip_racks=[tiprack])

    for index in range(number_of_columns_to_fill):
        m50.pick_up_tip()
        m50.transfer(
            mastermix_volume,
            deep_well6.cols(index),
            deep_well3.cols(index)[0].top(),
            new_tip='never')
        m50.mix(10, 50, deep_well3.cols(index))

        dest = [plate.cols(index) for plate in pcr_plates]
        m50.distribute(
            reagent_volume, deep_well3.cols(index), dest, new_tip='never')
        m50.drop_tip()
