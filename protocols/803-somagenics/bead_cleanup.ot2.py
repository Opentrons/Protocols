from opentrons import labware, instruments, modules

# labware setup
mag_deck = modules.load('magdeck', '2')
plate = labware.load('96-flat', '1')
pcr_strips = labware.load('96-PCR-flat', '2', share=True)
tuberack = labware.load('tube-rack-2ml', '4')
mag_beads = tuberack.wells('A1')
liquid_trash = labware.load('point', '7')

tiprack_1 = labware.load('tiprack-200ul', '5')
tiprack_2 = labware.load('tiprack-200ul', '6')

# pipette setup
p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack_1])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_2])


def run_custom_protocol(
    sample_number: int=10
        ):

    # number of sets of strip1-3 to use according to total number of sample
    cols = sample_number//8 + (1 if sample_number % 8 > 0 else 0)

    strips_1 = pcr_strips.cols[0::3][0:cols]
    strips_2 = pcr_strips.cols[1::3][0:cols]
    strips_3 = pcr_strips.cols[2::3][0:cols]

    sample_well = [well for col in strips_1 for well in col][0:sample_number]

    # transfer beads to all strip 1
    p300.transfer(20, mag_beads, sample_well,
                  mix_before=(3, 30), new_tip='always')

    # engage MagDeck
    mag_deck.engage()
    p300.delay(minutes=3)

    # remove solution from all stip 1
    for col in strips_1:
        m300.transfer(20, col.bottom(1), liquid_trash)

    # disengage MagDeck
    mag_deck.disengage()

    # transfer strips 1 to strip 2 in each set
    m300.transfer(23, strips_1, strips_2, mix_after=(3, 30), new_tip='always')

    p300.delay(minutes=10)

    # engage MagDeck
    mag_deck.engage()
    p300.delay(minutes=3)

    # transfer strips 2 to strips 3
    m300.transfer(21, strips_2, strips_3, new_tip='always')
