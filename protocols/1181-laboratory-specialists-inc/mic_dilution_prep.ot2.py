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
        dilution_num,
        dilution_loc):

    """
    Return the following lists:
    source_wells - locations of source well
    dil_wells - locations of dilution well
    source_vol - volumes of dilution source for each well
    buffer_vol - volumes of buffer for each well
    """
    prep_vol = 50 * 6 + 100  # Prepare more than enough volume for 6 replicates
    final_concs = [0] + [first_conc/(2**repeat)
                         for repeat in range(dilution_num)]
    initial_concs = [0, stock_conc]+final_concs[1:-1]
    dil_wells = [well for well in dilution_loc[1][:]+dilution_loc[0][::-1]]
    source_wells = [None, stock] + dil_wells[1:-1]

    buffer_vol = []
    source_vol = []

    for index, (conc1, conc2) in enumerate(zip(initial_concs, final_concs)):
        if index == 1:
            dest_vol = prep_vol * 2
        else:
            dest_vol = prep_vol
        vol = (dest_vol * conc2 / conc1 if conc1 > 0 else 0)
        source_vol.append(vol)
        buffer_vol.append(dest_vol - vol)

    return source_vol, buffer_vol, source_wells, dil_wells


def run_custom_protocol(
    stock_concentration: float=1600,
    initial_concentration: float=16,
    dilution_factor: float=2,
    dilution_start_column: int=1
        ):

    number_of_dilutions = 15
    dilution_loc = dilution_plate.cols(str(dilution_start_column), length=2)

    source_vol, buffer_vol, source_wells, dil_wells = \
        serial_dilution_calculations(
            stock_conc=stock_concentration,
            first_conc=initial_concentration,
            dilution_factor=dilution_factor,
            dilution_num=number_of_dilutions,
            dilution_loc=dilution_loc)

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
            m10.transfer(vol, source, dest, mix_after=(3, vol),
                         new_tip='never')
            m10.drop_tip()
        elif vol > 10:
            if not m300.tip_attached:
                m300.pick_up_tip(tiprack300.wells('G2'))
            m300.transfer(vol, source, dest, mix_after=(3, vol/2),
                          new_tip='never')
    m300.drop_tip()

    """
    Transfer serial dilutions to new plate
    """
    m300.start_at_tip(tiprack300.cols('3'))
    # transfer serial dilution to plate
    m300.distribute(50, dilution_loc[0], plate.cols[::2], disposal_vol=10)
    m300.distribute(50, dilution_loc[1], plate.cols[1::2], disposal_vol=10)
