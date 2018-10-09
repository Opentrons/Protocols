from opentrons import labware, instruments
from otcustomizers import StringSelection

# labware setup
block = labware.load('96-deep-well', '2')
plates = [labware.load('96-flat', slot)
          for slot in ['3', '4', '5', '6', '7', '8', '9', '10', '11']]
tiprack = labware.load('opentrons-tiprack-300ul', '1')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
        transfer_volume: float=100,
        number_of_plates: int=9,
        discard_tip: StringSelection('False', 'True')='False'):

    if discard_tip == 'False':
        discard_tip = False
    else:
        discard_tip = True

    for index, source in enumerate(block.cols()):
        dest = [plate.cols(index) for plate in plates[:number_of_plates]]
        m300.distribute(transfer_volume, source, dest, new_tip='once',
                        trash=discard_tip)
