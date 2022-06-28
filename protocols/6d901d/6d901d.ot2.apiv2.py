from opentrons import protocol_api
from opentrons.protocol_api.contexts import InstrumentContext

metadata = {
    'protocolName':
        ('Normalization with a multi-channel pipette used as a single-channel '
         'pipette'),
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.11'
    }

tiprack_slots = ['4', '5', '10', '11']


def transpose_matrix(m):
    return [[r[i] for r in reversed(m)] for i in range(len(m[0]))]


def flatten_matrix(m):
    """ Converts a matrix to a 1D array, e.g. [[1,2],[3,4]] -> [1,2,3,4]
    """
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


def run(ctx: protocol_api.ProtocolContext):

    [volumes_csv,
     pip_model,
     pip_mount,
     plate_type,
     res_type,
     filter_tip,
     tip_reuse] = get_values(  # noqa: F821
     "volumes_csv",
     "pip_model",
     "pip_mount",
     "plate_type",
     "res_type",
     "filter_tip",
     "tip_reuse")

    # create labware
    source_plate = ctx.load_labware(plate_type, '7')
    # There could be a destination plate in slot 8 for cherry picking
    # Load something tall so the pipette doesn't hit it
    ctx.load_labware('usascientific_96_wellplate_2.4ml_deep', '8')
    reservoir = ctx.load_labware(res_type, '9')
    source = reservoir.wells()[0]

    pip_size = pip_model.split('_')[0][1:]

    tip_name = 'opentrons_96_tiprack_'+pip_size+'ul'
    if filter_tip == 'yes':
        pip_size = '200' if pip_size == '300' else pip_size
        tip_name = 'opentrons_96_filtertiprack_'+pip_size+'ul'

    tipracks = [ctx.load_labware(tip_name, slot)
                for slot in tiprack_slots]

    pipette = ctx.load_instrument(
        pip_model, pip_mount, tip_racks=tipracks)

    if 'p20' in pip_model:
        pick_up_current = 0.15  # 150 mA for single tip
        ctx._implementation._hw_manager.hardware._attached_instruments[
          pipette._implementation.get_mount()].update_config_item(
          'pick_up_current', pick_up_current)

    # Tip_map has the columns reversed, pipette always picks up the
    # bottom-most tip in a given column until the column is depleted, and then
    # moves to the next column (from left to right).
    tip_map = []
    for rack in tipracks:
        tip_map.append(
            [[col for col in reversed(column)] for column in rack.columns()])
    # Flag at the end of each rack that is true if there are tips left
    for rack in tip_map:
        rack.append(True)

    def pick_up(pipette: InstrumentContext):
        """`pick_up()` will pause the ctx when all tip boxes are out of
        tips, prompting the user to replace all tip racks. Once tipracks are
        reset, the ctx will start picking up tips from the first tip
        box as defined in the slot order when assigning the labware definition
        for that tip box. `pick_up()` will track tips for both pipettes if
        applicable.

        :param pipette: The pipette desired to pick up tip
        as definited earlier in the ctx (e.g. p300, m20).
        """
        for rack in tip_map:
            # Check the flag to see if the rack is empty, then we don't loop
            # through that rack so that the algorithm executes faster.
            if rack[-1] is False:
                continue
            for column in rack[:-1]:
                for well in column:
                    if well.has_tip:
                        pipette.pick_up_tip(well)
                        if well.well_name == 'A12':  # last tip in the rack
                            rack[-1] = False
                        return

    # create volumes list
    volumes = [float(cell) for cell in well_csv_to_list(volumes_csv)]

    is_warning = False

    for vol in volumes:
        if vol < pipette.min_volume and vol > 1E-6:
            ctx.comment(
                'WARNING: volume {} is below pipette\'s minimum volume.'
                .format(vol))
            is_warning = True

    if is_warning:
        ctx.comment("\n")
        ctx.pause(
            "One or more minimum volume warnings were detected "
            "Do you wish to continue?\n")
    if tip_reuse == 'always':
        pick_up(pipette)

    for i, vol in enumerate(volumes):
        if tip_reuse == 'never':
            pick_up(pipette)
        pipette.aspirate(vol, source)
        pipette.dispense(vol, source_plate.wells()[i])
        if tip_reuse == 'never':
            pipette.drop_tip()
