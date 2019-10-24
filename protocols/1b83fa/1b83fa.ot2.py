from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'Updated Cherrypicking with CSV',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

example_csv = """
A1, 20, A1
A3, 10, A3
B2, 70, B3

"""

white_plate = 'FisherBrand_White_Plate_05-408-210'
if white_plate not in labware.list():
    labware.create(
        white_plate,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.46,
        depth=16,
        volume=200
    )

color_plate = 'FisherBrand_Color_Plate_14-230-23X'
if color_plate not in labware.list():
    labware.create(
        color_plate,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.46,
        depth=20.2,
        volume=300
    )

thermo_plate = 'ThermoScientific_Plate_AB-0600-L'
if thermo_plate not in labware.list():
    labware.create(
        thermo_plate,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.46,
        depth=20.2,
        volume=300
    )


def run_custom_protocol(
        volumes_csv: FileInput = example_csv,
        left_pipette: StringSelection(
            'p10', 'p50', 'p300') = 'p10',
        right_pipette: StringSelection(
            'p300', 'p50', 'p10') = 'p300',
        source_plate_type: StringSelection(
            'FisherBrand_White_Plate_05-408-210',
            'FisherBrand_Color_Plate_14-230-23X',
            'ThermoScientific_Plate_AB-0600-L'
            ) = 'FisherBrand_White_Plate_05-408-210',
        destination_plate_type: StringSelection(
            'ThermoScientific_Plate_AB-0600-L',
            'FisherBrand_White_Plate_05-408-210',
            'FisherBrand_Color_Plate_14-230-23X',
            ) = 'ThermoScientific_Plate_AB-0600-L',
        tip_reuse: StringSelection(
            'new tip each time', 'reuse tip') = 'new tip each time',
        blowout: StringSelection('yes', 'no') = 'yes',
        touchTip: StringSelection('yes', 'no') = 'yes'
        ):

    if left_pipette == right_pipette:
        raise Exception('Pipettes should be of different types.')

    left_size = int(left_pipette[1:])
    right_size = int(right_pipette[1:])
    big_min = max(left_size, right_size)/10

    tips300 = labware.load('opentrons_96_tiprack_300ul', '1')
    t300count = 0
    sharetips = True

    if left_size == 10:
        pip_min = instruments.P10_Single(mount='left')
        tips10 = labware.load('opentrons_96_tiprack_10ul', '4')
        t10count = 0
        sharetips = False
        if right_size == 50:
            pip_max = instruments.P50_Single(mount='right')
        else:
            pip_max = instruments.P300_Single(mount='right')
    elif left_size == 300:
        pip_max = instruments.P300_Single(mount='left')
        if right_size == 50:
            pip_min = instruments.P50_Single(mount='right')
        else:
            pip_min = instruments.P10_Single(mount='right')
            tips10 = labware.load('opentrons_96_tiprack_10ul', '4')
            t10count = 0
            sharetips = False
    elif left_size == 50:
        if right_size == 300:
            pip_min = instruments.P50_Single(mount='left')
            pip_max = instruments.P300_Single(mount='right')
        else:
            pip_max = instruments.P50_Single(mount='left')
            pip_min = instruments.P10_Single(mount='right')
            tips10 = labware.load('opentrons_96_tiprack_10ul', '4')
            t10count = 0
            sharetips = False

    if sharetips is True:
        def tip_pick(pip):
            nonlocal t300count
            pip.pick_up_tip(tips300.wells(t300count))
            t300count += 1
    elif sharetips is False:
        def tip_pick(pip):
            nonlocal t10count
            nonlocal t300count
            if pip == pip_min:
                pip_min.pick_up_tip(tips10.wells(t10count))
                t10count += 1
            else:
                pip_max.pick_up_tip(tips300.wells(t300count))
                t300count += 1

    data = [
        [srcwell, float(vol), destwell.strip()]
        for srcwell, vol, destwell in
        [row.split(',') for row in volumes_csv.splitlines() if row]
        ]

    source_plate = labware.load(source_plate_type, '2')
    dest_plate = labware.load(destination_plate_type, '3')

    for src, vol, dest in data:
        if src and vol and dest:
            if vol < big_min:
                if not pip_min.tip_attached:
                    tip_pick(pip_min)
                pip_min.transfer(
                    vol,
                    source_plate.wells(src),
                    dest_plate.wells(dest),
                    new_tip='never')
                if touchTip == 'yes':
                    pip_min.touch_tip(dest_plate.wells(dest))
                if blowout == 'yes':
                    pip_min.blow_out(dest_plate.wells(dest))
                if tip_reuse == 'new tip each time':
                    pip_min.drop_tip()
            else:
                if not pip_max.tip_attached:
                    tip_pick(pip_max)
                pip_max.transfer(
                    vol,
                    source_plate.wells(src),
                    dest_plate.wells(dest),
                    new_tip='never')
                if touchTip == 'yes':
                    pip_max.touch_tip(dest_plate.wells(dest))
                if blowout == 'yes':
                    pip_max.blow_out(dest_plate.wells(dest))
                if tip_reuse == 'new tip each time':
                    pip_max.drop_tip()
    if pip_min.tip_attached:
        pip_min.drop_tip()
    if pip_max.tip_attached:
        pip_max.drop_tip()
