from opentrons import containers, instruments, robot
import time


"""
Serial Dilution + ELISA
@author Opentrons
@date Septeber 20th, 2017
@robot_model OT S Hood

"""

p1000rack = containers.load('tiprack-1000ul', 'A1', 'p20-rack')
p300rack = containers.load('tiprack-200ul', 'C1', 'p300-rack')
p300rack2 = containers.load('tiprack-200ul', 'E1', 'p300-rack')

serial_dilution_plate = containers.load('96-deep-well', 'B1')
reaction_plate = containers.load('96-deep-well', 'D1')
samples = containers.load('tube-rack-2ml', 'C2')

buffers = containers.load('trough-12row', 'D2')

liquid_trash = containers.load('point', 'A2', 'liquid trash')


EGFR = buffers.wells('A2')
wash_buffer = buffers.wells('A3')
superblock = buffers.wells('A4')

diluted_antibody = buffers.wells('A5')
tmb = buffers.wells('A6')
sulfuric_acid = buffers.wells('A7')

binding_buffer = buffers.wells('A1')

"""
Calculation for serial dilution stock
@stock_concentration initial concentration of stock soln;
list in order of sample number
(i.e sample 1 is first, sample 2 second etc) (units must be 5mg/mL)
@dilution_concentration concentration for first stock dilution
(units must be ug/mL)
@serial_volume units must be mL

Formula used, C1*V1 = C2*V2 Can be calculated from CSV file with
concentrations as well.
"""

# Change concentrations of solutions as well as amount of solutions
initial_concentration = [5, 5, 5, 5]  # mg/ml
dilution_concentration = 50  # ug/ml
serial_volume = 1

dilution_concentration2 = 1  # ug/ml
serial_volume2 = .5

stock_volume1 = []
stock_volume2 = []
dilution_rows = [0]  # initial amount of rows to be used in serial dilution

for con in initial_concentration:

    stock_volume1.append(
                        1000*(dilution_concentration*serial_volume) /
                        (con*1000))

    stock_volume2.append(
                        1000*(dilution_concentration2*serial_volume2) /
                        dilution_concentration)


for i in range(len(initial_concentration) - 1):
    dilution_rows.append(dilution_rows[i] + 3)

"""
These are the columns where each dilution concentration is located.
@sample_loc - Col 1 contains all stock solutions.
@sample_loc1 - Col 2 contains dilution reference to 50 ug/ml
@sample_loc2 - Col 3 contains final dilution reference to 1000 ng/ml
"""
sample_loc = [well(0) for well in samples.rows(0,
              length=len(initial_concentration))]
sample_loc1 = [well(1) for well in samples.rows(0,
               length=len(initial_concentration))]
sample_loc2 = [well(2) for well in samples.rows(0,
               length=len(initial_concentration))]

reaction_plate_rows = reaction_plate.rows()
reaction_plate_wells = reaction_plate.wells()

p1000 = instruments.Pipette(
    name="single",
    tip_racks=[p1000rack],
    trash_container=liquid_trash,
    min_volume=100,
    max_volume=1000,
    axis="b"
)

p300 = instruments.Pipette(
    name="multi",
    tip_racks=[p300rack, p300rack2],
    trash_container=liquid_trash,
    min_volume=50,
    max_volume=300,
    channels=8,
    axis="a"
)


