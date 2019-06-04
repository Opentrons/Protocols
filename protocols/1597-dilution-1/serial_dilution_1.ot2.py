from opentrons import labware, instruments
import math

metadata = {
    'protocolName': 'Dilution 1: Coliform and HPC 1, 10x',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'SPL-culture-6'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(3, 2),
        spacing=(24, 24),
        diameter=22,
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
mix_tube = tubes.wells('A1')
coliform_hpc = tubes.wells('A2')
pbs = tubes.wells('B2')

# variables for height tracking 15 ml tubes
r_cyl = 7.52
heights = {
    'mix_tube': -42,
    'coliform_hpc': -42,
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

# transfer coliform HPC reagent
p1000.pick_up_tip()
height_track('coliform_hpc', 1000)
h = heights['coliform_hpc']
p1000.transfer(
    1000,
    coliform_hpc.top(h),
    mix_tube.top(),
    blow_out=True,
    new_tip='never'
    )
for well in plate.rows('A'):
    height_track('coliform_hpc', 1000)
    h = heights['coliform_hpc']
    p1000.transfer(
        1000,
        coliform_hpc.top(h),
        well.top(),
        blow_out=True,
        new_tip='never'
    )
p1000.drop_tip()

# transfer diluted solution
p1000.pick_up_tip()
height_track('mix_tube', 1000)
h = heights['mix_tube']
p1000.mix(5, 1000, mix_tube.top(h))
p1000.transfer(
    500,
    mix_tube.top(h),
    plate.wells('B1'),
    blow_out=True,
    new_tip='never'
    )
for well in ['B2', 'B3']:
    dest = plate.wells(well)
    height_track('mix_tube', 500)
    h = heights['mix_tube']
    p1000.transfer(
        1000,
        mix_tube.top(h),
        dest.top(),
        blow_out=True,
        new_tip='never'
    )
p1000.drop_tip()
