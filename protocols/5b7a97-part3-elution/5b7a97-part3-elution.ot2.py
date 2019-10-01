from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'MagMAX Part 3/3: Elution Transfer',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

tiprack = [labware.load('opentrons_96_tiprack_300ul', slot,
                        'Opentrons 300ul Tips') for slot in range(7, 10)]

pcr_name = 'qiagen_pcr_striprack'
if pcr_name not in labware.list():
    labware.create(
        pcr_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.0,
        depth=45.0,
        volume=1200
    )

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


def run_custom_protocol(
        p300Multi_mount: StringSelection('left', 'right') = 'left',
        number_of_plates: int = 1
):

    # check
    if number_of_plates > 3 or number_of_plates < 1:
        raise Exception("The 'Number Of Plates' parameter must be between 1 \
        and 3.")

    # create pipette
    pip300 = instruments.P300_Multi(mount=p300Multi_mount,
                                    tip_racks=tiprack)

    # create plates
    pcr_strips = []
    sample_plates = []

    for i in range(number_of_plates):
        pslot = i + 1
        pcr_strips.append(labware.load(pcr_name, pslot))
        sslot = i + 4
        sample_plates.append(labware.load(plate_name, sslot))

    sample_plates = [plate.rows('A') for plate in sample_plates]
    pcr_strips = [strip.rows('A') for strip in pcr_strips]

    for plate, strip in zip(sample_plates, pcr_strips):
        for p, s in zip(plate, strip):
            pip300.pick_up_tip()
            pip300.transfer(90, p, s, new_tip='never')
            pip300.blow_out(s.top())
            pip300.drop_tip()
