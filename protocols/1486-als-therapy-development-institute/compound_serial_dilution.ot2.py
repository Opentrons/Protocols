from opentrons import labware, instruments

metadata = {
    'protocolName': 'Compound Serial Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol(
        number_of_plates: int=10,
        num_of_dilutions: int=10,
        transfer_volume: float=30
        ):

    if number_of_plates > 10:
        raise Exception('Number of plate must not exceed 10.')

    # labware setup
    tiprack = labware.load('tiprack-200ul', '1')
    plates = [labware.load('96-flat', str(slot))
              for slot in range(2, 12)][:number_of_plates]

    # instrument setup
    m300 = instruments.P300_Multi(
        mount='left',
        tip_racks=[tiprack])

    for plate in plates:
        m300.pick_up_tip()
        m300.mix(3, 50, plate.cols('1'))
        for source, dest in zip(
                plate.cols('1', length=num_of_dilutions),
                plate.cols('2', length=num_of_dilutions)):
            m300.transfer(transfer_volume, source, dest, new_tip='never')
            m300.mix(3, 50, dest)
        m300.drop_tip()
