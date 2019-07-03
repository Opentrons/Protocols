from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Dilution Part 2: Coliform and HPC 100, 1000x',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'SPL-culture-6'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(3, 2),
        spacing=(41.1, 41.1),
        diameter=35,
        depth=19,
        volume=15000
    )

# load labware
plate = labware.load(plate_name, '1')
tubes = labware.load('opentrons-tuberack-15ml', '2')
tips1000 = labware.load('tiprack-1000ul', '4')

# pipettes
p1000 = instruments.P1000_Single(mount='right', tip_racks=[tips1000])

# reagents
mix_tubes = tubes.columns('1')[0:3]
pbs_tubes = tubes.columns('2')[0:3]
coliform_hpc = tubes.wells('C1')

# variables for height tracking 15 ml tubes
r_cyl = 7.52
heights = {
    'mix_tube1': -42,
    'mix_tube2': -42,
    'mix_tube3': -42,
    'pbs1': -42,
    'pbs2': -42,
    'pbs3': -42,
    'coliform_hpc': -42
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

# transfer coliform HPC reagent
p1000.pick_up_tip()
height_track('coliform_hpc', 1000)
h = heights['coliform_hpc']
p1000.transfer(
    1000,
    coliform_hpc.top(h),
    mix_tubes[0].top(),
    blow_out=True,
    new_tip='never'
    )
p1000.mix(5, 1000, mix_tubes[0])
p1000.drop_tip()

# dilute 100x
p1000.pick_up_tip()
height_track('mix_tube1', 1000)
h = heights['mix_tube1']
p1000.transfer(
    1000,
    mix_tubes[0].top(h),
    mix_tubes[1].top(),
    blow_out=True,
    new_tip='never'
    )
p1000.mix(5, 1000, mix_tubes[1])
for well in plate.rows('A'):
    height_track('mix_tube2', 500)
    h = heights['mix_tube2']
    p1000.transfer(
        500,
        mix_tubes[1].top(h),
        well.top(),
        blow_out=True,
        new_tip='never'
    )
p1000.drop_tip()

# dilute 1000x
p1000.pick_up_tip()
height_track('mix_tube2', 1000)
h = heights['mix_tube2']
p1000.transfer(
    1000,
    mix_tubes[1].top(h),
    mix_tubes[2].top(),
    blow_out=True,
    new_tip='never'
    )
p1000.mix(5, 1000, mix_tubes[2])
for well in plate.rows('B'):
    height_track('mix_tube3', 500)
    h = heights['mix_tube3']
    p1000.transfer(
        1000,
        mix_tubes[2].top(h),
        well.top(),
        blow_out=True,
        new_tip='never'
    )
p1000.drop_tip()
