from opentrons import labware, instruments

metadata = {
    'protocolName': 'Cell Seeding Protocol',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
tiprack = labware.load('opentrons-tiprack-300ul', '1', 'Tiprack')

# instruments setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])


def run_custom_protocol(
        number_of_plates: int=4,
        transfer_volume: float=70):

    cells = labware.load('trough-12row', '2', 'Cells').wells('A1')

    if number_of_plates > 6:
        raise Exception('Number of plates cannot exceed 6.')

    plates = [labware.load('384-plate', str(slot), 'Plate '+str())
              for index, slot in enumerate(range(3, 3+number_of_plates), 1)]

    count = 0
    m300.pick_up_tip()
    m300.mix(2, 300, cells)
    for plate in plates:
        m300.aspirate(300, cells)
        for col in plate.cols():
            for index in range(2):
                if m300.current_volume <= transfer_volume:
                    m300.blow_out(cells)
                    m300.aspirate(300, cells)
                m300.dispense(transfer_volume, col[index])
            count += 1
            if count % 12 == 0 and not count // 24 == number_of_plates:
                m300.blow_out(cells)
                cells = next(cells)
                m300.mix(2, 300, cells)
        m300.blow_out(cells)
    m300.drop_tip()
