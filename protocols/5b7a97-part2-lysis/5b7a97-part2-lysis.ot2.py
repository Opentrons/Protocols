from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'MagMAX Part 2/3: Lysis Loading',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tiprack = [labware.load('opentrons_96_tiprack_1000ul', slot,
                        'Opentrons 1000ul Tips') for slot in range(7, 10)]

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
reservoir = labware.load(res_name, '4', 'Trough (Nalgene 300mL)')

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


def run_custom_protocol(
        p1000Single_mount: StringSelection('right', 'left') = 'right',
        number_of_plates: int = 3,
        plate_fill: StringSelection('full', 'half') = 'full'
):
    # check for number of plates
    if number_of_plates > 3 or number_of_plates < 1:
        raise Exception("The 'Number Of Plates' parameter must be between 1 \
        and 3.")

    # plate creation
    sample_plates = []
    for i in range(number_of_plates):
        slotno = i+1
        sample_plates.append(labware.load(plate_name, slotno))

    if plate_fill == 'half':
        sample_plates = [plate.wells()[:48] for plate in sample_plates]

    # create pipette
    pip1000 = instruments.P1000_Single(mount=p1000Single_mount,
                                       tip_racks=tiprack)

    for plate in sample_plates:
        for i in plate:
            pip1000.pick_up_tip()
            pip1000.aspirate(700, reservoir)
            pip1000.dispense(700, i.top(-10))
            pip1000.blow_out(i.top())
            pip1000.drop_tip()
