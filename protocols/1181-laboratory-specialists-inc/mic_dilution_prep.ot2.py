from opentrons import labware, instruments

plate = labware.load('96-flat', '1')
trough = labware.load('trough-12row', '5')
dilution_plate = labware.load('96-deep-well', '4')

# reagent setup
buffer = trough.wells('A1')
stock = trough.wells('A2')

tiprack10 = labware.load('tiprack-10ul', '6')
tiprack300 = labware.load('tiprack-200ul', '7')

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack10])

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack300])


def serial_dilution_calculations(
        stock_conc,
        first_conc,
        dilution_factor,
        dilution_loc,
        vol_per_well
        ):
    """
    Return the following lists:
    source_wells - locations of source well
    dil_wells - locations of dilution well
    source_vol - volumes of dilution source for each well
    buffer_vol - volumes of buffer for each well
    """
    prep_vol = vol_per_well * 6 + 100  # Prepare more than enough vol for 6X
    dil_wells = [well for well in dilution_loc[1][:]+dilution_loc[0][::-1]]
    source_wells = [None, stock] + dil_wells[1:-1]
    buffer_vol = []
    source_vol = []
    for index in range(16):
        if index == 0:              # first well is control
            b_vol = prep_vol        # buffer volume == prep_vol
            s_vol = 0               # 0 uL stock volume
        elif index == 1:
            conc_1 = stock_conc
            conc_2 = first_conc
            first_prep_vol = prep_vol * (1 + 1/dilution_factor)
            s_vol = first_prep_vol * conc_2 / conc_1
            b_vol = first_prep_vol - s_vol
        else:
            conc_1 = first_conc / (dilution_factor ** (index-1))
            conc_2 = first_conc / (dilution_factor ** index)
            s_vol = prep_vol * conc_2 / conc_1
            b_vol = prep_vol
        buffer_vol.append(b_vol)
        source_vol.append(s_vol)
    return source_vol, buffer_vol, source_wells, dil_wells


def run_custom_protocol(
        stock_concentration: float=1600,
        initial_concentration: float=16,
        dilution_factor: float=2,
        dilution_start_column: int=1,
        final_volume_in_each_well: float=50):

    dilution_loc = dilution_plate.cols(str(dilution_start_column), length=2)

    source_vol, buffer_vol, source_wells, dil_wells = \
        serial_dilution_calculations(
            stock_conc=stock_concentration,
            first_conc=initial_concentration,
            dilution_factor=dilution_factor,
            dilution_loc=dilution_loc,
            vol_per_well=final_volume_in_each_well)

    """
    Transfer buffer for serial dilution wells
    """
    # transfer common volume of buffer to all dilution well
    m300.transfer(min(buffer_vol), buffer, dilution_loc)

    # transfer leftover volume to the rest of the wells
    leftover_buffer_vol = [vol-min(buffer_vol) for vol in buffer_vol]
    m300.pick_up_tip(tiprack300.wells('H2'))
    for vol, loc in zip(leftover_buffer_vol, dil_wells):
        if vol:
            m300.transfer(vol, buffer, loc, new_tip='never')
    m300.drop_tip()

    """
    Start serial dilutions
    """
    # perform serial dilution using one pipette tip
    for vol, source, dest in zip(source_vol, source_wells, dil_wells):
        if vol > 0 and vol <= 10:
            m10.pick_up_tip(tiprack10.wells('H1'))
            m10.transfer(vol, source, dest, mix_after=(6, vol),
                         new_tip='never')
            m10.drop_tip()
        elif vol > 10:
            if not m300.tip_attached:
                m300.pick_up_tip(tiprack300.wells('G2'))
            m300.transfer(vol, source, dest, mix_befor=(3, vol/2),
                          mix_after=(3, vol/2), new_tip='never')
    m300.drop_tip()

    """
    Transfer serial dilutions to new plate
    """
    m300.start_at_tip(tiprack300.cols('3'))
    # transfer serial dilution to plate
    m300.distribute(50, dilution_loc[0], plate.cols[::2], disposal_vol=10)
    m300.distribute(50, dilution_loc[1], plate.cols[1::2], disposal_vol=10)
