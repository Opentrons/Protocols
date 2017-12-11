from opentrons import containers, instruments

containers.create(
    'septum-plate',  # name of you container
    grid=(8, 7),   # specify amount of (columns, rows)
    spacing=(9, 18),  # distances (mm) between each (column, row)
    diameter=2.46,       # diameter (mm) of each well on the plate
    depth=10)

"""
Column A
"""
tiprack = containers.load('tiprack-200ul', 'A1')
tuberack = containers.load('tube-rack-2ml', 'A2')

"""
Column B
"""
septum1 = containers.load('septum-plate', 'B3')

"""
Column C
"""
septum2 = containers.load('septum-plate', 'C3')
trash = containers.load('trash-box', 'C2')
trough = containers.load('trough-12row', 'C1')

"""
Column D
"""
septum3 = containers.load('septum-plate', 'D1')
septum4 = containers.load('septum-plate', 'D2')
septum5 = containers.load('septum-plate', 'D3')

"""
Column E
"""
septum6 = containers.load('septum-plate', 'E1')
septum7 = containers.load('septum-plate', 'E2')
septum8 = containers.load('septum-plate', 'E3')

"""
Instruments
"""
p50 = instruments.Pipette(
    axis='a',
    name='p50multi',
    max_volume=50,
    min_volume=5,
    channels=8,
    tip_racks=[tiprack],
    trash_container=trash)

p100 = instruments.Pipette(
    axis='b',
    name='p100single',
    max_volume=100,
    min_volume=10,
    channels=1,
    tip_racks=[tiprack],
    trash_container=trash)


def run_custom_protocol(plate_number: int=4):
    plates = [septum1, septum2, septum3, septum4,
              septum5, septum6, septum7, septum8]
    # Plates/Tube racks
    if (plate_number > 8):
        raise Exception(print("Error - too many plates"))
    """
    Variable initialization/Reagent setup
    """
    multichannel = False
    if plate_number > 2:
        multichannel = True

    if multichannel:
        pipette = p50
        source = trough
    else:
        pipette = p100
        source = tuberack

    hexane = source.wells('A1')
    work_soln = source.wells('A2')

    """
    Protocol
    """
    # Step 2
    pipette.pick_up_tip()
    pipette.transfer(30, hexane, trash, new_tip='never', blow_out=True)

    for septum in plates[0:plate_number]:

        # Step 4-9
        if multichannel:
            sept_multi = [well.top(-5) for well in septum.cols(0)]
            pipette.aspirate(5, work_soln)
            for well in sept_multi:
                pipette.aspirate(20, work_soln)
                pipette.dispense(20, well).touch_tip(-2)

            pipette.dispense(work_soln)

        else:
            sept_single = [well.top(-5) for well in septum.wells()]
            pipette.aspirate(5, work_soln)
            for well in sept_single:
                pipette.aspirate(20, work_soln)
                pipette.dispense(20, well).touch_tip(-2)

            pipette.dispense(work_soln)
        # Step 10

    pipette.return_tip()