def run_protocol(hours_to_incubate: float=16):
    # Step 1: Add 90uL of EGRF to ELISA plate and delay for 16 hours
    p300.transfer(90, EGFR, reaction_plate_rows, trash=False)

    # Bypass time.sleep in testing env
    import os
    if os.getenv('OT_TESTING') is not None:
        hours_to_incubate = 0

    robot._driver.power_off()

    time.sleep(60*60*hours_to_incubate)

    robot._driver.power_on()

    robot.home()

    p300.start_at_tip(p300rack.rows(0))
    p300.transfer(90, reaction_plate_rows, liquid_trash)

    # Step 2: Wash plate with buffer and add superblock
    p300.pick_up_tip()

    for _ in range(4):
        p300.transfer(300,
                      wash_buffer,
                      reaction_plate_rows,
                      mix_after=(3, 300),
                      new_tip='never')
        p300.transfer(300, reaction_plate_rows, liquid_trash, new_tip='never')

    p300.drop_tip()

    p300.transfer(200, superblock, reaction_plate_rows)

    # Step 3: Serial dilution to 1000 ng/mL
    dilution_vol = [1000 - stock for stock in stock_volume1]

    p1000.transfer(dilution_vol,
                   binding_buffer,
                   sample_loc1)

    p1000.transfer(stock_volume1, sample_loc, sample_loc1, mix_after=(5, 1000))

    dilution_vol2 = [1000 - stock for stock in stock_volume2]
    p1000.transfer(
        dilution_vol2,
        binding_buffer,
        sample_loc2)

    p1000.transfer(stock_volume2,
                   sample_loc1,
                   sample_loc2,
                   mix_after=(5, 1000),
                   new_tip='always')

    five_fold_columns = [
                        cols(1, length=7)
                        for cols in serial_dilution_plate.rows(dilution_rows)
                        ]
    reference_wells = [
                      cols(0)
                      for cols in serial_dilution_plate.rows(dilution_rows)
                      ]

    p1000.distribute(400, binding_buffer, five_fold_columns)
    p1000.transfer(500, sample_loc2, reference_wells, new_tip='always')

    for row in dilution_rows:
        for well in serial_dilution_plate.rows(row)(0, length=6):
            p1000.transfer(
                100,
                well,
                next(well), mix_after=(5, 500), new_tip='once')

    # Start ELISA wash
    p300.pick_up_tip()

    # get rid of superblock
    p300.transfer(200,
                  reaction_plate.rows('1', to='12'),
                  liquid_trash,
                  new_tip='never')

    for _ in range(4):
        p300.transfer(300,
                      wash_buffer,
                      reaction_plate.rows('1', to='12'),
                      mix_after=(3, 300),
                      new_tip='never')
        p300.transfer(300,
                      reaction_plate.rows('1', to='12'),
                      liquid_trash,
                      new_tip='never')

    p300.drop_tip()

    for row in dilution_rows:
        p300.distribute(90,
                        serial_dilution_plate.rows(row),
                        reaction_plate.rows(row, length=3))

    # incubation step??
    p300.transfer(90,
                  reaction_plate.rows('1', to='12'),
                  liquid_trash,
                  trash=False)

    p300.pick_up_tip()

    for _ in range(4):
        p300.transfer(300,
                      wash_buffer,
                      reaction_plate.rows('1', to='12'),
                      mix_after=(3, 300),
                      new_tip='never',
                      trash=False)
        p300.transfer(300,
                      reaction_plate.rows('1', to='12'),
                      liquid_trash,
                      new_tip='never',
                      trash=False)

    p300.drop_tip()

    p300.pick_up_tip()
    p300.transfer(90,
                  diluted_antibody,
                  reaction_plate.rows('1', to='12'),
                  new_tip='never',
                  trash=False)

    p300.transfer(90,
                  reaction_plate.rows('1', to='12'),
                  liquid_trash,
                  new_tip='never')
    p300.drop_tip()

    p300.pick_up_tip()
    for i in range(4):
        p300.transfer(300,
                      wash_buffer,
                      reaction_plate.rows('1', to='12'),
                      mix_after=(3, 300),
                      new_tip='never',
                      trash=False)
        p300.transfer(300,
                      reaction_plate.rows('1', to='12'),
                      liquid_trash,
                      new_tip='never',
                      trash=False)

    p300.drop_tip()

    p300.transfer(90, tmb, reaction_plate.rows('1', to='12'), new_tip='once')

    p300.delay(minutes=15)

    p300.transfer(90,
                  sulfuric_acid,
                  reaction_plate.rows('1', to='12'),
                  new_tip='once')
