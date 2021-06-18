metadata = {
    'protocolName': 'ProcartaPlex Protocol-1 [6/7]',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}


def run(protocol):
    [mnt300] = get_values(  # noqa: F821
     'mnt300')

    # load labware
    tips = [
        protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', s) for s in [7, 10]
        ]

    m300 = protocol.load_instrument('p300_multi_gen2', mnt300, tip_racks=tips)
    sampPlate = protocol.load_labware('spl_96_wellplate_200ul_flat', '4')
    standardsPlate = protocol.load_labware('spl_96_wellplate_200ul_flat', '5')
    destPlate = protocol.load_labware('spl_96_wellplate_200ul_flat', '1')
    rsvr = protocol.load_labware('nest_12_reservoir_15ml', '6')

    # Variables
    beads, washBuffer = rsvr.wells()[:2]

    destWells = destPlate.rows()[0]
    sampsAndStandards = sampPlate.rows()[0][:10]+standardsPlate.rows()[0]

    # create functions
    def msg_with_alert(msg, time=6):
        """
        This function will flash the on-deck lights, once per 2 seconds
        and display the 'msg' in the pause step in the OT app.
        Param msg: Message to be included in the pause step.
        Param time: Number of seconds to flash lights
        """
        for _ in range(time):
            protocol.set_rail_lights(not protocol.rail_lights_on)
            protocol.delay(seconds=1)

        protocol.pause(msg)

    def wash(src):
        """
        This function contains all of the steps neeeded for this custom wash.
        The pipette will pick up tips and using the same set of tips,
        transfer 150uL of Wash Buffer to all of the wells in the destination
        plate (top of the well to prevent cross contamination).
        Once complete, the pipette will trash the tips and the OT-2 will begin
        blinking to signify that the user can remove the plate for off deck
        processing.
        Param src: Location of wash buffer (should be well)
        """
        m300.pick_up_tip()
        for well in destWells:
            m300.transfer(
                150, src, well.top(-2), new_tip='never', air_gap=30)
        m300.drop_tip()

        msg_with_alert("""
        Wash Buffer added. Please remove plate for off robot processing.
        When complete, please return plate to deck and click RESUME.
        """)

    # Add 50uL of beads to all the wells in dest plate
    protocol.comment('Adding 50uL of beads to wells...')

    m300.pick_up_tip()

    for well in destWells:
        m300.transfer(
            50, beads, well.top(-4), mix_before=(3, 100),
            air_gap=20, new_tip='never'
            )

    m300.drop_tip()

    msg_with_alert("""
    Please remove plate and incubate on magnet for 2 minutes.
    Once complete, please replace plate on deck and click RESUME
    """)

    # Wash 1
    wash(washBuffer)
    msg_with_alert("""
    Please add Sample Plate and Standard Plate if not on the deck.
    When ready, click RESUME
    """)

    # Transfer samples and standards to destination plate
    protocol.comment('Transferring 50uL of sample and standards to wells...')

    for src, dest in zip(sampsAndStandards, destWells):
        m300.transfer(50, src, dest, mix_before=(3, 50), air_gap=20)

    msg_with_alert("""
    Please remove plate and incubate for 30 minutes on rotator.
    Afterwards, please incubate overnight at 4 deg C.
    When ready to resume, begin PROTOCOL NAME PART 2
    """)
