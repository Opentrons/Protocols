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
        number_of_samples: int=96,
        tip_start_column: str=1,
        trough_start_column: int=1):

    if number_of_samples >= 12:
        plate_loc = [col for col in plate.cols()]
    else:
        plate_loc = [col for col in plate.cols()][:number_of_samples]

    # uses well A2 in trough if more than 72 samples
    if number_of_samples > 72:
        source_loc = [trough.wells(trough_start_column-1
                                   if col < 9 else trough_start_column)
                      for col in range(len(plate_loc))]
    else:
        source_loc = [trough.wells(trough_start_column-1)
                      for col in range(len(plate_loc))]

    m300.start_at_tip(tiprack.cols(tip_start_column))
    m300.pick_up_tip()
    m300.mix(3, 300, source_loc[0])
    m300.blow_out(source_loc[0])
    for dest, source in zip(plate_loc, source_loc):
        m300.transfer(250, source, dest.top(), blow_out=True, new_tip='never')
    m300.drop_tip()
