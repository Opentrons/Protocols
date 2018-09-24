from opentrons import labware, instruments, modules, robot

"""
Normalize Libraries
"""
# labware setup
mag_deck = modules.load('magdeck', '4')
mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
in_plate = labware.load('96-PCR-flat', '5')
out_plate = labware.load('96-PCR-flat', '1')
tuberack = labware.load('tube-rack-2ml', '2')
trough = labware.load('trough-12row', '3')
liquid_trash = trough.wells('A12')


# reagent setup
LNA1 = tuberack.wells('A1')  # Library Normalization Additives 1
LNB1 = tuberack.wells('B1')  # Library Normalization Beads 1
LNW1 = tuberack.wells('C1')  # Library Normalization Wash 1
LNS1 = tuberack.wells('D1')  # Library Normalization Storage Buffer 1
NAOH = tuberack.wells('A2')  # 0.1 N NaOH

tipracks50 = [labware.load('tiprack-200ul', slot) for slot in ['6', '7']]
tipracks10 = [labware.load('tiprack-10ul', slot) for slot in ['8', '9']]

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks50)

p10 = instruments.P10_Single(
    mount='right',
    tip_racks=tipracks10)


def run_custom_protocol(
        number_of_samples: int=24,
        ):

    if number_of_samples <= 24:
        input = [well
                 for col in in_plate.cols('1', to='6')
                 for well in col.wells('A', to='D')][:number_of_samples]
        mag = [well
               for col in mag_plate.cols('1', to='6')
               for well in col.wells('A', to='D')][:number_of_samples]
        output = [well
                  for col in out_plate.cols('1', to='6')
                  for well in col.wells('A', to='D')][:number_of_samples]
    else:
        input = [well for well in in_plate.wells()][:number_of_samples]
        mag = [well for well in mag_plate.wells()][:number_of_samples]
        output = [well for well in out_plate.wells()][:number_of_samples]

    # Transfer 20 uL supernatant to new plate
    p50.transfer(20, input, mag, new_tip='always')

    # Transfer 44 uL LNA1 per sample to trough
    lna_vol = round(number_of_samples*1.05*44)
    p50.transfer(lna_vol, LNA1, trough.wells('A1'))

    # Transfer 8 uL LNB1 per sample to trough
    lnb_vol = round(number_of_samples*1.05*8)
    p50.pick_up_tip()
    p50.mix(5, 50, LNB1)
    p50.transfer(lnb_vol, LNB1, trough.wells('A1'), new_tip='never')
    p50.mix(10, 50, trough.wells('A1'))
    p50.drop_tip()

    # Transfer 45 uL combined LNA1 and LNB1 to each library
    p50.transfer(45, trough.wells('A1'), [well.top() for well in mag])

    robot.comment("Shake at 1800 rpm for 30 minutes. Place the plate back on \
        the MagDeck in slot 4.")

    robot.pause()

    # Turn on MagDeck for 2 minutes
    mag_deck.engage()
    p50.delay(minutes=2)

    # Remove supernatant from each well
    for well in mag:
        p50.transfer(65, well, liquid_trash)

    # Wash beads twice with LNW1
    for cycle in range(2):
        p50.transfer(45, LNW1, [well.top() for well in mag])
        robot.comment("Shake at 1800 rpm for 5 minutes. Place the plate back on \
            the MagDeck in slot 4.")
        robot.pause()
        for well in mag:
            p50.transfer(50, mag, liquid_trash)

    # Add 30 uL NaOH to each well
    p50.distribute(30, NAOH, [well.top() for well in mag])

    robot.comment("Shake at 1800 rpm for 5 minutes. Place the plate back on \
        the MagDeck in slot 4.")

    robot.pause()

    # Turn on MagDeck for 2 minutes
    mag_deck.engage()
    p50.delay(minutes=2)

    # Add 30 uL LNS1 to each well of a new plate
    p50.distribute(30, LNS1, [well.top() for well in output])

    # Add supernatant to new plate
    for well, dest in zip(mag, output):
        p50.transfer(60, well, dest)

    # Disengage MagDeck
    mag_deck.disengage()
