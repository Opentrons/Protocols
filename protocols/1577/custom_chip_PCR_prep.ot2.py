from opentrons import labware, instruments

metadata = {
    'protocolName': 'Custom Chip PCR Preparation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
chip_name = '3x8-chip'
if chip_name not in labware.list():
    labware.create(
        chip_name,
        grid=(8, 3),
        spacing=(9, 7.75),
        diameter=5,
        depth=0,
        volume=20
    )

strips_name = 'Tempassure-PCR-strips-200ul'
if strips_name not in labware.list():
    labware.create(
        strips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6,
        depth=20,
        volume=200
    )

# load labware
tubes = labware.load('opentrons-tuberack-2ml-eppendorf', '1', 'reagent tubes')
chip = labware.load(chip_name, '2')
strips = labware.load(strips_name,
                      '3',
                      'strips')
tips10 = labware.load('tiprack-10ul', '4')
tips50 = labware.load('opentrons-tiprack-300ul', '5')

# pipettes
p10 = instruments.P10_Single(mount='right', tip_racks=[tips10])
p50 = instruments.P50_Single(mount='left', tip_racks=[tips50])

# reagents
h2o = tubes.wells('A1')
red_buffer = tubes.wells('B1')
primer = tubes.wells('C1')
dna_pol = tubes.wells('D1')
mix_tube = tubes.wells('A2')

# create master mix, enough for 4 extra samples
p50.transfer(15.5*28, h2o, mix_tube.top(), blow_out=True)
p50.transfer(5*28, red_buffer, mix_tube.top(), blow_out=True)
p50.transfer(1*28, primer, mix_tube.top(), blow_out=True)
p50.pick_up_tip()
p50.transfer(0.25*28, dna_pol.bottom(), mix_tube, new_tip='never')
p50.mix(10, 50, mix_tube)
p50.drop_tip()

# set up spots
spots = [well for row in chip.rows() for well in row]
for i, spot in enumerate(spots[8:16]):
    offset = spot.from_center(r=0.8, theta=180, h=1.0)
    new = (spot, offset)
    spots[i] = new

# transfer sample to strips and immediately transfer water to membrane
sample_strips = strips.wells()[0:24]
for i, (spot, dest) in enumerate(zip(spot, sample_strips)):
    source = spot if i >= 8 and i < 16 else spot.top()
    p10.transfer(8, source, dest, blow_out=True)
    p10.transfer(10, h2o, spot.top(1))

# transfer master mix to new strip tubes
mix_strips = strips.wells()[24:48]
p50.transfer(21.75, mix_tube, mix_strips)

# transfer sample to corresponding strip tube already containing master mix
for source, dest in zip(sample_strips, mix_strips):
    p10.pick_up_tip()
    p10.transfer(3, source, dest, new_tip='never')
    p10.mix(10, 10, dest)
    p10.drop_tip()
