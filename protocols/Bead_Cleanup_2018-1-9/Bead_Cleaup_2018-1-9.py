from opentrons import containers, instruments, robot

"""
Column A
"""
tiprack = containers.load('tiprack-200ul', 'A1', 'Tip M')
tiprack2 = containers.load('tiprack-200ul', 'A2', 'Tip N')
tiprack3 = containers.load('tiprack-200ul', 'A3', 'Tip O')

"""
Column B
"""
tiprack4 = containers.load('tiprack-200ul', 'B1', 'Tip J')
trough = containers.load('trough-4row', 'B2')
tiprack5 = containers.load('tiprack-200ul', 'B3', 'Tip L')
"""
Column C
"""
tiprack6 = containers.load('tiprack-200ul', 'C1', 'Tip G')
cleanup_plate = containers.load('384-plate', 'C2')
tiprack7 = containers.load('tiprack-200ul', 'C3', 'Tip I')


"""
Column D
"""
tiprack8 = containers.load('tiprack-200ul', 'D1', 'Tip D')
supernatant_plate = containers.load('384-plate', 'D2')
tiprack9 = containers.load('tiprack-200ul', 'D3', 'Tip F')

"""
Column E
"""
trash_A = containers.load('trash-box', 'E1')
liquid_trash = containers.load('trash-box', 'E2')
trash_C = containers.load('trash-box', 'E3')

"""
Pipettes
"""

m50 = instruments.Pipette(
    axis='a',
    name='50ul Multichannel',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[
        tiprack, tiprack2, tiprack3, tiprack4,
        tiprack5, tiprack6, tiprack7, tiprack8, tiprack9],
    trash_container=trash_A)

"""
Reagent and Variable Initialization
"""

AMPureXP = trough.wells('A1')
EtoH = trough.wells('A2', 'A3')
H20 = trough.wells('A4')


def run_custom_protocol(number_of_samples: int=384):

    initial_rows = [1, 7, 13, 19]
    samples = 192
    samples_processed = samples/96

    cleanup_wells = []
    for row in cleanup_plate.rows():
        cleanup_wells.append(row.wells('A'))
        cleanup_wells.append(row.wells('B'))

    supernantant_wells = []
    for row in supernatant_plate.rows():
        supernantant_wells.append(row.wells('A'))
        supernantant_wells.append(row.wells('B'))

    """
    1. Transfer 33ul of beads to the cleanup plate, reuse tips
    """
    m50.start_at_tip(tiprack.rows(0))
    m50.transfer(33, AMPureXP, cleanup_wells, new_tip='once', trash=False)

    for start in initial_rows[0:samples_processed]:
        start = start-1
        end = start + 12

        """
        2. Pause for 5 minutes, mix samples separately
        and then wait for 5 minutes on the magnet
        """
        robot.home()
        m50.delay(minutes=15)

        """
        3. Transfer 42ul of supernatant from
        plate in slot C2 to plate in slot D2
        """
        m50.transfer(
            42,
            cleanup_wells[start:end],
            supernantant_wells[start:end],
            new_tip='always')

        """
        4. Transfer 40ul of EtoH from resevoir 1 to plate in slot C2
        """
        m50.start_at_tip(tiprack2.rows(1))
        m50.transfer(
            40,
            EtoH[0],
            cleanup_wells[start:end],
            new_tip='once',
            trash=False)

        """
        5. Transfer 43ul of used EtoH from plate in slot C2 to liquid trash
        """
        m50.start_at_tip(tiprack2.rows(2))
        m50.transfer(
            43,
            cleanup_wells[start:end],
            liquid_trash,
            new_tip='always',
            trash=False)

        """
        6. Transfer 45ul of fresh EtoH from resevoir 2 to plate in slot C2
        """
        m50.transfer(
            45,
            EtoH[1],
            cleanup_wells[start:end],
            new_tip='once',
            trash=False)

        """
        7. Transfer 55ul of used EtoH from plate in slot C2 to liquid trash
        """
        curr_tip = m50.current_tip
        m50.transfer(
            45,
            cleanup_wells[start:end],
            liquid_trash,
            new_tip='always',
            trash=False)
        m50.start_at_tip(curr_tip)
        m50.transfer(
            10, cleanup_wells[start:end], liquid_trash, new_tip='always')
        """
        8. Elute DNA in H20 and put tips back in box
        """
        m50.transfer(
            12,
            H20,
            cleanup_wells[start:end],
            new_tip='once',
            trash=False)
