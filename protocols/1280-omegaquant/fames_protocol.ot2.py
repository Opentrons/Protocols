from opentrons import labware, instruments

# labware setup
plate = labware.load('96-flat', '2')
trough1 = labware.load('trough-12row', '3')
trough2 = labware.load('trough-12row', '6')
tiprack = labware.load('opentrons-tiprack-300ul', '5')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])


def run_custom_protocol(
        number_of_samples: int=96,
        tip_start_column: str=2,
        trough_start_column: int=2):

    if number_of_samples >= 12:
        plate_loc = [col for col in plate.cols()]
    else:
        plate_loc = [col for col in plate.cols()][:number_of_samples]

    # uses well A2 in trough if more than 72 samples
    if number_of_samples > 72:
        wistd_loc = [trough1.wells(trough_start_column-1
                                   if col < 9 else trough_start_column)
                     for col in range(len(plate_loc))]
        water_loc = [trough2.wells(trough_start_column-1
                                   if col < 9 else trough_start_column)
                     for col in range(len(plate_loc))]
    else:
        wistd_loc = [trough1.wells(trough_start_column-1)
                     for col in range(len(plate_loc))]
        water_loc = [trough2.wells(trough_start_column-1)
                     for col in range(len(plate_loc))]

    m300.start_at_tip(tiprack.cols(tip_start_column))
    # transfer WISTD to wells
    m300.pick_up_tip()
    m300.mix(3, 300, wistd_loc[0])
    m300.blow_out(wistd_loc[0])
    for dest, source in zip(plate_loc, wistd_loc):
        m300.transfer(250, source, dest.top(), blow_out=True, new_tip='never')
    m300.drop_tip()

    # transfer water to wells
    m300.pick_up_tip()
    m300.mix(3, 300, water_loc[0])
    m300.blow_out(water_loc[0])
    for dest, source in zip(plate_loc, water_loc):
        m300.transfer(250, source, dest.top(), blow_out=True, new_tip='never')
    m300.drop_tip()
