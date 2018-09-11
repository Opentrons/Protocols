from opentrons import labware, instruments

"""
Day 2: Drugging
"""

# labware setup
trough = labware.load('trough-12row', '1')
mix_plate = labware.load('96-deep-well', '2')
plate = labware.load('96-flat', '3')
tiprack1 = labware.load('tiprack-200ul', '4')
tiprack2 = labware.load('tiprack-200ul', '5')

# reagent
media = trough.wells('A3')

# pipette setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack1])

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack2])


def run_custom_protocol(
    column_for_serial_dilution: int=2,
    tiprack_start_column: int=2
        ):

    column = str(column_for_serial_dilution)

    # Define the tip start location
    m300.start_at_tip(tiprack1.cols(str(tiprack_start_column)))

    # Transfer media to the column for serial dilution in deep well plate
    m300.transfer(900, media, mix_plate.cols(column))

    p50.transfer(700, media, mix_plate.cols(column).wells('G'))

    p50.transfer(
        300,
        mix_plate.cols(column).wells('H'),
        mix_plate.cols(column).wells('G'))

    p50.pick_up_tip()
    p50.mix(10, 50, mix_plate.cols(column).wells('H'))
    p50.transfer(
        100,
        mix_plate.cols(column).wells('H'),
        mix_plate.cols(column).wells('F'),
        new_tip='never')
    p50.drop_tip()

    source_loc = mix_plate.cols(column).wells('G', to='D')
    dest_loc = mix_plate.cols(column).wells('E', to='B')

    p50.pick_up_tip()
    for source, dest in zip(source_loc, dest_loc):
        p50.mix(10, 50, source)
        p50.transfer(100, source, dest, new_tip='never')
    p50.drop_tip()

    source_well = [well for well in mix_plate.cols(column)]
    dest_row = [row for row in plate.rows()]

    # Transfer serial diluted drug to cells
    for source, dest in zip(source_well, dest_row):
        p50.distribute(20, source, dest, disposal_vol=0)
