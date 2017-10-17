"""
NGS Prep Clean-up
@author Opentrons
@date October 17th, 2017
@robot OT Pro, OT S
"""

from opentrons import containers, instruments, robot
import math

"""
 Column A
"""
# trough with solutions
beads = containers.load('point', 'A1')

tip300_rack = containers.load('tiprack-200ul', 'A3')

"""
 Column B
"""
tip200_rack = containers.load('tiprack-200ul', 'B1')

EtOH = containers.load('point', 'B2')

"""
 Column C
"""
# trash to dispose of liquid
H20 = containers.load('point', 'C2')

mag_plate = containers.load('96-PCR-flat', 'C3')

"""
 Column D
"""

# cool deck (note this will take up slots D3/E3)
elution_plate = containers.load('96-PCR-flat', 'D1')

# output plate for library reactions
TE = containers.load('point', 'D2')


"""
 Column E
"""

# heat plate for reactions
gel_plate = containers.load('96-PCR-flat', 'E1')

trash = containers.load('trash-box', 'E3')

# p200 (20 - 200 uL) (single)
p200single = instruments.Pipette(
    axis='b',
    name='p200single',
    max_volume=200,
    min_volume=20,
    channels=1,
    tip_racks=[tip200_rack])

p300multi = instruments.Pipette(
    axis='a',
    name='p300multi',
    max_volume=300,
    min_volume=50,
    channels=8,
    tip_racks=[tip300_rack])

mag_deck = instruments.Magbead(name='mag_deck')


def run_protocol(TE_volume: float=20.0, number_of_samples: int=96):
    # all commands go in this function

    try:
        number_of_samples <= 96
    except ValueError:
        print(
         "You can only input samples less than or equal to 96.")

        # Helper Functions
        def tip_wash(pipette):
            for _ in range(3):
                pipette.aspirate(200, H20)
                pipette.dispense(200, trash)
            for _ in range(2):
                pipette.aspirate(200, EtOH)
                pipette.dispense(200, trash)

        def EtOH_wash(pipette, plate, tiprack, vol):
            p300multi.start_at_tip(tip300_rack.rows('1'))

            for row in plate.rows():
                pipette.pick_up_tip()
                pipette.aspirate(vol, EtOH)
                pipette.dispense(vol, row)
                pipette.mix(5, vol)

                tip_wash(pipette)

                pipette.return_tip()

            mag_deck.engage().delay(minutes=5)

            p300multi.start_at_tip(tip300_rack.rows('1'))
            for row in plate.rows():
                pipette.pick_up_tip()

                pipette.aspirate(vol, row)
                pipette.dispense(vol, trash)

                tip_wash(pipette)

                pipette.return_tip()

    """
       Step 1 Add Magnetic Beads:
       -Get 8 tips from rack A
       -Go to bead trough and pipette up and down 5x with 100 ul to mix
       -Suck up 50 ul of beads
       -Dispense into PCR plate (magnet down),
       pipette up and down 5x with 100 ul to mix

       Step 2: Tip Wash
       -(Pick up 200 ul of water, expel into waste) x 3 times
       -(Pick up 200 ul of EtOH, expel into waste) x 2
       -Replace tips into box

    """

    # Step 1 and Step 2
    for row in mag_plate.rows():
        p300multi.pick_up_tip()
        p300multi.mix(5, 100, beads)
        p300multi.aspirate(50, beads)
        p300multi.dispense(50, row)
        p300multi.mix(5, 100)

        tip_wash(p300multi)

        p300multi.return_tip()

    """
    Step 3: Bind and Beadwash
            -Bind DNA for 10 minutes
            -Raise magnent and wait 10 minutes
            -Remove 125 ul of elute from all wells
    Step 4: Wash tips
    """

    robot.home()
    p300multi.delay(minutes=10)

    mag_deck.engage().delay(minutes=10)

    p300multi.start_at_tip(tip300_rack.rows('1'))
    for row in mag_plate.rows():
        p300multi.pick_up_tip()

        p300multi.aspirate(125, row)
        p300multi.dispense(125, trash)

        tip_wash(p300multi)

        p300multi.return_tip()

    mag_deck.disengage()

    """
    Step 5: Wash all wells with EtOH
            -Add 200 EtOH to each well and pipette up and down
            5x
            -Wash tips
    Step 6: Lift magnent and wait five minutes
    Step 7: Remove 200 to waste
    """
    EtOH_wash(p300multi, mag_plate, tip300_rack, 200)

    """
    Step 8: Disengage mag deck
    Step 9: Wash all wells with 200 EtOH
    Step 10: Disengage mag deck
    Step 11: Wash all wells with 50 EtOH
    Step 12: Disengage mag deck
    """
    mag_deck.disengage()

    EtOH_wash(p300multi, mag_plate, tip300_rack, 200)

    mag_deck.disengage()

    EtOH_wash(p300multi, mag_plate, tip300_rack, 50)

    mag_deck.disengage()

    robot.home()
    p300multi.delay(minutes=5)

    """
    Step 13: Elute DNA from all rows
             -Resuspend in TE
             -Sit 5 minutes
             -Magnetize
             -Put elute in clean plate and gel plate
    """
    p200single.start_at_tip(tip200_rack.wells('A1'))
    for row in mag_plate.rows():
        for well in row:
            p200single.pick_up_tip()

            p200single.aspirate(TE_volume, TE)
            p200single.dispense(TE_volume, well)
            p200single.mix(5, TE_volume)

            tip_wash(p200single)

            p200single.return_tip()

    p200single.delay(minutes=5)

    mag_deck.engage().delay(minutes=5)

    p200single.start_at_tip(tip200_rack.wells('A1'))

    num_rows = math.ceil(number_of_samples/8)

    for i in range(num_rows):
        for well1, well2, well3 in zip(mag_plate.rows(i),
                                       elution_plate.rows(i),
                                       gel_plate.rows(i)):
            p200single.pick_up_tip()

            p200single.aspirate(TE_volume, well1)
            p200single.dispense(TE_volume, well2)

            p200single.aspirate(5, well2)
            p200single.dispense(5, well3)

            p200single.drop_tip(trash)
