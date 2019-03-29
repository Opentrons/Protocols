from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'First Amplification (Part 2/8)',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
tubes = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
samples_rack = labware.load('96-PCR-tall', '2')
index_plate = labware.load('PCR-strip-tall', '3')

# set up tip rack to accommodate single transfers with multi-channel pipette
tip_rack300 = labware.load('opentrons-tiprack-300ul', '7')
tips_temp = []
for row in range(7, -1, -1):
    tips_temp.append(tip_rack300.rows()[row])
tips = [well for row in tips_temp for well in row]
tip_counter = 0

# pipette
m50 = instruments.P50_Multi(
    mount='right'
)

# reagent setup
NLM = tubes.wells('A1')


def run_custom_protocol(
    number_of_samples: StringSelection('3', '4', '6', '8',
                                       '9', '12', '16') = '4'):
    global tip_counter

    # setup samples and mix indexes
    number_of_samples = int(number_of_samples)
    samples = samples_rack.wells('A4', length=number_of_samples)
    mix_indexes = index_plate.wells('A1', length=number_of_samples)

    # transfer mix indexes to corresponding samples
    for i, s in zip(mix_indexes, samples):
        m50.pick_up_tip(tips[tip_counter])
        m50.transfer(10, i, s, blow_out=True, new_tip='never')
        m50.drop_tip()
        tip_counter += 1

    # distribute NLM to samples and mix
    for s in samples:
        m50.pick_up_tip(tips[tip_counter])
        m50.transfer(20, NLM, s, disposal_vol=3, new_tip='never')
        m50.mix(10, 50, s)
        m50.drop_tip()
        tip_counter += 1
