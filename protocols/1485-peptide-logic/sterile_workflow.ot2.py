from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Compound Serial Dilution',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

compound_plate_name = "corning-384-round-plate"
if compound_plate_name not in labware.list():
    labware.create(
        compound_plate_name,
        grid=(24, 16),
        spacing=(4.5, 4.5),
        diameter=3.6,
        depth=11.6)


# labware setup
compound_plate = labware.load(compound_plate_name, '1')
trough = labware.load('trough-12row', '5')

tiprack_300 = [labware.load('opentrons-tiprack-300ul', slot)
               for slot in ['10', '11']]
tiprack_50 = [labware.load('opentrons-tiprack-300ul', slot)
              for slot in ['6', '7', '8', '9']]

# instrument setup
m300 = instruments.P50_Multi(
    mount='left',
    tip_racks=tiprack_300)

m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=tiprack_50)

m300_tip_count = 0
m50_tip_count = 0


def update_m300_tip_count(col_num):
    global m300_tip_count
    m300_tip_count += col_num
    if m300_tip_count == len(tiprack_300) * 12:
        robot.pause("Your 10 uL tips have run out. Replenish the tip racks \
before resuming.")
        m300_tip_count = 0
        m300.reset_tip_tracking()


def update_multi_tip_count(col_num):
    global m50_tip_count
    m50_tip_count += col_num
    if m50_tip_count == len(tiprack_50) * 12:
        robot.pause("Your 300 uL tips have run out. Replenish the tip racks \
before resuming.")
        m50_tip_count = 0
        m50.reset_tip_tracking()


def run_custom_protocol(number_of_compounds: int=17):

    # reagent setup
    buffer = trough.wells('A1')

    dil_list = [row.wells(col_index, length=12) for col_index in ['1', '13']
                for row in compound_plate.rows('A', 'B')]

    if number_of_compounds == 17:
        dil_list = dil_list[:3]
    elif number_of_compounds < 17 and number_of_compounds > 1:
        dil_list = dil_list[:2]
    elif number_of_compounds == 1:
        dil_list = [dil_list[0]]

    # transfer 50 uL buffer
    m300.distribute(
        50, buffer, [col for row in dil_list for col in row[1:]])
    update_multi_tip_count(1)

    # perform serial dilutions
    for row in dil_list:
        for source, dest in zip(row[:11], row[1:]):
            m50.pick_up_tip()
            m50.transfer(25, source, dest, new_tip='never')
            m50.mix(3, 50, dest.bottom(2))
            m50.blow_out(dest.top())
            m50.drop_tip()
            update_multi_tip_count(1)
