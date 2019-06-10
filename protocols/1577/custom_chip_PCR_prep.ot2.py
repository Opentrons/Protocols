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


def run_custom_protocol(
        number_of_samples: int = 24
):
    # check for too many samples
    if number_of_samples > 24:
        raise Exception("24 sample membranes maximum on chip.")

    num_samples_for_mm = number_of_samples + 4

    # create master mix, enough for 4 extra samples
    p50.transfer(
        15.5*num_samples_for_mm,
        h2o,
        mix_tube.top(),
        blow_out=True
        )
    p50.transfer(
        5*num_samples_for_mm,
        red_buffer,
        mix_tube.top(),
        blow_out=True
        )
    if num_samples_for_mm > 10:
        p50.transfer(
            1*num_samples_for_mm,
            primer,
            mix_tube.top(),
            blow_out=True
            )

    p10.pick_up_tip()
    p10.transfer(
        0.25*num_samples_for_mm,
        dna_pol.bottom(),
        mix_tube,
        new_tip='never')
    p10.mix(10, 10, mix_tube)
    p10.blow_out(mix_tube.top())
    p10.drop_tip()

    # set up spots
    spots = [well for row in chip.rows() for well in row]
    for ind in range(8, 16):
        spot = spots[ind]
        offset = spot.from_center(r=0.8, theta=180, h=1.0)
        new = (spot, offset)
        spots[ind] = new
    spots = spots[0:number_of_samples]

    # slow flow rate and transfer sample to strips and immediately transfer
    # water to membrane
    p10.set_flow_rate(aspirate=2, dispense=2)
    sample_strips = strips.wells()[0:number_of_samples]
    for i, (spot, dest) in enumerate(zip(spots, sample_strips)):
        source = spot if i >= 8 and i < 16 else spot.top(1)
        p10.transfer(8, source, dest, blow_out=True)
        p10.transfer(10, h2o, source)

    # transfer master mix to new strip tubes
    mix_strips = strips.wells()[24:24+number_of_samples]
    p50.transfer(21.75, mix_tube, mix_strips)

    # reset flow rate to default and transfer sample to corresponding strip
    # tube already containing master mix
    p10.set_flow_rate(aspirate=5, dispense=10)
    for source, dest in zip(sample_strips, mix_strips):
        p10.pick_up_tip()
        p10.transfer(3, source, dest, new_tip='never')
        p10.mix(10, 10, dest)
        p10.drop_tip()
