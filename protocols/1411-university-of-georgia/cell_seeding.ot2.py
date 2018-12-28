from opentrons import labware, instruments

metadata = {
    'protocolName': 'Cell Seeding Protocol',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# create custom reservoir
reservoir_name = 'biotix-reservoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=72,
        depth=23
        )

# labware setup
tiprack = labware.load('opentrons-tiprack-300ul', '1', 'Tiprack')
cells = labware.load(reservoir_name, '2', 'Cells').wells('A1')

# instruments setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack])


def run_custom_protocol(
        number_of_plates: int=4,
        transfer_volume: float=70):

    if number_of_plates > 9:
        raise Exception('Number of plates cannot exceed 9.')

    transfer_volume = 70
    number_of_plates = 4
    plates = [labware.load('384-plate', str(slot), 'Plate '+str())
              for index, slot in enumerate(range(3, 3+number_of_plates), 1)]

    m300.pick_up_tip()
    for plate in plates:
        m300.mix(2, 300, cells)
        m300.aspirate(300, cells)
        for col in plate.cols():
            for index in range(2):
                if m300.current_volume <= transfer_volume:
                    m300.blow_out(cells)
                    m300.aspirate(300, cells)
                m300.dispense(transfer_volume, col[index])
        m300.blow_out(cells)
