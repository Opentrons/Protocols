from opentrons import labware, instruments, modules, robot

# labware setup
mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('96-deep-well', '1', share=True)
plate = labware.load('96-deep-well', '2')
trough = labware.load('trough-12row', '3')
liquid_trash = labware.load('point', '4')
flat_plate = labware.load('96-flat', '5')

# reagent setup
RNase_A = trough.wells('A1')
solution_II = trough.wells('A2')
N3_buffer = trough.wells('A3')
LC_beads = trough.wells('A4')
ETR_bind_buffer = trough.wells('A5')
Mag_Bind_RQ = trough.wells('A6')
ETR_wash_buffer = trough.wells('A7')
VHB_buffer = trough.wells('A8')
SPM_wash_buffer = trough.wells('A9')
elution_buffer = trough.wells('A10')

# tipracks
tipracks300 = [labware.load('tiprack-200ul', slot)
               for slot in ['6', '7', '8', '9', '10']]

tiprack50 = labware.load('tiprack-200ul', '11')

# pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks300)

m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tiprack50])


def run_custom_protocol(
        elution_buffer_volume: float=50):

    plate_loc = [well for well in plate.rows(0)]
    plate_top_loc = [well.top() for well in plate_loc]

    mag_loc = [well for well in plate.rows(0)]

    m300.transfer(250, RNase_A, plate_top_loc)

    robot.pause("Resuspend the cells by vortexing.")

    m300.transfer(250, solution_II, plate_top_loc)

    robot.pause("Gently mix by shaking and rotating the plate for 1 minute \
    to obtain a cleared lysate. A 5 minute incubation at room temperature may \
    be necessary")

    m300.transfer(125, N3_buffer, plate_top_loc)

    m300.transfer(30, LC_beads, plate_top_loc)

    robot.pause("Mix by gently shaking the plate until a flocculent white \
    precipitate forms. Place the block on the MagDeck. Place a new 96-well \
    Block in slot 2.")

    mag_deck.engage(height=15)
    m300.delay(minutes=5)

    for source, dest in zip(mag_loc, plate_loc):
        m300.transfer(500, source, dest)

    mag_deck.disengage()

    m300.transfer(500, ETR_bind_buffer, plate_top_loc)

    for well in plate_loc:
        m50.transfer(20, Mag_Bind_RQ, well, mix_after=(10, 50), new_tip='once')

    m300.delay(minutes=5)

    robot.pause("Place the block from slot 2 in the MagDeck. You can discard \
    the old plate.")

    mag_deck.engage(height=15)
    m300.delay(minutes=5)

    for well in mag_loc:
        m300.transfer(1050, well, liquid_trash)

    mag_deck.disengage()

    for index, well in enumerate(mag_loc):
        m300.pick_up_tip()
        if index == 0:
            reuse_tip = m300.current_tip()
        m300.transfer(500, ETR_wash_buffer, well, new_tip='never')
        m300.mix(10, 300, well)
        m300.return_tip()

    mag_deck.engage(height=15)
    m300.delay(minutes=5)

    m300.start_at_tip(reuse_tip)
    for well in mag_loc:
        m300.transfer(510, well, liquid_trash)

    mag_deck.disengage()

    robot.pause("Replenish all of your tipracks.")
    m300.reset_tip_tracking()
    m300.start_at_tip(tipracks300[0].cols(0))

    for cycle in range(2):
        for index, well in enumerate(mag_loc):
            m300.pick_up_tip()
            if index == 0:
                reuse_tip = m300.current_tip()
            m300.transfer(700, VHB_buffer, well, new_tip='never')
            m300.mix(10, 300, well)
            m300.return_tip()

        mag_deck.engage(height=15)
        m300.delay(minutes=5)

        m300.start_at_tip(reuse_tip)
        for well in mag_loc:
            m300.transfer(700, well, liquid_trash)

    for index, well in enumerate(mag_loc):
        m300.pick_up_tip()
        if index == 0:
            reuse_tip = m300.current_tip()
        m300.transfer(700, SPM_wash_buffer, well, new_tip='never')
        m300.mix(10, 300, well)
        m300.return_tip()

    mag_deck.engage(height=15)
    m300.delay(minutes=5)

    m300.start_at_tip(reuse_tip)
    for well in mag_loc:
        m300.transfer(700, well, liquid_trash)

    m300.delay(minutes=10)
    mag_deck.disengage()

    for well in mag_loc:
        m300.transfer(elution_buffer_volume, elution_buffer, well,
                      mix_after=(20, 50))

    mag_deck.engage()
    m300.delay(minutes=5)

    flat_loc = [well for well in flat_plate.rows(0)]
    for source, dest in zip(mag_loc, flat_loc):
        m300.transfer(elution_buffer_volume, source, dest)
