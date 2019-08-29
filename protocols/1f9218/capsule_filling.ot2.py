from opentrons import labware, instruments, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Capsule Filling',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
capsule_rack_name = 'milimoli_100_capsulerack'
if capsule_rack_name not in labware.list():
    labware.create(
        capsule_rack_name,
        grid=(10, 10),
        spacing=(13, 13),
        diameter=2,
        depth=10,
        volume=500
    )

# load modules and labware
oil = labware.load('agilent_1_reservoir_290ml', '3', 'oil').wells(0)
tips1000 = labware.load('opentrons_96_tiprack_1000ul', '6')


def run_custom_protocol(
        p1000_mount: StringSelection('right', 'left') = 'right',
        number_of_capsules_to_fill: int = 100,
        volume_to_fill_in_ul: float = 200
):
    # check
    if volume_to_fill_in_ul < 100:
        raise Exception('Invalid volume for P1000 pipette')

    # load capsule plates
    slots = ['4', '10'] if number_of_capsules_to_fill > 100 else ['4']
    capsule_racks = [
        labware.load(capsule_rack_name, slot, 'capsules') for slot in slots]

    # pipette
    p1000 = instruments.P1000_Single(mount=p1000_mount, tip_racks=[tips1000])
    p1000.set_flow_rate(aspirate=100)

    max_vol = oil.properties['total-liquid-volume']*0.9
    total_vol = 0

    x = 108.00
    y = 72.00
    h = -10

    def height_track():
        nonlocal h
        dh = (volume_to_fill_in_ul/(x*y))+0.01
        h = h - dh if h - dh > -37 else -37

    def vol_track():
        nonlocal total_vol
        nonlocal h
        total_vol += volume_to_fill_in_ul
        if total_vol > max_vol:
            robot.pause('Refill oil reservoir before resuming.')
            total_vol = volume_to_fill_in_ul
            h = -10

    def oil_transfer(dest):
        height_track()
        vol_track()
        p1000.aspirate(volume_to_fill_in_ul, oil.top(h))
        p1000.delay(seconds=5)
        p1000.dispense(volume_to_fill_in_ul, dest.top(-1))
        p1000.blow_out(dest.top(-1))

    caps_left = number_of_capsules_to_fill
    caps_on_deck = len(capsule_racks)*100
    num_fills = math.ceil(caps_left/caps_on_deck)
    capsules = [well for plate in capsule_racks for well in plate.wells()]

    for r in range(num_fills):
        num_caps_for_fill = caps_left if caps_left < 100 else 100
        p1000.pick_up_tip()
        for c in capsules[:num_caps_for_fill]:
            oil_transfer(c)
        p1000.drop_tip()

        if r < num_fills - 1:
            caps_left -= caps_on_deck
            robot.pause('Replace filled capsule plates with empty capsules \
before resuming. ' + str(num_fills-r-1) + ' fills remaining.')
