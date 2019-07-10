from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Dilution Part 4: MS2 100, 1000x',
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
e_coli = tubes.wells('B1')
pbs_tubes = tubes.rows('A')[2:5]
mix_tubes = [tube for tube in tubes.columns('2')]

# variables for height tracking 15 ml tubes
r_cyl = 7.52
heights = {
    'e_coli': -42,
    'mix_tube1': -42,
    'mix_tube2': -42,
    'mix_tube3': -42,
    'pbs1': -42,
    'pbs2': -42,
    'pbs3': -42,
    'ms2': -42
}


# 15 ml reagent height tracking function
def height_track(tube, vol):
    global heights

    # update height from which to aspirate
    dh = vol/(math.pi*(r_cyl**2))
    heights[tube] -= dh


# create 10x dilution
p1000.pick_up_tip()
for (ind, pbs, mix_tube) in zip(range(1, 4), pbs_tubes, mix_tubes):
    pbs_name = 'pbs' + str(ind)
    for _ in range(9):
        height_track(pbs_name, 1000)
        h = heights[pbs_name]
        p1000.transfer(
            1000,
            pbs.top(h),
            mix_tube.top(),
            new_tip='never',
            blow_out=True
            )
        p1000.blow_out(mix_tube.top())
p1000.drop_tip()

# distribute E. coli host to recipient tubes
p1000.pick_up_tip()
dests = [tube for row in ['B', 'C'] for tube in tubes.rows(row)[2:5]]
height_track('e_coli', 100*len(dests))
h = heights['e_coli']
p1000.distribute(
    100,
    e_coli,
    [tube.top() for tube in dests],
    disposal_vol=0
)

# transfer MS2 reagent
p1000.pick_up_tip()
height_track('ms2', 1000)
h = heights['ms2']
p1000.transfer(
    1000,
    ms2.top(h),
    mix_tubes[0].top(),
    blow_out=True,
    new_tip='never'
    )

height_track('mix_tube1', 1000)
h = heights['mix_tube1']
p1000.mix(5, 1000, mix_tubes[0])
p1000.transfer(
    1000,
    mix_tubes[0].top(h),
    mix_tubes[1].top(),
    blow_out=True,
    new_tip='never'
    )

height_track('mix_tube2', 1000)
h = heights['mix_tube2']
p1000.mix(5, 1000, mix_tubes[1])
for tube in tubes.wells('B3', 'B4'):
    p1000.transfer(
        500,
        mix_tubes[1].top(h),
        tube.top(),
        blow_out=True,
        new_tip='never')
height_track('mix_tube2', 500)
h = heights['mix_tube2']
p1000.transfer(
    500,
    mix_tubes[1].top(h),
    tubes.wells('B5'),
    blow_out=True,
    new_tip='never'
    )

# 1000x dilution
height_track('mix_tube2', 1000)
h = heights['mix_tube2']
p1000.transfer(
    1000,
    mix_tubes[1].top(h),
    mix_tubes[2].top(),
    blow_out=True,
    new_tip='never'
    )

height_track('mix_tube3', 1000)
h = heights['mix_tube3']
p1000.mix(5, 1000, mix_tubes[2])
for tube in tubes.wells('C3', 'C4'):
    p1000.transfer(
        500,
        mix_tubes[2].top(h),
        tube.top(),
        blow_out=True,
        new_tip='never')
height_track('mix_tube3', 500)
h = heights['mix_tube3']
p1000.transfer(
    500,
    mix_tubes[2].top(h),
    tubes.wells('C5'),
    blow_out=True,
    new_tip='never'
    )
p1000.drop_tip()
