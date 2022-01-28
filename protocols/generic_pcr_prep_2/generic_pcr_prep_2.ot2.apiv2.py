import math
from opentrons import protocol_api

metadata = {
    'protocolName': 'PCR Prep part 2',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library',
    'apiLevel': '2.2'
    }


def get_values(*names):
    import json
    _all_values = json.loads("""{ "number_of_samples":"80",
                                  "left_pipette_lname":"p300_multi_gen2",
                                  "right_pipette_lname":"p20_multi_gen2",
                                  "use_filter_tips_left": false,
                                  "use_filter_tips_right": false,
                                  "mastermix_volume":"18",
                                  "DNA_volume":"2",
                                  "twelve_well_reservoir_lname",
                                  "DNA_well_plate":"biorad_96_wellplate_200ul_pcr",
                                  "destination_well_plate":"biorad_96_wellplate_200ul_pcr",
                                  "DNA_well_plate_tmod",
                                  "dest_well_plate_tmod"}
                                  """)
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):
    [number_of_samples, left_pipette_lname, right_pipette_lname,
     mastermix_volume, use_filter_tips_left, use_filter_tips_right,
     DNA_volume, twelve_well_reservoir_lname, DNA_well_plate,
     destination_well_plate] \
      = get_values(  # noqa: F821
        "number_of_samples", "left_pipette_lname", 'right_pipette_lname',
        "use_filter_tips_left", "use_filter_tips_right",
        "mastermix_volume", "DNA_volume", "twelve_well_reservoir_lname",
        "DNA_well_plate", "destination_well_plate_lname"
     )

    # Error checking
    if not left_pipette and not right_pipette:
        raise Exception('You have to select at least 1 pipette.')

    tiprack_l_slots = ['5', '6']
    tiprack_r_slots = ['7', '8']

    # load modules
    '''

    Add your modules here with:

    module_name = ctx.load_module('{module_loadname}', '{slot number}')

    Note: if you are loading a thermocycler, you do not need to specify
    a slot number - thermocyclers will always occupy slots 7, 8, 10, and 11.

    For all other modules, you can load them on slots 1, 3, 4, 6, 7, 9, 10.

    '''
    tmod_list = []
    for tmod_lname, slot in zip([DNA_well_plate_tmod, dest_well_plate_tmod],
                                [DNA_plate_slot, dest_plate_slot]):
        if tmod_lname:
            tmod = ctx.load_module(tmod_lname, slot)
            tmod_list.append(tmod)
        else:
            tmod_list.append(None)
    tmod_dna_plate, tmod_dest_plate = tmod_list
    '''

    Add your labware here with:

    labware_name = ctx.load_labware('{loadname}', '{slot number}')

    If loading labware on a module, you can load with:

    labware_name = module_name.load_labware('{loadname}')
    where module_name is defined above.

    '''
    # labware setup
    dna_plate = protocol_context.load_labware(
        DNA_well_plate, '1', 'DNA plate')
    dest_plate = protocol_context.load_labware(
        destination_well_plate, '2', 'Destination plate')
    res12 = protocol_context.load_labware(
        'usascientific_12_reservoir_22ml', '3', 'reservoir')
    # load tipracks
    '''

    Add your tipracks here as a list:

    For a single tip rack:

    tiprack_name = [ctx.load_labware('{loadname}', '{slot number}')]

    For multiple tip racks of the same type:

    tiprack_name = [ctx.load_labware('{loadname}', 'slot')
                     for slot in ['1', '2', '3']]

    If two different tipracks are on the deck, use convention:
    tiprack[number of microliters]
    e.g. tiprack10, tiprack20, tiprack200, tiprack300, tiprack1000

    '''

    tiprack_lnames = {
        "p20s_filtered": "opentrons_96_filtertiprack_20ul",
        "p20s_nonfiltered": "opentrons_96_tiprack_20ul",
        "p300s_filtered": "opentrons_96_filtertiprack_200ul",
        "p300s_nonfiltered": "opentrons_96_tiprack_300ul",
        "p1000s_filtered": "opentrons_96_filtertiprack_1000ul",
        "p1000s_nonfiltered": "opentrons_96_tiprack_1000ul"
    }

    tipracks = []
    for pip_lname, is_filtered, slot in zip([left_pipette_lname,
                                            right_pipette_lname],
                                            [use_filter_tips_left,
                                             use_filter_tips_right],
                                            [tiprack_l_slots,
                                             tiprack_r_slots]):
        if "20_" in pip_lname:
            if is_filtered:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p20s_filtered"], slot))
            else:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p20s_nonfiltered"], slot))
        elif "300_" in pip_lname:
            if is_filtered:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p300s_filtered"], slot))
            else:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p300s_nonfiltered"],
                                     slot))
        elif "1000_" in pip_lname:
            if is_filtered:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p100s_filtered"], slot))
            else:
                tipracks.append(
                    ctx.load_labware(tiprack_lnames["p1000s_nonfiltered"],
                                     slot))
        else:
            tipracks.append(None)
    tiprack_l, tiprack_r = tipracks

    pipette_l = None
    pipette_r = None

    for pip, mount, slots in zip(
            [left_pipette, right_pipette],
            ['left', 'right'],
            [['5', '6'], ['7', '8']]):

        if pip:
            range = pip.split('_')[0][1:]
            rack = 'opentrons_96_tiprack_' + range + 'ul'
            tipracks = [
                protocol_context.load_labware(rack, slot) for slot in slots]
            if mount == 'left':
                pipette_l = protocol_context.load_instrument(
                    pip, mount, tip_racks=tipracks)
            else:
                pipette_r = protocol_context.load_instrument(
                    pip, mount, tip_racks=tipracks)

    # determine which pipette has the smaller volume range
    pip_s, pip_l = rank_pipettes(pipette_l, pipette_r)

    # reagent setup
    mastermix = res12.wells()[0]

    # Make sure we have a pipette that can handle the volume of mastermix
    # Ideally the smaller one
    pipette = pipette_selector(pip_s, pip_l, mastermix_volume)

    col_num = math.ceil(number_of_samples/8)

    protocol_context.comment("Transferring master mix")
    pipette.pick_up_tip()
    for dest in dest_plate.rows()[0][:col_num]:
        pipette.transfer(
            mastermix_volume,
            mastermix,
            dest,
            new_tip='never'
        )
        pipette.blow_out(mastermix.top())
    pipette.drop_tip()

    # Transfer DNA to the destination plate
    pipette = pipette_selector(pip_s, pip_l, DNA_volume)

    protocol_context.comment("Transferring DNA")
    for source, dest in zip(dna_plate.rows()[0][:col_num],
                            dest_plate.rows()[0][:col_num]):
        pipette.transfer(DNA_volume, source, dest)


def rank_pipettes(pipette_l, pipette_r):
    """
    Given two pipettes this function will return them in the order of smallest
    to largest. This function assumes that error checking for cases where
    no pipettes were loaded was already done.
    """
    if not pipette_l:
        return [pipette_r, pipette_r]
    elif not pipette_r:
        return [pipette_l, pipette_l]
    else:
        if pipette_l.max_volume <= pipette_r.max_volume:
            return [pipette_l, pipette_r]
        else:
            return [pipette_r, pipette_l]


def pipette_selector(small_pipette, large_pipette, volume):
    """
    This function will return the smallest volume pipette capable
    of handling the given volume parameter.
    """
    if small_pipette and large_pipette:
        if (volume <= small_pipette.max_volume
           and volume >= small_pipette.min_volume):
            return small_pipette
        elif (volume <= large_pipette.max_volume
              and volume >= large_pipette.min_volume):
            return large_pipette
        else:
            raise Exception(("There is no suitable pipette loaded for "
                             "pipetting a volume of {} uL").format(volume))
