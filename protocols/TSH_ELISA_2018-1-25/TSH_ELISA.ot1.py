from opentrons import containers, instruments, robot
import math

"""
Workflow description: TSH ELISA Assay Procedure (see attached pdf)
Robot: OT-One S Pro
Pipettes: p100 (10 - 100 uL) (single), p300 (50 - 300 uL) (multi)
Labware: 96 well plate (flat),200uL tiprack,2 mL tube rack,0.75 mL tube rack
"""

"""
Column A
"""
tiprack1 = containers.load('tiprack-200ul', 'A1')
tiprack2 = containers.load('tiprack-200ul', 'A2')


"""
Column B
"""
trough = containers.load('trough-12row', 'B1')
trash = containers.load('trash-box', 'B2')
"""
Column C
"""
plate = containers.load('96-flat', 'C1')
tuberack = containers.load('tube-rack-15_50ml', 'C2')


"""
Column D
"""
samples = containers.load('tube-rack-2ml', 'D1')
liquid_trash = containers.load('trash-box', 'D2')

"""
Instruments
"""

pipette = instruments.Pipette(
    axis='a',
    name='100ul Singlechannel',
    max_volume=100,
    min_volume=10,
    channels=1,
    tip_racks=[tiprack1],
    trash_container=trash)

p300 = instruments.Pipette(
    axis='b',
    name='300ul Multichannel',
    max_volume=300,
    min_volume=50,
    channels=1,
    tip_racks=[tiprack2],
    trash_container=trash)

"""
Reagent and Variable Set-up
"""
standard_25 = tuberack.wells('A1')
standard_10 = tuberack.wells('B1')
standard_5 = tuberack.wells('C1')
standard_2 = tuberack.wells('A2')
standard_half = tuberack.wells('B2')
standard_0 = tuberack.wells('C2')

enzyme_conjugate = tuberack.wells('A3')

TMB = tuberack.wells('B3')
stop_soln = tuberack.wells('A4')
dioH20 = trough.wells('A1')


def run_custom_protocol(number_of_samples: int=24,
                        number_of_mixes: int=10,
                        sample_volume: int=100,
                        standard_replicates: int=3):

    samples_left = number_of_samples
    num_rows = math.ceil(number_of_samples/8)
    # 1. Dispense 100 µL of standards
    pipette.transfer(
        sample_volume, standard_25, plate.cols(0)[0:standard_replicates])
    pipette.transfer(
        sample_volume, standard_10, plate.cols(1)[0:standard_replicates])
    pipette.transfer(
        sample_volume, standard_5, plate.cols(2)[0:standard_replicates])
    pipette.transfer(
        sample_volume, standard_2, plate.cols(3)[0:standard_replicates])
    pipette.transfer(
        sample_volume, standard_half, plate.cols(4)[0:standard_replicates])
    pipette.transfer(
        sample_volume, standard_0, plate.cols(5)[0:standard_replicates])

    sample = samples.wells('A1')
    samples_left = number_of_samples
    end = False
    # 1. Dispense specimens and controls into appropriate wells.
    for row in range(num_rows):

        if samples_left > 8:
            well_val = 8
        else:
            well_val = samples_left
            end = True

        for well in range(well_val):

            pipette.pick_up_tip()
            pipette.aspirate(sample_volume, sample)
            #  Evaluate the starting well for the experimental sample
            #  Based on the amount of standards inputted
            #  Always starts in the "A" Column
            pipette.dispense(
                sample_volume,
                plate.wells(8*(standard_replicates+(row*2)) + well))

            #  This grabs the next row after the
            #  experimental sample for the negative control
            #  You need a pairing for each sample.
            pipette.aspirate(sample_volume, sample)
            pipette.dispense(
                sample_volume,
                plate.wells(8*(standard_replicates+(row*2+1)) + well))

            pipette.drop_tip()
            # Will only grab the next sample if
            # it's not at the end of the tube rack
            if (well == 7) and (not end):
                sample = next(sample)

        samples_left = samples_left-8

    # 3. Dispense 100 µL of Enzyme Conjugate Reagent into each well.
    # 4. Thoroughly mix for 30 seconds.
    # It is very important to mix them completely.
    for row in range(num_rows):

        # Checks how many samples are left so that it can iterate through
        # one row each
        if samples_left > 8:
            well_val = 8
        else:
            well_val = samples_left

        for well in range(well_val):

            pipette.pick_up_tip()
            pipette.aspirate(sample_volume, enzyme_conjugate)
            pipette.dispense(
                sample_volume,
                plate.wells(8*(standard_replicates+(row*2)) + well))
            pipette.mix(number_of_mixes, sample_volume)
            pipette.drop_tip()

    # 5. Incubate at room temperature (18-25°C) for 60 minutes.
    robot.home()

    pipette.delay(minutes=60)

    # 6. Remove the incubation mixture by
    # flicking plate contents into a waste container.

    for row in range(num_rows):
        p300.pick_up_tip()
        p300.aspirate(
            sample_volume*2, plate.wells(8*(standard_replicates+(row*2))))
        p300.dispense(liquid_trash)
        p300.drop_tip()

    # 7. Rinse and flick the microtiter wells
    # 5 times with distilled or deionized water. (Please do not use tap water.)
    for row in range(num_rows):
        for _ in range(5):
            p300.pick_up_tip()
            p300.aspirate(sample_volume*2, dioH20)
            p300.dispense(plate.wells(8*(standard_replicates+(row*2))))

            p300.aspirate(
                sample_volume*2, plate.wells(8*(standard_replicates+(row*2))))
            p300.dispense(liquid_trash)
            p300.drop_tip()

    #  9. Dispense 100 µL of TMB Reagent into each well.
    #  Gently mix for 10 seconds.
    for row in range(num_rows):

        if samples_left > 8:
            well_val = 8
        else:
            well_val = samples_left

        for well in range(well_val):

            pipette.pick_up_tip()
            pipette.aspirate(sample_volume, TMB)
            pipette.dispense(
                sample_volume,
                plate.wells(8*(standard_replicates+(row*2)) + well))
            pipette.mix(number_of_mixes//2, sample_volume)
            pipette.drop_tip()

    # 10. Incubate at room temperature for 20 minutes.
    robot.home()

    pipette.delay(minutes=20)

    # 11. Stop the reaction by adding 100 µL of Stop Solution to each well.
    # 12. Gently mix for 30 seconds. It is important to make sure
    # that all the blue color changes to yellow color
    # completely.
    for row in range(num_rows):

        if samples_left > 8:
            well_val = 8
        else:
            well_val = samples_left

        for well in range(well_val):

            pipette.pick_up_tip()
            pipette.aspirate(sample_volume, stop_soln)
            pipette.dispense(
                sample_volume,
                plate.wells(8*(standard_replicates+(row*2)) + well))
            pipette.mix(number_of_mixes, sample_volume)
            pipette.drop_tip()
