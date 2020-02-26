metadata = {
    'protocolName': 'Normalization',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
    }

tiprack_slots = ['1', '4', '7', '10']


def transpose_matrix(m):
    return [[r[i] for r in reversed(m)] for i in range(len(m[0]))]


def flatten_matrix(m):
    return [cell for row in m for cell in row]


def well_csv_to_list(csv_string):
    """
    Takes a csv string and flattens it to a list, re-ordering to match
    Opentrons well order convention (A1, B1, C1, ..., A2, B2, B2, ...)
    """
    data = [
        line.split(',')
        for line in reversed(csv_string.split('\n')) if line.strip()
        if line
    ]
    if len(data[0]) > len(data):
        # row length > column length ==> "landscape", so transpose
        return flatten_matrix(transpose_matrix(data))
    # "portrait"
    return flatten_matrix(data)


def run(protocol):
    [volumes_csv, pip_model, pip_mount, plate_type,
     res_type, filter_tip, tip_reuse] = get_values(  # noqa: F821
        'volumes_csv', 'pip_model', 'pip_mount', 'plate_type',
         'res_type', 'filter_tip', 'tip_reuse')

    # create labware
    plate = protocol.load_labware(plate_type, '3')

    reservoir = protocol.load_labware(res_type, '2')
    source = reservoir.wells()[0]

    pip_size = pip_model.split('_')[0][1:]

    pip_size = '300' if pip_size == '50' else pip_size
    tip_name = 'opentrons_96_tiprack_'+pip_size+'ul'
    if filter_tip == 'yes':
        pip_size = '200' if pip_size == '300' else pip_size
        tip_name = 'opentrons_96_filtertippack_'+pip_size+'ul'
        if pip_size == '20':
            raise Exception('Filter tips are not yet supported on the P20.')

    tipracks = [protocol.load_labware(tip_name, slot)
                for slot in tiprack_slots]

    pipette = protocol.load_instrument(pip_model, pip_mount,
                                       tip_racks=tipracks)

    # create volumes list
    volumes = [float(cell) for cell in well_csv_to_list(volumes_csv)]

    for vol in volumes:
        if vol < pipette.min_volume:
            protocol.comment(
                'WARNING: volume {} is below pipette\'s minimum volume.'
                .format(vol))

    pipette.transfer(
        volumes,
        source,
        plate.wells()[:len(volumes)],  # added for simulation purposes
        new_tip=tip_reuse)
