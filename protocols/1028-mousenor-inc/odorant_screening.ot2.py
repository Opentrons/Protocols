from opentrons import labware, instruments

sample_plate = labware.load('96-flat', '1')

elisa_plate = labware.load('96-flat', '2')

dilution_plate = labware.load('96-deep-well', '3')

trough = labware.load('trough-12row', '5')

liquid_trash = labware.load('point', '6').wells('A1')

# reagent setup
cAMP_standard = trough.wells('A1')
lysis_buffer = trough.wells('A2')
diluted_cAMP = trough.wells('A3')
antibody = trough.wells('A4')
substrate_solution = trough.wells('A5')
wash_buffer = trough.wells('A6')


tiprack50 = labware.load('tiprack-200ul', '4')
tiprack300s = [labware.load('tiprack-200ul', slot)
               for slot in ['7', '8', '9', '10']]


p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack50])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tiprack300s)


def run_custom_protocol(
        sample_source_col: str=3,
        sample_cols: int=2,
        sample_dest_col: str=5
        ):

    # create serial dilutions
    m300.transfer(270, lysis_buffer, dilution_plate.cols('1'))
    p50.transfer(30, lysis_buffer, dilution_plate.wells('H1'))
    p50.transfer(30, cAMP_standard, dilution_plate.wells('A1'),
                 mix_after=(3, 15))
    p50.transfer(
        30,
        dilution_plate.wells('A1', length=6),
        dilution_plate.wells('B1', length=6),
        mix_after=(3, 15))

    # transfer standards to ELISA plate
    m300.transfer(
        60,
        dilution_plate.cols('1'),
        [col for col in elisa_plate.cols('1', to='2')])

    # transfer samples to ELISA plate
    sample_source = sample_plate.cols(sample_source_col, length=sample_cols)
    sample_dest = elisa_plate.cols(sample_dest_col, length=sample_cols)
    m300.transfer(60, sample_source, sample_dest, new_tip='always')

    plate_loc = elisa_plate.cols('1', to='2')+sample_dest

    # transfer dilution cAMP-AP to plate
    m300.pick_up_tip()
    for col in plate_loc:
        m300.transfer(30, diluted_cAMP, col.top(), new_tip='never')
    m300.drop_tip()

    # transfer antibody to plate and mix
    for col in plate_loc:
        m300.transfer(60, antibody, col, mix_after=(3, 30))

    m300.delay(minutes=60)

    # remove solution from wells
    m300.transfer(150, plate_loc, liquid_trash, new_tip='always')

    # wash 6x with wash buffer
    for cycle in range(6):
        for col in plate_loc:
            m300.pick_up_tip()
            m300.transfer(200, wash_buffer, col, new_tip='never')
            m300.transfer(200, col, liquid_trash, new_tip='never')
            m300.drop_tip()

    # add substrate/enhancer solution to plate
    m300.pick_up_tip()
    for col in plate_loc:
        m300.transfer(100, substrate_solution, col.top(), new_tip='never')
    m300.drop_tip()
