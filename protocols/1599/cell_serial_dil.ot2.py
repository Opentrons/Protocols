from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Customizable Cell Culture Serial Dilution',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'Greiner-96-flat'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.96,
        depth=10.9,
        volume=350
    )

deep_name = 'USA-Scientific-PlateOne-96-deepwell'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=41.3,
        volume=2000
    )

tubes_name = 'Cellstar-15ml-3x5'
if tubes_name not in labware.list():
    labware.create(
        tubes_name,
        grid=(5, 3),
        spacing=(25, 25),
        diameter=7.58,
        depth=118.1,
        volume=15000
    )

tips50_name = 'TipOne-tiprack-50ul'
if tips50_name not in labware.list():
    labware.create(
        tips50_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60
    )

tips300_name = 'TipOne-tiprack-300ul'
if tips300_name not in labware.list():
    labware.create(
        tips300_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3.5,
        depth=60
    )

# load labware
tubes = labware.load(tubes_name, '2')
tips50 = labware.load(tips50_name, '4', '50ul tips')
tips300 = labware.load(tips300_name, '5', '300ul tips')

# pipettes
p50 = instruments.P50_Single(mount='right', tip_racks=[tips50])
p300 = instruments.P300_Single(mount='left', tip_racks=[tips300])


def run_custom_protocol(
        dilution_plate_type: StringSelection(
            'deepwell', 'standard') = 'standard',
        dilution_factor: float = 1.5,
        total_mixing_volume: float = 200.0,
        number_of_samples: int = 8,
        number_of_dilutions_per_sample: int = 11,
        dilution_start_well: str = 'A1',
        dilution_orientation: StringSelection(
            'vertical', 'horizontal') = 'horizontal',
        tip_use_strategy: StringSelection(
            'use one tip per sample',
            'new tip for each transfer') = 'use one tip per sample'
        ):

    # load specified dilution plate
    if dilution_plate_type == 'standard':
        dil_plate = labware.load(plate_name, '1')
    else:
        dil_plate = labware.load(deep_name, '1')

    # parse start well
    start_row = dilution_start_well.strip()[0]
    start_col = dilution_start_well.strip()[1:]

    row_names = 'ABCDEFGH'
    col_names = [str(num) for num in range(1, 13)]
    if start_row not in row_names or start_col not in col_names:
        raise Exception('Invalid start well.')

    # row: index dictionary
    letters = {}
    for ind, char in zip(range(8), row_names):
        letters[char] = ind

    # variables check
    start_row_ind = letters[start_row]
    if dilution_orientation == 'horizontal':
        col_used = int(start_col) + number_of_dilutions_per_sample
        if col_used > 12:
            raise Exception('Too many dilutions with specified start column.')
        if start_row_ind + number_of_samples > 8:
            raise Exception('Too many samples with specified start row')
    else:
        if start_row_ind + number_of_dilutions_per_sample >= 8:
            raise Exception('Too many dilutions with specified start row.')
        col_used = int(start_col) + number_of_samples
        if col_used > 13:
            raise Exception('Too many samples with specified start column.')

    # diluent height tracking function
    dil_height = -45
    v_out = 0

    def h_track(vol):
        nonlocal dil_height
        nonlocal v_out
        v_out += vol
        if v_out > 3500 and dil_height - 25 > -105:
            v_out = 0
            dil_height -= 25

    # setup sample tubes and initial heights
    diluent = tubes.wells('A1')
    liquid_trash = tubes.wells('B1').top()

    # Distribute diluent across the plate to the the number of samples
    # And add diluent to one column/row after the number of samples for a blank
    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    if dilution_orientation == 'horizontal':
        dil_start_ind = int(start_col)
        dil_end_ind = dil_start_ind + number_of_dilutions_per_sample

        d_dests = [
            well
            for col in dil_plate.columns()[dil_start_ind:dil_end_ind]
            for well in col[start_row_ind:start_row_ind+number_of_samples]
            ]
    else:
        dil_start_ind = start_row_ind + 1
        dil_end_ind = dil_start_ind + number_of_dilutions_per_sample

        d_dests = [
            well
            for row in dil_plate.rows()[dil_start_ind:dil_end_ind]
            for well in row[int(start_col)-1:
                            int(start_col)-1+number_of_samples]
        ]

    pipette = p300 if diluent_volume > 50 else p50
    pipette.pick_up_tip()
    for d in d_dests:
        h_track(diluent_volume)
        pipette.move_to(diluent.top())
        robot.head_speed(z=50, a=50)
        pipette.aspirate(diluent_volume, diluent.top(dil_height))
        robot.head_speed(z=125, a=125)
        pipette.dispense(diluent_volume, d.top())
        pipette.blow_out()
    pipette.drop_tip()

    # select pipette based on volume
    pipette = p300 if total_mixing_volume > 50 else p50

    # serially dilute according to input parameters
    if tip_use_strategy == 'use one tip per sample':
        new_tip = 'never'
    else:
        new_tip = 'always'

    if dilution_orientation == 'horizontal':
        for row in dil_plate.rows()[start_row_ind:
                                    start_row_ind+number_of_samples]:

            start_ind = int(start_col) - 1

            if new_tip == 'never':
                pipette.pick_up_tip()

            pipette.transfer(
                transfer_volume,
                row[start_ind:start_ind+number_of_dilutions_per_sample],
                row[start_ind+1:start_ind+number_of_dilutions_per_sample+1],
                mix_after=(3, total_mixing_volume / 2),
                new_tip=new_tip
                )

            pipette.transfer(
                transfer_volume,
                row[start_ind+number_of_dilutions_per_sample],
                liquid_trash,
                new_tip=new_tip
                )

            if new_tip == 'never':
                pipette.drop_tip()

    else:
        for col in dil_plate.columns()[
                int(start_col)-1:
                int(start_col)+number_of_samples-1
                ]:

            start_ind = start_row_ind
            end_ind = start_ind + number_of_dilutions_per_sample

            if new_tip == 'never':
                pipette.pick_up_tip()

            pipette.transfer(
                transfer_volume,
                col[start_ind:end_ind],
                col[start_ind+1:end_ind+1],
                mix_after=(3, total_mixing_volume / 2),
                new_tip=new_tip
                )

            pipette.transfer(
                transfer_volume,
                col[end_ind],
                liquid_trash,
                new_tip=new_tip
                )

            if new_tip == 'never':
                pipette.drop_tip()
