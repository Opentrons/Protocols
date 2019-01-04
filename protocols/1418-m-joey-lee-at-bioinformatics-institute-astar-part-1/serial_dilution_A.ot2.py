from opentrons import labware, instruments

metadata = {
 'protocolName': 'Serial Dilution A',
 'author': 'Laura <protocols@opentrons.com>',
 'source': 'Custom Protocol Request'
}


def run_custom_protocol(
        sample_volume: int=4,
        number_samples: int=8,
        reagent_volume: int=100):

    if 'custom-resevoir' not in labware.list():
        labware.create(
             'custom-resevoir',
             grid=(1, 1),
             spacing=(63.88, 0),
             depth=25.5,
             diameter=2)
    initial_plate = labware.load('96-flat', '1')
    resevoir = labware.load('custom-resevoir', '4')
    tiprack = labware.load('opentrons-tiprack-300ul', '2')
    tiprack10 = labware.load('tiprack-10ul', '5')
    tuberack = labware.load('opentrons-tuberack-2ml-eppendorf', '3')

    m300 = instruments.P300_Multi(mount='left', tip_racks=[tiprack])
    p10 = instruments.P10_Single(mount='right', tip_racks=[tiprack10])
    # transfer sample
    p10.transfer(
        sample_volume,
        tuberack.wells(0, length=number_samples),
        initial_plate.columns('2'),
        new_tip='always')

    # perform serial dilution
    m300.pick_up_tip()
    m300.transfer(
        reagent_volume,
        resevoir,
        initial_plate.columns('2'),
        new_tip='never',
        mix_before=(3, 100)
    )
    m300.transfer(
        100,
        resevoir,
        initial_plate.columns('3', '4'),
        new_tip='never',
        mix_before=(3, 100))
    m300.transfer(
        120,
        resevoir,
        initial_plate.columns('5', '6'),
        new_tip='never',
        mix_before=(3, 100))
    m300.transfer(
        100,
        resevoir,
        initial_plate.columns('7', '8'),
        new_tip='never',
        mix_before=(3, 100))
    m300.transfer(
        100,
        resevoir,
        initial_plate.columns('7', '8'),
        new_tip='never',
        mix_before=(3, 100))
    m300.drop_tip()

    m300.transfer(
        [100, 100, 40, 40, 20, 20],
        initial_plate.columns('2', to='7'),
        initial_plate.columns('3', to='8'))
