from opentrons import labware, instruments, modules, robot

"""
Clean Up Libraries
"""
# labware setup
mag_deck = modules.load('magdeck', '4')
# mag_plate = labware.load('96-PCR-flat', '4', share=True)
mag_plate = labware.load('biorad-hardshell-96-PCR', '4', share=True)
in_plate = labware.load('96-PCR-flat', '5')
out_plate = labware.load('96-PCR-flat', '1')
# out_plate = labware.load('biorad-hardshell-96-PCR', '2')
trough = labware.load('trough-12row', '2')
liquid_trash = trough.wells('A12')

# reagent setup
rsb = trough.wells('A1')  # resuspension buffer
beads = trough.wells('A2')  # AMPure XP beads
ethanol = trough.wells('A3')  # 80% ethanol

tipracks50 = [labware.load('tiprack-200ul', slot) for slot in ['6', '7', '8']]

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks50)


def run_custom_protocol(
        number_of_samples: int=24,
        PCR_product_volume: float=50,
        bead_ratio: float=1.8,
        dry_time: int=15
        ):

    if number_of_samples <= 24:
        inputs = [well
                  for col in in_plate.cols('1', to='6')
                  for well in col.wells('A', to='D')][:number_of_samples]
        mag = [well
               for col in mag_plate.cols('1', to='6')
               for well in col.wells('A', to='D')][:number_of_samples]
        outputs = [well
                   for col in out_plate.cols('1', to='6')
                   for well in col.wells('A', to='D')][:number_of_samples]
    else:
        inputs = [well for well in in_plate.wells()][:number_of_samples]
        mag = [well for well in mag_plate.wells()][:number_of_samples]
        outputs = [well for well in out_plate.wells()][:number_of_samples]

    bead_vol = PCR_product_volume*bead_ratio

    # Transfer PCR product
    p50.transfer(PCR_product_volume, inputs, mag, new_tip='always')

    # Transfer beads to each well
    p50.distribute(bead_vol, beads, [well.top() for well in mag])

    total_vol = bead_vol + PCR_product_volume + 5

    robot.pause("Shake at 1800 rpm for 2 minutes.")

    # Incubate at RT for 5 minutes
    p50.delay(minutes=5)

    # Engage MagDeck for 2 minutes, remain engaged
    mag_deck.engage()
    p50.delay(minutes=2)

    # Remove supernatant
    p50.transfer(total_vol, mag, liquid_trash, new_tip='always')

    # Wash beads twice with 80% ethanol
    for cycle in range(2):
        p50.transfer(200, ethanol, [well.top() for well in mag])
        p50.delay(seconds=30)
        for well in mag:
            p50.transfer(220, well.top(), liquid_trash)

    # Air dry
    p50.delay(minutes=dry_time)

    # Turn off MagDeck
    mag_deck.disengage()

    # Transfer RSB to well
    p50.transfer(52.5, rsb, [well.top() for well in mag])

    robot.pause("Shake at 1800 rpm for 2 minutes.")

    # Turn on MagDeck for 2 minutes
    mag_deck.engage()
    p50.delay(minutes=2)

    # Transfer supernatant to new PCR plate
    p50.transfer(50, mag_plate, outputs, new_tip='always')

    # Disengage MagDeck
    mag_deck.disengage()
