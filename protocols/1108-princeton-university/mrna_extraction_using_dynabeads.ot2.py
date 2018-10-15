from opentrons import labware, instruments, modules, robot
import math

"""
Bead Preparation and Direct mRNA Isolation
"""

# labware setup
mag_module = modules.load('magdeck', '1')
mag_plate = labware.load('biorad-hardshell-96-PCR', '1', share=True)
sample_plate = labware.load('PCR-strip-tall', '2')
new_plate = labware.load('PCR-strip-tall', '3')
deep_block = labware.load('96-deep-well', '4')
trough = labware.load('trough-12row', '5')
temp_module = modules.load('tempdeck', '7')
temp_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)
tipracks50 = [labware.load('tiprack-200ul', slot)
              for slot in ['6']]
tipracks300 = [labware.load('tiprack-200ul', slot)
               for slot in ['8', '9', '10', '11']]

# reagent setup
dynabeads = deep_block.wells('A1')
LBB = trough.wells('A1')
wash_buffer_A = trough.wells('A2')
wash_buffer_B = trough.wells('A3')
LSB = trough.wells('A4')
tris_HCl = trough.wells('A5')
liquid_trash = trough.wells('A12')

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks50)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks300)

tip_50_count = 0
tip_50_count_limit = 96 * len(tipracks50)

tip_300_count = 0
tip_300_count_limit = 12 * len(tipracks300)


def update_tip_50_count(num):
    global tip_50_count
    tip_50_count += num
    if tip_50_count == tip_50_count_limit:
        robot.pause("P50 tips have run out. Resume the protocol when the tips\
    are replenished.")
        p50.reset_tip_tracking()
        p50.start_at_tip(tipracks50[0].wells(0))
        tip_50_count = 0


def update_tip_300_count(num):
    global tip_300_count
    tip_300_count += num
    if tip_300_count == tip_300_count_limit:
        robot.pause("P300 tips have run out. Resume the protocol when the tips\
    are replenished.")
        m300.reset_tip_tracking()
        m300.start_at_tip(tipracks300[0].cols(0))
        tip_300_count = 0


def wash_plate(number_of_samples, wash_buffer, dest, bead_wait_time):
    for col in dest:
        m300.transfer(100, wash_buffer, col, mix_after=(2, 100))
        update_tip_300_count(1)
    mag_module.engage()
    m300.delay(minutes=bead_wait_time)
    for col in dest:
        m300.transfer(100, dest, liquid_trash)
        update_tip_300_count(1)
    mag_module.disengage()


def run_custom_protocol(
        number_of_samples: int=96,
        bead_wait_time: int=5):

    mag_loc_top = [well.top() for well in mag_plate.wells()][
        :number_of_samples]
    mag_loc_bottom = [well.bottom(1)
                      for well in mag_plate.wells()][:number_of_samples]

    cols = math.ceil(number_of_samples/8)

    """
    beads prepartion
    """
    # mix dynabeads thoroughly before using
    p50.pick_up_tip()
    p50.mix(10, 50, dynabeads)
    p50.distribute(
        20, dynabeads, mag_loc_top, mix_before=(5, 50),
        disposal_vol=0, new_tip='once')
    update_tip_50_count(1)

    # turn on Magnetic Module
    mag_module.engage()
    p50.delay(minutes=bead_wait_time)

    # remove supernatant
    p50.transfer(25, mag_loc_bottom, liquid_trash, new_tip='once')
    update_tip_50_count(1)

    # turn off Magnetic Module
    mag_module.disengage()

    # resuspend beads in LBB buffer
    for col in mag_plate.cols('1', length=cols):
        m300.transfer(100, LBB, col, mix_after=(10, 100))
        update_tip_300_count(1)

    """
    Direct mRNA Isolation
    """
    # turn on Magnetic Module
    mag_module.engage()
    p50.delay(minutes=bead_wait_time)

    # remove supernatant
    for col in mag_plate.cols('1', length=cols):
        m300.transfer(100, col.bottom(1), liquid_trash)
        update_tip_300_count(1)

    # add sample lysate to beads
    for sample_col, dest_col in zip(
            sample_plate.cols('1', length=cols),
            mag_plate.cols('1', length=cols)):
        m300.transfer(100, sample_col, dest_col, mix_after=(10, 100))
        update_tip_300_count(1)

    robot.pause("Incubate mix on a plate mixer for 10 minutes at room \
    temperature. Increase incubation time if the solution is viscous. Place \
    the plate back on the Magnetic Module.")

    # turn on Magnetic Module
    mag_module.engage()
    p50.delay(minutes=bead_wait_time)

    # remove supernatant
    for col in mag_plate.cols('1', length=cols):
        m300.transfer(100, col.bottom(1), liquid_trash)
        update_tip_300_count(1)

    # wash with Washing Buffer A
    wash_plate(
        number_of_samples, wash_buffer_A, mag_plate.cols('1', length=cols),
        bead_wait_time)

    # wash with Washing Buffer B
    wash_plate(
        number_of_samples, wash_buffer_B, mag_plate.cols('1', length=cols),
        bead_wait_time)

    # wash with LSB
    wash_plate(number_of_samples, LSB, mag_plate.cols('1', length=cols),
               bead_wait_time)

    # add Tris-HCl
    for col in mag_plate.cols('1', length=cols):
        m300.transfer(31, tris_HCl, col, mix_after=(3, 30))
        update_tip_300_count(1)

    robot.pause("Put the plate on the Temperature Module.")

    # set Temp Module to 80°
    temp_module.set_temperature(80)
    temp_module.wait_for_temp()
    p50.delay(minutes=5)
    temp_module.deactivate()

    robot.pause("Put the plate back on the Magnetic Module.")

    # turn on Magnetic Module
    mag_module.engage()
    p50.delay(minutes=bead_wait_time)

    # transfer 30 uL to a fresh tube
    for index, col in enumerate(mag_plate.cols('1', length=cols)):
        m300.transfer(30, col.bottom(1), new_plate.cols(index))
        update_tip_300_count(1)
