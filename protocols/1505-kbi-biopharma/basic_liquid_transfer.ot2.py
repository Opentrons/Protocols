from opentrons import labware, instruments
import math

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


def run_custom_protocol(number_of_samples: int = 48,
                        number_of_aliquots_per_source_well: int = 4,
                        volume_of_each_aliquot: float = 100.0):

    # volume check for p1000 pipette
    if volume_of_each_aliquot < 100:
        raise Exception("Specified volume not supported by p1000 pipette.")

    num_total_aliquots = number_of_samples*number_of_aliquots_per_source_well

    num_deep_well_plates = math.ceil(number_of_samples/24)
    num_tube_racks = math.ceil(num_total_aliquots/96)
    num_tip_racks = math.ceil(number_of_samples/96)

    # load appropriate number of each labware
    deep_plates = [labware.load('24-deep-well-plate', str(s+1))
                   for s in range(num_deep_well_plates)]

    tube_racks = [labware.load('1ml-tuberack', str(s+num_deep_well_plates+1))
                  for s in range(num_tube_racks)]

    tips1000 = [labware.load('tiprack-1000ul',
                str(s+num_deep_well_plates+num_tube_racks+1))
                for s in range(num_tip_racks)]

    # load pipette with tip racks attached
    p1000 = instruments.P1000_Single(mount='right', tip_racks=tips1000)

    # create continuous lists of source wells, destination wells, and tips
    all_sources = [well for plate in deep_plates
                   for well in plate.wells()][0:number_of_samples]

    all_dests = [tube for rack in tube_racks for tube in rack.wells()]
    dest_sets = []
    for s in range(number_of_samples):
        start = s*number_of_aliquots_per_source_well
        end = (s+1)*number_of_aliquots_per_source_well
        set = all_dests[start:end]
        dest_sets.append(set)

    # execute transfers
    for source, set in zip(all_sources, dest_sets):
        p1000.distribute(volume_of_each_aliquot,
                         source.bottom(2),
                         [tube.top(-2) for tube in set],
                         disposal_vol=p1000.min_volume/2)
