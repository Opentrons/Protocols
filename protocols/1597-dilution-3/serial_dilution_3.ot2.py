from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Dilution Part 3: MS2 1, 10x',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
tubes = labware.load('opentrons-tuberack-15ml', '1')
tips1000 = labware.load('tiprack-1000ul', '4')

# pipettes
p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips1000])

# reagents
ms2 = tubes.wells('A1')
pbs = tubes.wells('B1')
mix_tube = tubes.wells('C1')

# variables for height tracking 15 ml tubes
r_cyl = 7.52
heights = {
    'mix_tube': -42,
    'ms2': -42,
    'pbs': -42
}


# 15 ml reagent height tracking function
def height_track(tube, vol):
    global heights

    # update height from which to aspirate
    dh = vol/(math.pi*(r_cyl**2))
    heights[tube] -= dh


# create 10x dilution
p1000.pick_up_tip()
for _ in range(9):
    height_track('pbs', 1000)
    h = heights['pbs']
    p1000.transfer(
        1000,
        pbs.top(h),
        mix_tube.top(),
        new_tip='never',
        blow_out=True
        )
    p1000.blow_out(mix_tube.top())
p1000.drop_tip()

# transfer MS2 reagent
p1000.pick_up_tip()
for tube in tubes.rows('B')[1:4]:
    height_track('ms2', 1000)
    h = heights['ms2']
    p1000.transfer(
        1000,
        ms2.top(h),
        tube.top(),
        blow_out=True,
        new_tip='never'
        )
height_track('ms2', 1000)
h = heights['ms2']
p1000.transfer(
    1000,
    ms2.top(h),
    mix_tube.top(),
    new_tip='never',
    blow_out=True
    )

# mix and transfer diluted solution
height_track('mix_tube', 1000)
h = heights['mix_tube']
p1000.mix(5, 1000, mix_tube.top(h))
for tube in tubes.wells('C2', 'C3'):
    p1000.transfer(
        500,
        mix_tube.top(h),
        tube.top(),
        blow_out=True,
        new_tip='never'
        )
height_track('mix_tube', 500)
h = heights['mix_tube']
p1000.transfer(
    500,
    mix_tube.top(h),
    tubes.wells('C4').top(),
    blow_out=True,
    new_tip='never'
    )
p1000.drop_tip()
