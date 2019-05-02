from opentrons import labware, instruments

metadata = {
    'protocolName': 'Cell Culture Assay',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = '96-flat-culture'
if plate_name not in labware.list():
    labware.create(plate_name,
                   grid=(12, 8),
                   spacing=(9, 9),
                   diameter=6.42,
                   depth=11,
                   volume=330)

petri_dish_name = '6x6-petri-dish-square'
if petri_dish_name not in labware.list():
    labware.create(petri_dish_name,
                   grid=(6, 6),
                   spacing=(20, 20),
                   diameter=20,
                   depth=9,
                   volume=180)

# load labware
plates = [labware.load(plate_name, slot) for slot in ['8', '9']]
petris = [labware.load(petri_dish_name, slot)
          for slot in ['4', '5', '6', '10']]
tips10 = labware.load('tiprack-10ul', '11')

# pipettes
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tips10]
)

for i, plate in enumerate(plates):
    # setup plate wells corresponding to desired petri dish output
    sources = [plate.wells('H'+str(col), to='C'+str(col))
               for col in range(1, 13)]

    dests = petris[i*2].rows() + petris[i*2+1].rows()

    # perform transfer in correct order
    for source_row, dest_col in zip(sources, dests):
        p10.pick_up_tip()
        for s, d in zip(source_row, dest_col):
            p10.transfer(10, s, d.bottom(3.2), blow_out=True, new_tip='never')
        p10.drop_tip()
