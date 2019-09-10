from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': '',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
galipot_name = 'galipot_small'
if galipot_name not in labware.list():
    labware.create(
        galipot_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=18,
        depth=50
    )

rack_name = '48_well_tuberack'
if rack_name not in labware.list():
    labware.create(
        rack_name,
        grid=(8, 6),
        spacing=(13.9, 13.9),
        diameter=8,
        depth=50,
        volume=2000
    )

example_csv = """1668,
1665,
1747,
1759,
1639
"""

# load labware
tipracks1000 = [
    labware.load('opentrons_96_tiprack_1000ul', slot) for slot in ['1', '2']]
te = labware.load(galipot_name, '3', '1X tris-EDTA buffer').wells(0)


def run_custom_protocol(
        p1000_mount: StringSelection('right', 'left') = 'right',
        volume_CSV: FileInput = example_csv
):
    # pipette
    p1000 = instruments.P1000_Single(mount=p1000_mount, tip_racks=tipracks1000)

    # parse
    volumes = [
        float(line.split(',')[0]) for line in volume_CSV.splitlines() if line]
    if len(volumes) > 48*9:
        raise Exception('Too many volumes (' + str(len(volumes)) + 'for deck.')

    # load tube tube racks
    num_tuberacks = math.ceil(len(volumes)/48)
    tuberacks = [
        labware.load(rack_name, slot, 'destination tuberack ' + str(i+1))
        for i, slot in enumerate(range(4, 12))][:num_tuberacks]
    all_tubes = [tube for rack in tuberacks for tube in rack.wells()]

    tip1000_count = 0
    tip1000_max = len(tipracks1000)*96

    def pick_up():
        nonlocal tip1000_count
        if tip1000_count > tip1000_max:
            robot.pause('Refill 1000ul tipracks before resuming.')
            p1000.reset()
            tip1000_count = 0
        tip1000_count += 1
        p1000.pick_up_tip()

    # perform dilution transfer
    for i, (vol, dest) in enumerate(zip(volumes, all_tubes)):
        if i == 0:
            pick_up()
            p1000.move_to(dest.top())
            robot.comment('Ensure pipette tip is centered and flush with the \
opening of tube A1 of tuberack 1. Cancel run if not.')
            p1000.delay(seconds=10)
        # determine offset for dispense
        offset = -10 if vol >= 1800 else -20
        num_transfers = math.ceil(vol/1000)
        v_per_trans = vol/num_transfers
        for _ in range(num_transfers):
            if not p1000.tip_attached:
                pick_up()
            p1000.transfer(v_per_trans, te, dest.top(offset), new_tip='never')
            p1000.blow_out()
            p1000.drop_tip()
