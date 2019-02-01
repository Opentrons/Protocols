from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Compound Serial Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
compound_plate = labware.load('384-plate', '1')
cell_plates = [labware.load('384-plate', slot)
               for slot in ['2', '3', '5', '6', '8', '9']]
trough = labware.load('trough-12row', '4')

tiprack_10 = [labware.load('tiprack-10ul', slot)
              for slot in ['10', '11']]
tiprack_50 = labware.load('opentrons-tiprack-300ul', '7')

# instrument setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=tiprack_10)

m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tiprack_50])

tip_count = 0


def update_single_tip_count(col_num):
    global tip_count
    tip_count += col_num
    print(tip_count)
    if tip_count == len(tiprack_10) * 96:
        robot.pause("Your 10 uL tips have run out. Replenish the tip racks \
before resuming.")
        tip_count = 0
        p10.reset_tip_tracking()
        print('update')


# reagent setup
buffer = trough.wells('A1')

number_of_compounds = 17

dil_list = [row.wells(col_index, length=12) for col_index in ['1', '13']
            for row in compound_plate.rows('A', 'B')]

if number_of_compounds == 17:
    dil_list = dil_list[:3]
elif number_of_compounds < 17:
    dil_list = dil_list[:2]

# transfer 50 uL buffer
m50.pick_up_tip()
for row in dil_list:
    for col in row[1:]:
        m50.transfer(50, buffer, col, new_tip='never')
        m50.blow_out(col.top())
m50.drop_tip()

# perform serial dilutions
for row in dil_list:
    m50.pick_up_tip()
    for source, dest in zip(row[:11], row[1:]):
        m50.transfer(25, source, dest, mix_after=(3, 50), new_tip='never')
    m50.drop_tip()

# tranfer 5 uL compound to cell plate in triplicate
compound_sources = [row.wells(col, length=12) for col in ['1', '13']
                    for row in compound_plate.rows()][:number_of_compounds]

compound_dests = []
for plate in cell_plates:
    for i in range(0, 15, 3):
        compound_dests.append(
            [row.wells(0, length=12) for row in plate.rows[i:i+3]])
    for i in range(1, 16, 3):
        compound_dests.append(
            [row.wells(13, length=12) for row in plate.rows[i:i+3]])

for source, dest in zip(compound_sources, compound_dests):
    for index, source_well in enumerate(source):
        dests = [dest[0][index], dest[1][index], dest[2][index]]
        p10.distribute(5, source_well, dests)
        update_single_tip_count(1)
