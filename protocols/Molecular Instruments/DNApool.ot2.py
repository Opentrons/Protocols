from opentrons import labware, instruments

## CUSTOMIZATION
final_volume = 1500 
probe_num = [40, 5]
plate_loc = [4, 5]
sample_loc = [['A1', 'B1'], ['A2', 'B2']]


tiprack = labware.load('tiprack-200ul', 1)
target_rack = labware.load('tube-rack-2ml', 2)
diluent_rack = labware.load('tube-rack-15_50ml', 3)

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack]
    )

p300 = instruments.P300_Single(
    mount='right',
    tip_racks=[tiprack]
    )

probe_plate = []

for plate in plate_loc:
    new_plate = labware.load('96-flat', plate)
    probe_plate.append(new_plate)

info_list = list(zip(probe_plate, probe_num, sample_loc))


for each_plate in info_list:
    for sample in each_plate[2]:
        p300.pick_up_tip()
        if each_plate[1] > 12:
            p300.consolidate(30, each_plate[0].rows[0:(each_plate[1]//12)], target_rack[sample], new_tip='never')
        else:
            pass
        p300.consolidate(30, each_plate[0].rows[each_plate[1]//12][:each_plate[1]%12], target_rack[sample])
        p300.pick_up_tip()
        p300.transfer(final_volume - 30 * each_plate[1], diluent_rack['A1'], target_rack[sample], new_tip='never')
        p300.mix(10, 300, target_rack[sample])
        p300.drop_tip()
