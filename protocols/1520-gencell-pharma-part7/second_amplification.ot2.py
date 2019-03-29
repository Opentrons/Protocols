from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Second Amplification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
wash_rack = labware.load('96-PCR-tall', '1')
tube_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '2')

# set up tip rack to accommodate single transfers with multi-channel pipette
tip_rack50 = labware.load('opentrons-tiprack-300ul', '7')
tips_temp = []
for row in range(7, -1, -1):
    tips_temp.append(tip_rack50.rows()[row])
tips = [well for row in tips_temp for well in row]
tip_counter = 0

# pipettes
m50 = instruments.P50_Multi(
    mount='right',
)


def run_custom_protocol(
        number_of_samples: StringSelection('1', '2', '3', '4') = '4'):
    global tip_counter

    # reagent setup
    number_of_samples = int(number_of_samples)
    samples = wash_rack.wells('E6', length=number_of_samples)
    primers = tube_rack.wells('A1')
    NEM_mix = tube_rack.wells('A2')

    # distribute primers to samples
    m50.pick_up_tip(tips[tip_counter])
    m50.distribute(5, primers, [s.top() for s in samples], new_tip='never')
    m50.drop_tip()
    tip_counter += 1

    # distribute NLM to samples and mix
    for s in samples:
        m50.pick_up_tip(tips[tip_counter])
        m50.transfer(20, NEM_mix, s, new_tip='never')
        m50.mix(5, 40, s)
        m50.drop_tip()
        tip_counter += 1
