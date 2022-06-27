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

tiprack_slots = ['1', '2', '10', '11']


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


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "volumes_csv":"20,0,12,20,18,20,17,14,20,12,20,18\\n20,20,20,20,20,20,20,20,20,16,20,20\\n20,12,12,20,12,20,12,20,18,18,12,20\\n20,0,20,20,0,20,0,20,20,20,20,20\\n12,0,0,20,20,20,20,13,12,20,20,13\\n20,20,20,20,12,17,20,20,20,0,14,20\\n20,20,20,0,13,20,12,20,13,19,20,19\\n20,20,20,17,20,20,20,0,15,20,19,13",
                                  "pip_model":"p20_single_gen2",
                                  "pip_mount":"right",
                                  "plate_type":"nest_96_wellplate_200ul_flat",
                                  "res_type":"nest_1_reservoir_195ml",
                                  "filter_tip":"no",
                                  "tip_reuse":"never"
                                  }
                                  """)  # noqa: E501 Do not report 'line too long' warnings
    return [_all_values[n] for n in names]


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
    plate = ctx.load_labware(plate_type, '4')

    reservoir = ctx.load_labware(res_type, '6')
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
        # REVIEW: Recommended pick up current for m300 per tip, but is it
        # suitable for a p20?
        pick_up_current = 0.1
        ctx._implementation._hw_manager.hardware._attached_instruments[
          pipette._implementation.get_mount()].update_config_item(
          'pick_up_current', pick_up_current)

    # Created a tip_map with the columns reversed pipette always picks up the
    # bottom-most tip in a given column.
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
        pipette.dispense(vol, plate.wells()[i])
        if tip_reuse == 'never':
            pipette.drop_tip()
