from opentrons import labware, instruments

metadata = {
    'protocolName': 'DNA Sample Dilution and PCR Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware
tuberack = labware.load('tube-rack-2ml', '1')
pcr_strips = labware.load('opentrons-aluminum-block-96-PCR-plate', '2')
tiprack_10 = labware.load('tiprack-10ul', '4')
tiprack_50 = labware.load('opentrons-tiprack-300ul', '5')

# custom PCR block with rack in right side
loading_block_r = 'mic-SBS-loading-block-right'
if loading_block_r not in labware.list():
    custom_plate = labware.create(
        loading_block_r,
        grid=(8, 6),
        spacing=(4.5, 9),
        diameter=4,
        depth=14,
        volume=200)
block = labware.load('mic-SBS-loading-block-right', '3')

# pipettes
m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_10]
)

p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50]
)

# reagent and strip setup
water = tuberack.wells('A1')
qPCR_mm = tuberack.wells('A2')
oligo1 = tuberack.wells('A3')
oligo2 = tuberack.wells('A4')
mix = tuberack.wells('A5')

strips = [strip for strip in pcr_strips.cols()]
strip_a = strips[0]
strip_b = strips[1]
strip_c = strips[2]
strip_d = strips[3]

# DNA sample dilution and mix
m10.transfer(2,
             strip_a[0],
             strip_c[0],
             blow_out=True,
             mix_after=(3, 10))
m10.transfer(2,
             strip_b[0],
             strip_d[0],
             blow_out=True,
             mix_after=(3, 10))


def run_custom_protocol(water_vol=4,
                        qPCR_mm_vol=7.5,
                        oligo1_vol=0.75,
                        oligo2_vol=0.75,
                        DNA_sample_vol=2):

    # create reaction mix for 52 samples (extra volume for 48 samples)
    p50.transfer(water_vol*52, water, mix.top(), mix_after=(3, 50))
    p50.transfer(qPCR_mm_vol*52, qPCR_mm, mix.top(), mix_after=(3, 50))
    p50.transfer(oligo1_vol*52, oligo1, mix.top(), mix_after=(3, 50))
    p50.transfer(oligo2_vol*52, oligo2, mix.top(), mix_after=(3, 50))

    # transfer composed mix to all 48 wells of right block rack
    total_mix_vol = water_vol + qPCR_mm_vol + oligo1_vol + oligo2_vol
    p50.transfer(total_mix_vol, mix.bottom(), block.wells(), blow_out=True)

    # transfer DNA samples from strips to block in specified order
    trans_order = [0, 2, 1, 3]
    for ind, well_num in enumerate(trans_order):
        origin = pcr_strips.rows['A'][well_num]
        dest1 = block.rows['A'][ind]
        dest2 = block.rows['A'][ind+4]
        m10.transfer(2, origin, dest1, blow_out=True, mix_after=(5, 5))
        m10.transfer(2, origin, dest2, blow_out=True, mix_after=(5, 5))
