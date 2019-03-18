from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Basic Liquid Transfer for Multiple Aliquots',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
trough_name = '24-deep-well-plate'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(6, 4),
        spacing=(18, 18),
        diameter=17,
        depth=43
    )

tube_rack_name = '1ml-tuberack'
if tube_rack_name not in labware.list():
    labware.create(
        tube_rack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.4,
        depth=44
    )

# load each labware
deep_plates = [labware.load('24-deep-well-plate', str(s+1))
               for s in range(4)]
tube_racks = [labware.load('1ml-tuberack', str(s+1)) for s in range(4, 9)]
tips1000 = [labware.load('tiprack-1000ul', str(s+1))
            for s in range(9, 11)]

# set up continuous list of wells across each type of labware
all_wells = [well for plate in deep_plates for well in plate]
all_tubes = [tube for rack in tube_racks for tube in rack]
all_tips = [tip for rack in tips1000 for tip in rack]

# load pipette with tip racks attached
p1000 = instruments.P1000_Single(mount='right', tip_racks=tips1000)

# setup total number of available wells, tubes, and tips
max_wells = len(all_wells)
max_tubes = len(all_tubes)
max_tips = len(all_tips)

# initialize global counters to check if a deck refill is necessary
well_count = 0
tube_count = 0
tip_count = 0


def run_custom_protocol(number_of_samples: int = 48,
                        number_of_aliquots_per_sample: int = 4,
                        volume_of_each_aliquot: float = 100.0):
    global well_count
    global tube_count
    global tip_count

    # volume check for p1000 pipette
    if volume_of_each_aliquot < 100:
        raise Exception("Specified volume not supported by p1000 pipette.")

    def check_wells():
        global well_count
        well_count += 1
        if well_count >= max_wells:
            robot.pause("Please refill deep-well plates before continuing.")
            well_count = 0

    def check_tubes(aliquots):
        global tube_count
        tube_count += aliquots
        if tube_count >= max_tubes:
            robot.pause("Please refill tuberacks before continuing.")
            tube_count = 0

    def check_tips():
        global tip_count
        tip_count += 1
        if tip_count >= max_tips:
            robot.pause("Please refill tipracks before continuing.")
            p1000.reset()

    # execute transfers
    for _ in range(number_of_samples):
        # check all labware to see if a refill is needed
        check_wells()
        check_tubes(number_of_aliquots_per_sample)
        check_tips()

        # execute transfer
        source = all_wells[well_count]
        dests = all_tubes[tube_count:tube_count+number_of_aliquots_per_sample]
        p1000.distribute(volume_of_each_aliquot,
                         source.bottom(2),
                         [dest.top(-2) for dest in dests],
                         disposal_vol=50)


run_custom_protocol()
