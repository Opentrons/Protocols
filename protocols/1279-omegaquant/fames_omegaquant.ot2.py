from opentrons import labware, instruments

# labware setup
plate = labware.load('96-flat', '2')
trough = labware.load('trough-12row', '1')
tiprack = labware.load('opentrons-tiprack-300ul', '5')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
        number_of_samples: int=96):

    col_num = int(number_of_samples / 8 +
                  (1 if number_of_samples % 8 > 0 else 0))

    plate_loc = plate.cols()[:col_num]

    # uses well A2 in trough if more than 72 samples
    source_loc = [trough.wells(0 if col < 9 else 1) for col in range(col_num)]

    m300.pick_up_tip()
    m300.mix(3, 300, source_loc[0])
    m300.blow_out(source_loc[0])
    for dest, source in zip(plate_loc, source_loc):
        m300.transfer(250, source, dest.top(), blow_out=True, new_tip='never')
    m300.drop_tip()
