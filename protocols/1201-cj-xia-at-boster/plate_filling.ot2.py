from opentrons import labware, instruments

trough_bottom = labware.load('point', '5')

slots = ['1', '2', '3', '4', '6', '7', '8', '9', '10']

tiprack = labware.load('tiprack-200ul', '11')

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
    number_of_plates: int=9,
    tip_starting_column: int=1
        ):

    plates = [labware.load('96-flat', slot)
              for slot in slots[:number_of_plates]]

    m300.start_at_tip(tiprack.cols(str(tip_starting_column)))
    m300.distribute(
        100,
        trough_bottom,
        [col for plate in plates for col in plate.cols()])
