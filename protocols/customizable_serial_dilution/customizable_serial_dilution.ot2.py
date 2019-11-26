from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

trough = labware.load('usascientific_12_reservoir_22ml', '2')

liquid_trash = trough.wells('A12')


def run_custom_protocol(
    pipette_type: StringSelection(
        'p300-Single', 'p300-Multi', 'p50-Single', 'p50-Multi', 'p10-Single',
        'p10-Multi') = 'p300-Multi',
    labware_type: StringSelection(
        'Bio-Rad 96 Well Plate 200uL PCR',
        'Corning 12 Well Plate 6.9mL Flat',
        'Corning 24 Well Plate 3.4mL Flat',
        'Corning 384 Well Plate 112 uL Flat',
        'Corning 48 Well Plate 1.6 mL Flat',
        'Corning 6 Well Plate 16.8 mL Flat',
        'Corning 96 Well Plate 360 uL Flat',
        'USA Scientific 96 Deep Well Plate 2.4 mL') = 'Bio-Rad 96 Well \
        Plate 200uL PCR',
    dilution_factor: float = 3.0,
    number_of_dilution_plates: int = 1,
    num_of_dilutions: int = 10,
    total_mixing_volume: float = 150.0,
    tip_use_strategy: StringSelection(
        'use one tip', 'new tip each time') = 'use one tip'):

    # check plate number
    if number_of_dilution_plates > 8:
        raise Exception('Maximum of 8 dilution plates.')

    pip_name = pipette_type.split('-')[1]
    tip_name = pipette_type.split('-')[0]

    plate_names = [
        'biorad_96_wellplate_200ul_pcr',
        'corning_12_wellplate_6.9ml_flat',
        'corning_24_wellplate_3.4ml_flat',
        'corning_384_wellplate_112ul_flat',
        'corning_48_wellplate_1.6ml_flat',
        'corning_6_wellplate_16.8ml_flat',
        'corning_96_wellplate_360ul_flat',
        'usascientific_96_wellplate_2.4ml_deep'
    ]

    if labware_type == 'Corning 12 Well Plate 6.9mL Flat':
        plate_name = plate_names[1]
    elif labware_type == 'Corning 24 Well Plate 3.4mL Flat':
        plate_name = plate_names[2]
    elif labware_type == 'Corning 384 Well Plate 112 uL Flat':
        plate_name = plate_names[3]
    elif labware_type == 'Corning 48 Well Plate 1.6 mL Flat':
        plate_name = plate_names[4]
    elif labware_type == 'corning_6_wellplate_16.8ml_flat':
        plate_name = plate_names[5]
    elif labware_type == 'corning_96_wellplate_360ul_flat':
        plate_name = plate_names[6]
    elif labware_type == 'corning_96_wellplate_360ul_flat':
        plate_name = plate_names[7]
    else:
        plate_name = plate_names[0]
    plates = [
        labware.load(plate_name, slot, 'dilution plate ' + str(i+1))
        for i, slot in enumerate(
         ['3', '5', '6', '7', '8', '9', '10', '11'][:number_of_dilution_plates]
        )
    ]

    if tip_name == 'p300' or tip_name == 'p50':
        tiprack = [labware.load('opentrons_96_tiprack_300ul', slot)
                   for slot in ['1', '4']]
    elif tip_name == 'p10':
        tiprack = [labware.load('opentrons_96_tiprack_10ul', slot)
                   for slot in ['1', '4']]

    if pipette_type == 'p300-Single':
        pipette = instruments.P300_Single(
            mount='left',
            tip_racks=tiprack)
    elif pipette_type == 'p50-Single':
        pipette = instruments.P50_Single(
            mount='left',
            tip_racks=tiprack)
    elif pipette_type == 'p300-Multi':
        pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=tiprack)
    elif pipette_type == 'p50-Multi':
        pipette = instruments.P50_Multi(
            mount='left',
            tip_racks=tiprack)
    elif pipette_type == 'p10-Multi':
        pipette = instruments.P10_Multi(
            mount='left',
            tip_racks=tiprack)
    elif pipette_type == 'p10-Single':
        pipette = instruments.P10_Single(
            mount='left',
            tip_racks=tiprack)

    new_tip = 'never' if tip_use_strategy == 'use one tip' else 'always'

    transfer_volume = total_mixing_volume/dilution_factor
    buffer_volume = total_mixing_volume - transfer_volume

    tip_max = 12*len(tiprack) if pip_name == 'Multi' else 96*len(tiprack)
    tip_count = 0

    def pick_up():
        nonlocal tip_count
        if tip_count == tip_max:
            robot.pause('Replace tipracks in slots 1 and 4 before resuming.')
            pipette.reset()
            tip_count = 0
        pipette.pick_up_tip()
        tip_count += 1

    for p_i, plate in enumerate(plates):

        pick_up()

        if pip_name == 'Multi':

            # Distribute diluent across the plate to the the number of samples
            # And add diluent to one column after the number of samples for a
            # blank
            pipette.distribute(buffer_volume, trough.wells()[p_i], plate.cols(
                '2', length=(num_of_dilutions)), new_tip='never')

            # Dilution of samples across the 96-well flat bottom plate
            for s, d in zip(
                    plate.columns('1', to=(num_of_dilutions-1)),
                    plate.columns('2', to=num_of_dilutions)):
                if not pipette.tip_attached:
                    pick_up()
                pipette.transfer(
                    transfer_volume,
                    s,
                    d,
                    mix_after=(3, total_mixing_volume/2),
                    new_tip='never')
                if new_tip == 'always':
                    pipette.drop_tip()

            # Remove transfer volume from the last column of the dilution
            if not pipette.tip_attached:
                pick_up()
            pipette.transfer(
                transfer_volume,
                plate.columns(num_of_dilutions),
                liquid_trash,
                new_tip='never')

            pipette.drop_tip()

        else:
            # Distribute diluent across the plate to the the number of samples
            # And add diluent to one column after the number of samples for a
            # blank
            for col in plate.cols('2', length=(num_of_dilutions)):
                pipette.distribute(
                    buffer_volume, trough.wells()[p_i], col, new_tip='never')

            for row in plate.rows():
                for s, d in zip(
                        row.wells('1', to=(num_of_dilutions-1)),
                        row.wells('2', to=(num_of_dilutions))):

                    if not pipette.tip_attached:
                        pick_up()

                    pipette.transfer(
                        transfer_volume,
                        s,
                        d,
                        mix_after=(3, total_mixing_volume / 2),
                        new_tip='never')

                    if new_tip == 'always':
                        pipette.drop_tip()

                if not pipette.tip_attached:
                    pick_up()

                pipette.transfer(
                    transfer_volume,
                    row.wells(num_of_dilutions),
                    liquid_trash,
                    new_tip='never')

                if new_tip == 'always':
                    pipette.drop_tip()

            if pipette.tip_attached:
                pipette.drop_tip()
