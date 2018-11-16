from opentrons import labware, instruments, modules
from otcustomizers import StringSelection

"""
RNA Quantification 96 samples
"""

# labware setup
temp_deck = modules.load('tempdeck', '4')
temp_plate = labware.load('96-flat', '4', 'Donor Plate', share=True)
plate = labware.load('96-flat', '1', 'Receptor Plate')
tiprack_300 = labware.load('tiprack-200ul', '5')
tiprack_10 = labware.load('tiprack-10ul', '6')

temp_deck.set_temperature(4)
temp_deck.wait_for_temp()


def run_custom_protocol(
        reagent_container: StringSelection(
            'trough-12row', 'opentrons-tuberack-15ml')='trough-12row',
        reagent_volume: float=198,
        DNA_volume: float=2):

    # reagent
    dye = labware.load(reagent_container, '2').wells('A1')

    # pipette setup
    if reagent_container == 'trough-12row':
        p300 = instruments.P300_Multi(
            mount='left',
            tip_racks=[tiprack_300])
        plate_target = plate.cols()
    else:
        p300 = instruments.P300_Single(
            mount='left',
            tip_racks=[tiprack_300])
        plate_target = plate.wells()

    m10 = instruments.P10_Multi(
        mount='right',
        tip_racks=[tiprack_10])

    p300.transfer(reagent_volume, dye, plate_target)

    for source, dest in zip(temp_plate.cols(), plate.cols()):
        m10.transfer(DNA_volume, source, dest, blow_out=True)
