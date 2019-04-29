from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'ELISA',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }


def run_custom_protocol():

    # labware setup
    tiprack_50 = labware.load('opentrons-tiprack-300ul', '2')
    tipracks_300 = [labware.load('opentrons-tiprack-300ul', slot)
                    for slot in ['3', '7', '10']]
    stp_plate = labware.load('96-well-plate-20mm', '6')
    trough = labware.load('trough-12row', '8')
    flat_plate = labware.load('96-flat', '9')

    # instruments setup
    m50 = instruments.P50_Multi(
        mount='left',
        tip_racks=[tiprack_50])
    m300 = instruments.P300_Multi(
        mount='right',
        tip_racks=tipracks_300)

    # reagent setup
    denaturing_buffer = trough.wells('A1')
    anti_CHO_HRP = trough.wells('A2')
    substrate_TMB = trough.wells('A3')
    stop_solution = trough.wells('A4')

    # transfer denaturing buffer
    for col in stp_plate.cols():
        m300.transfer(50, denaturing_buffer, col, mix_after=(15, 150))

    m300.delay(minutes=10)

    # add enzyme conjugate reagent
    m300.distribute(
        100, anti_CHO_HRP, flat_plate.cols(), blow_out=anti_CHO_HRP)

    # transfer STP plate
    for source, dest in zip(stp_plate.cols(), flat_plate.cols()):
        m50.transfer(25, source, dest)

    robot.pause("Remove the plate from the robot for incubation and shaking. \
    Wash and dry wells before placing it back in slot 9 and resuming.")

    # add TMB substrate
    m300.distribute(
        100,
        substrate_TMB,
        [col[0].top() for col in flat_plate.cols()],
        blow_out=substrate_TMB)

    m300.delay(minutes=30)

    # add stop solution
    m300.distribute(
        100,
        stop_solution,
        [col[0].top() for col in flat_plate.cols()],
        blow_out=stop_solution)
