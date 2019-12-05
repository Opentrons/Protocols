metadata = {
    'protocolName': 'Illumina Nextera XT NGS Prep 2: Clean-Up Libraries',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.0'
    }


def run(protocol):
    [pip_type, pip_mount, no_of_samps, pcr_vol,
     bead_ratio, dry_time] = get_values(  # noqa: F821
    'pip_type', 'pip_mount', 'no_of_samps', 'pcr_vol',
    'bead_ratio', 'dry_time')

    # labware setup
    mag_deck = protocol.load_module('magdeck', '4')
    mag_plate = mag_deck.load_labware('biorad_96_wellplate_200ul_pcr')
    in_plate = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr', '5', 'Load Plate'
    )
    out_plate = protocol.load_labware(
        'biorad_96_wellplate_200ul_pcr', '1', 'Final Plate (empty)'
    )
    trough = protocol.load_labware(
        'usascientific_12_reservoir_22ml', '2', 'Reservoir, 12-channel'
    )
    # reagent setup
    rsb = trough['A1']  # resuspension buffer
    beads = trough['A2']  # AMPure XP beads
    ethanol = trough['A3']  # 80% ethanol
    liquid_trash = trough['A12'].top()

    tip_no = no_of_samps * 4 + 3
    no_racks = tip_no//96 + (1 if tip_no % 96 > 0 else 0)
    tips = [
        protocol.load_labware('opentrons_96_tiprack_300ul', str(slot))
        for slot in range(6, 7+no_racks)
    ]

    pip = protocol.load_instrument(pip_type, pip_mount, tip_racks=tips)

    if no_of_samps <= 24:
        inputs = [well
                  for col in in_plate.columns()[:6]
                  for well in col[:4]][:no_of_samps]
        mag = [well
               for col in mag_plate.columns()[:6]
               for well in col[:4]][:no_of_samps]
        outputs = [well
                   for col in out_plate.columns()[:6]
                   for well in col[:4]][:no_of_samps]
    else:
        inputs = [well for well in in_plate.wells()][:no_of_samps]
        mag = [well for well in mag_plate.wells()][:no_of_samps]
        outputs = [well for well in out_plate.wells()][:no_of_samps]

    bead_vol = pcr_vol*bead_ratio

    # Transfer PCR Product
    pip.transfer(pcr_vol, inputs, mag, new_tip='always')

    # Transfer beads to each well
    pip.distribute(bead_vol, beads, [well.top() for well in mag])

    total_vol = bead_vol + pcr_vol + 5

    protocol.pause("Shake at 1800 rpm for 2 minutes.")

    # Incubate at RT for 5 minutes
    protocol.delay(minutes=5)

    # Engage MagDeck for 2 minutes, remain engaged
    mag_deck.engage()
    protocol.delay(minutes=2)

    # Remove supernatant
    pip.transfer(total_vol, mag, liquid_trash, new_tip='always')

    # Wash beads twice with 80% ethanol
    for cycle in range(2):
        pip.transfer(200, ethanol, [well.top() for well in mag])
        protocol.delay(seconds=30)
        for well in mag:
            pip.transfer(220, well.top(), liquid_trash)

    # Air dry
    protocol.delay(minutes=dry_time)

    # Turn off MagDeck
    mag_deck.disengage()

    # Transfer RSB to well
    pip.transfer(52.5, rsb, [well.top() for well in mag])

    protocol.pause("Shake at 1800 rpm for 2 minutes.")

    # Turn on MagDeck for 2 minutes
    mag_deck.engage()
    protocol.delay(minutes=2)

    # Transfer supernatant to new PCR plate
    pip.transfer(50, mag, outputs, new_tip='always')

    # Disengage MagDeck
    mag_deck.disengage()
