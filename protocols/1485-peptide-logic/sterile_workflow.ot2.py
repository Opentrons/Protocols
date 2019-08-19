from opentrons import labware, instruments

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

tipracks = [labware.load('opentrons-tiprack-300ul', slot)
            for slot in ['6', '7', '8', '9', '10', '11']]


# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks)

m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=tipracks)


def run_custom_protocol(number_of_compounds: int=17):

    if number_of_compounds > 30:
        raise Exception("Number of compounds cannot exceed 30.")

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

    m50.start_at_tip(tipracks[0].cols('2'))

    # perform serial dilutions
    for row in dil_list:
        for source, dest in zip(row[:11], row[1:]):
            m50.pick_up_tip()
            m50.transfer(25, source, dest, new_tip='never')
            m50.mix(3, 50, dest.bottom(2))
            m50.blow_out(dest.top())
            m50.drop_tip()
