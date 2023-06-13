metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Krishna <krishna.soma@opentrons.com>',
    'apiLevel': '2.13'
}


def run(protocol):

    # modules
    tempdeck = protocol.load_module('temperature module gen2', '1')
    tempdeck.set_temperature(4)

    # labware
    reservoir = tempdeck.load_labware('nest_12_reservoir_15ml')
    pcr_plate = protocol.load_labware(
        'corning_96_wellplate_360ul_flat', '5')
    sample_plate = protocol.load_labware(
        'corning_96_wellplate_360ul_flat', '3', 'sample plate')

    tiprack300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
    tiprack20 = [protocol.load_labware('opentrons_96_tiprack_20ul', '4')]

    # pipettes
    m300 = protocol.load_instrument(
         'p300_multi_gen2', 'left', tip_racks=tiprack300)
    m20 = protocol.load_instrument(
         'p20_multi_gen2', 'right', tip_racks=tiprack20)

    # variables
    vol_mm = 23.0
    vol_sample = 2.0

    mm = reservoir.wells()[0]
    sample_sources = sample_plate.rows()[0]
    pcr_destinations = pcr_plate.rows()[0]

    # add mastermix with the same tip
    m300.transfer(vol_mm, mm, pcr_destinations)

    # add sample with fresh tips each time, and mix (2x)
    for s, d in zip(sample_sources, pcr_destinations):
        m20.transfer(vol_sample, s, d, mix_after=(2, 10))
