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
trough = labware.load('trough-12row', '1')
plate = labware.load(plate_name, '4')
petris = [labware.load(petri_dish_name, slot) for slot in ['5', '6']]
tuberack = labware.load('tube-rack-2ml', '7')
tips50 = labware.load('tiprack-200ul', '8')
tips10 = labware.load('tiprack-10ul', '9')

# pipettes
m50 = instruments.P50_Multi(
    mount='right',
    tip_racks=[tips50]
)

p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tips10]
)


def run_custom_protocol(number_of_samples: int = 12):
    # check for max 12 samples:
    if number_of_samples > 12:
        raise Exception('Cannot accommodate more than 12 samples.')

    # liquid setup
    buffer = trough.wells('A1')
    liquid_trash = trough.wells('A12')
    row_A = plate.rows('A')

    # fill plate with buffer
    m50.pick_up_tip()
    m50.transfer(90, buffer, row_A, new_tip='never')
    m50.drop_tip()

    # transfer up to 12 samples from tubes to plate
    samples = tuberack.wells('A1', length=number_of_samples)
    for tube, well in zip(samples, row_A):
        p10.transfer(10, tube, well)

    # serially dilute down each column from row A through row H
    for sample_ind, (sample, top) in enumerate(zip(samples, row_A)):
        p10.pick_up_tip()
        p10.transfer(10, sample, top, new_tip='never')
        col = plate.columns(sample_ind)
        for well_ind in range(7):
            source = col[well_ind]
            dest = col[well_ind+1]
            p10.transfer(10, source, dest, mix_before=(5, 10), new_tip='never')
        p10.mix(5, 10, col[7])
        p10.transfer(1, col[7], liquid_trash, new_tip='never')
        p10.drop_tip()

    # setup plate wells corresponding to desired petri dish output
    sources = [plate.wells('H'+str(col), to='C'+str(col))
               for col in range(1, number_of_samples+1)]
    dests = petris[0].rows() + petris[1].rows()

    # perform transfer in correct order
    for source_row, dest_col in zip(sources, dests):
        p10.pick_up_tip()
        for s, d in zip(source_row, dest_col):
            p10.transfer(10, s, d.bottom(3.2), blow_out=True, new_tip='never')
        p10.drop_tip()
