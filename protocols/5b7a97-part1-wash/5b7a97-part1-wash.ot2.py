from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'MagMAX Part 1/3: Customizable Processing Plate Filling',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tiprack = labware.load('opentrons_96_tiprack_300ul', '7',
                       'Opentrons 300ul Tips')

res_name = 'nalgene_1_reservoir_300ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=123.0,
        depth=36.6,
        volume=300000
    )
reservoir = labware.load(res_name, '8', 'Trough (Nalgene 300mL)')


def run_custom_protocol(
        p300Multi_mount: StringSelection('left', 'right') = 'left',
        plate_type: StringSelection(
            'Wash Solution 1',
            'Wash Solution 2',
            'Elution Buffer') = 'Wash Solution 1',
        plate_fill: StringSelection('Full', 'Half') = 'Full',
        number_of_plates: int = 6
):
    # check for number of plates
    if number_of_plates > 6 or number_of_plates < 1:
        raise Exception("The 'Number Of Plates' parameter must be between 1 \
        and 6.")

    # create pipette
    pip300 = instruments.P300_Multi(mount=p300Multi_mount, tip_racks=[tiprack])

    # create correct labware and transfer volume (trans_vol)
    if plate_type == 'Elution Buffer':
        plate_name = 'Kingfisher_96_wellplate_200ul_flat'
        if plate_name not in labware.list():
            labware.create(
                plate_name,
                grid=(12, 8),
                spacing=(9, 9),
                diameter=8.0,
                depth=12.8,
                volume=200
            )
        trans_vol = 90
    else:
        plate_name = 'Kingfisher_96_deepwellplate_2400ul'
        if plate_name not in labware.list():
            labware.create(
                plate_name,
                grid=(12, 8),
                spacing=(9, 9),
                diameter=8.3,
                depth=42.3,
                volume=2400
            )
        trans_vol = 500

    load_plates = []
    for i in range(number_of_plates):
        slotno = str(i + 1)
        load_plates.append(labware.load(plate_name, slotno))

    if plate_fill == 'Half':
        sam_plates = [plate.rows('A')[:6] for plate in load_plates]
    else:
        sam_plates = [plate.rows('A')[:] for plate in load_plates]

    pip300.pick_up_tip()
    for dest in sam_plates:
        for d in dest:
            pip300.transfer(trans_vol, reservoir, d, new_tip='never')
            pip300.blow_out(d.top())
    pip300.drop_tip()

    robot.comment('Congratulations. {}, {} plates have been filled with {}.'
                  .format(number_of_plates, plate_fill, plate_type))
