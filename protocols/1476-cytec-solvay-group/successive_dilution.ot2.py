from opentrons import labware, instruments

metadata = {
    'protocolName': 'Successive Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

trough_A_name = 'wheaton-glass-dish'
if trough_A_name not in labware.list():
    labware.create(
        trough_A_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=76,
        depth=64)

tube_b_name = 'wheaton-serum-bottle-30-ml'
if tube_b_name not in labware.list():
    labware.create(
        tube_b_name,
        grid=(4, 2),
        spacing=(29.1, 34.5),
        diameter=25,
        depth=92)

# labware setup
a_rack = labware.load(trough_A_name, '7')
b_racks = [labware.load(tube_b_name, slot)
           for slot in ['3', '6']]
c_racks = [labware.load('opentrons-tuberack-15ml', slot)
           for slot in ['1', '2', '4', '5']]
tipracks = [labware.load('tiprack-1000ul', slot)
            for slot in ['8', '9', '10']]

# instruments setup
p1000 = instruments.P1000_Single(
    mount='left',
    tip_racks=tipracks)

# reagent setup
solution_a = a_rack.wells('A1')
solution_b = [well for rack in b_racks for well in rack]
solution_c = [well for rack in c_racks for well in rack][:48]


def run_custom_protocol(
        num_of_samples: int=2,
        num_of_dilutions: int=3,
        solution_A_volume: float=9000,
        dilution_volume: float=1000):

    # transfer solution A to C
    p1000.pick_up_tip()
    for well in solution_c[:num_of_samples * num_of_dilutions]:
        p1000.transfer(solution_A_volume, solution_a, well.top(),
                       blow_out=True, new_tip='never')
    p1000.drop_tip()

    # transfer solution B to C
    for index in range(num_of_samples):
        source_num = num_of_dilutions - 1
        sources = [solution_b[index]] + \
            solution_c[index * (source_num): (index+1) * (source_num)]
        dests = solution_c[
            index * num_of_dilutions: (index+1) * num_of_dilutions]
        p1000.pick_up_tip()
        for source, dest in zip(sources, dests):
            p1000.transfer(dilution_volume, source, dest, new_tip='never')
            p1000.mix(5, 1000)
        p1000.drop_tip()
