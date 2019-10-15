from opentrons import labware, instruments

metadata = {
    'protocolName': 'ELISA',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


example_csv = """
50,500,5000
10,10000,100000
100,,
"""


def run_custom_protocol(
        number_of_columns: int=12):

    if number_of_columns > 12:
        raise Exception('The number of columns cannot exceed 12.')
    if number_of_columns % 2 == 1:
        raise Exception('The number of columns should be even.')

    # labware setup
    trough = labware.load('trough-12row', '8')
    plate = labware.load('96-flat', '9')

    tiprack_m300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['3', '7']]

    # instrument setup
    m300 = instruments.P300_Multi(
        mount='left',
        tip_racks=tiprack_m300)

    # reagent setup
    TMB_substrate = trough.wells('A2')
    stop_solution = trough.wells('A3')

    """
    Adding TMB substrate
    """
    m300.distribute(
        100,
        TMB_substrate,
        [col[0].top() for col in plate.cols[:number_of_columns]],
        blow_out=TMB_substrate)

    m300.delay(minutes=30)

    """
    Adding Stop Solution
    """
    for col in plate.cols[:number_of_columns]:
        m300.pick_up_tip()
        m300.transfer(100, stop_solution, col, new_tip='never')
        m300.drop_tip()
