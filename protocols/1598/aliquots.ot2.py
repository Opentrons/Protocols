from opentrons import labware, instruments, robot
import math

metadata = {
    'protocolName': 'Biological Aliquots Transfer',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
rack_name = 'Sarstedt-500ul-3x6'
if rack_name not in labware.list():
    labware.create(
        rack_name,
        grid=(6, 3),
        spacing=(20.75, 25),
        diameter=10,
        depth=24,
        volume=500
    )

# load labware
dest_tuberacks = [labware.load(rack_name, slot, '500ul Tuberack ' + slot)
                  for slot in ['1', '2']]
reagent_tubes = labware.load('opentrons-tuberack-15_50ml', '3')
tips1000 = labware.load('tiprack-1000ul', '4')

# pipettes
p1000 = instruments.P1000_Single(mount='left', tip_racks=[tips1000])

# destination tubes
dest_tubes = [tube for rack in dest_tuberacks for tube in rack.wells()]

# reagents and height initializers
plasma = reagent_tubes.wells('A1')
serum = reagent_tubes.wells('A2')
csf1 = reagent_tubes.wells('A3')
csf2 = reagent_tubes.wells('A4')


def run_custom_protocol(
        volume_of_CSF_tube_1_in_ml: float = 20,
        volume_of_CSF_tube_2_in_ml: float = 20,
        volume_of_plasma_in_ml: float = 6,
        volume_of_serum_in_ml: float = 3
):
    # constants for tube radii
    r15 = 7.5
    r50 = 13.4

    # function to calculate initial heights for CSF based on input volume
    def calc_initial_15(vol):
        dh = -(16.9 - vol)*1000/(math.pi*(r15**2)) - 8
        return dh

    # function to calculate initial heights for plasma and serum based on input
    # volume
    def calc_initial_50(vol):
        dh = -(56.4 - vol)*1000/(math.pi*(r15**2)) - 14
        return dh

    # calculate initial heights of all reagents
    csf1_initial = calc_initial_50(volume_of_CSF_tube_1_in_ml)
    csf2_initial = calc_initial_50(volume_of_CSF_tube_2_in_ml)
    plasma_initial = calc_initial_15(volume_of_plasma_in_ml)
    serum_initial = calc_initial_15(volume_of_serum_in_ml)

    heights = {
        'csf1': csf1_initial,
        'csf2': csf2_initial,
        'plasma': plasma_initial,
        'serum': serum_initial
    }

    def height_track15(reagent, vol):
        nonlocal heights

        dh = vol/(math.pi*(r15**2))
        heights[reagent] -= dh

    def height_track50(reagent, vol):
        nonlocal heights

        dh = vol/(math.pi*(r50**2))
        heights[reagent] -= dh

    # transfer CSF1
    p1000.pick_up_tip()
    for tube in dest_tubes[:30]:
        height_track50('csf1', 500)
        h = heights['csf1']
        p1000.transfer(
            500,
            csf1.top(h),
            tube.top(),
            blow_out=True,
            new_tip='never'
        )
    p1000.drop_tip()
    robot.pause('Please replace tubes with 20 new tubes in slots 1 and 2. '
                'Fill down each column before moving across the row.')

    # transfer CSF2
    p1000.pick_up_tip()
    for tube in dest_tubes[:20]:
        height_track50('csf2', 250)
        h = heights['csf2']
        p1000.transfer(
            250,
            csf2.top(h),
            tube.top(),
            blow_out=True,
            new_tip='never'
        )
    p1000.drop_tip()
    robot.pause('Please replace tubes with 30 new tubes in slots 1 and 2. '
                'Fill down each column before moving across the row.')

    # transfer plasma
    p1000.pick_up_tip()
    for tube in dest_tubes[:30]:
        height_track15('plasma', 250)
        h = heights['plasma']
        p1000.transfer(
            250,
            plasma.top(h),
            tube.top(),
            blow_out=True,
            new_tip='never'
        )
    p1000.drop_tip()
    robot.pause('Please replace tubes with 15 new tubes in slot 1. Fill down '
                'each column before moving across the row.')

    # transfer serum
    p1000.pick_up_tip()
    for tube in dest_tubes[:15]:
        height_track15('serum', 250)
        h = heights['serum']
        p1000.transfer(
            250,
            serum.top(h),
            tube.top(),
            blow_out=True,
            new_tip='never'
        )
    p1000.drop_tip()
