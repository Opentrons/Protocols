from opentrons import protocol_api
import re
from collections import Counter
from typing import Union

metadata = {
    'protocolName': 'Cherrypicking with multiple pipettes and modules',
    'author': 'Eskil Andersen <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.11'
}


def get_instruction_param_val(params_string: str, param_name: str):
    # Split the comma separated parameters string into individual parameters
    # Parameters are not case or leading/trailing ws sensitive
    params_string = params_string.strip().lower()
    params = params_string.split(',')
    param = ''
    for p in params:
        if param_name in p:
            param = p
            break
    # Return False if the parameter isn't in the instruction parameters
    if param == '':
        return False
    # Check if there's a value associated with the parameter
    if '=' in param:
        return param.split('=')[1]
    # Raise an exception if there's no associated value with the parameter
    else:
        err_msg = "There was no associated value with the parameter {}"
        err_msg = err_msg.format(param)
        raise Exception(err_msg)


def reply_to_bool(reply_string: str) -> Union[bool, None]:
    """ Takes a yes/no reply to a question in the form of a string and
    returns a True/False boolean value or None for blank entries.
    """

    reply_string = reply_string.strip().lower()
    if reply_string == "yes":
        return True
    if reply_string == "no":
        return False
    if reply_string == "":
        return None
    raise Exception("Unrecognized reply, should be yes or no")


def read_var(input: str, var_type: str):
    """
    Takes an input and checks if it is a blank string.
    If the string is blank it is returned as is, otherwise
    the function converts it to an int or a float depending on
    the value of var_type
    """

    if input == '':
        return input

    if var_type == "int":
        try:
            return int(input)
        except ValueError:
            err_msg = "Error converting the input '{}' to an integer"
            err_msg = err_msg.format(input)
            raise ValueError(err_msg)

    if var_type == "float":
        try:
            return float(input)
        except ValueError:
            err_msg = "Error converting the input '{}' to a float"
            err_msg = err_msg.format(input)
            raise ValueError(err_msg)

    err_msg = f"Unrecognized variable type argument: {var_type}"
    raise Exception(err_msg)


def get_values(*names):
    import json
    _all_values = json.loads("""{
                                  "transfer_csv":" step_id,instruction,instruction_parameters,source_labware,source_magnetic_module,source_temperature_module,source_slot,source_well,Source_well_starting_volume,transfer_volume,air_gap_volume,dest_labware,dest_magnetic_module,dest_temperature_module,dest_slot,dest_well,dest_well_starting_volume,touch_tip,blow_out\\n1,transfer,,nest_96_wellplate_2ml_deep,yes,no,1,A1,2000,1000,50,corning_6_wellplate_16.8ml_flat,no,no,3,A6,0,no,no\\n2,transfer,,corning_384_wellplate_112ul_flat,no,no,2,B1,100,90,10,nest_12_reservoir_15ml,no,no,4,B2,10,yes,yes\\n3,aspirate_and_park_tip,,corning_384_wellplate_112ul_flat,no,no,2,C1,100,50,10,,no,no,,,,,\\n4,pause,5m30s,,,,,,,,,,,,,,,,\\n5,dispense_parked_tip,step_id=3,,,,,,,60,,,,,,,,yes,yes\\n6,transfer,,corning_384_wellplate_112ul_flat,no,no,2,D1,100,20,0,corning_6_wellplate_16.8ml_flat,no,no,3,B6,10,yes,yes",
                                  "left_mount_pipette_type":"p20_single_gen2",
                                  "right_mount_pipette_type":"p300_single_gen2",
                                  "left_tip_type":"standard",
                                  "right_tip_type":"standard",
                                  "left_pip_tiprack_slots":"10,11",
                                  "right_pip_tiprack_slots":"5,8"
                                  }
                                  """)  # noqa: E501 Do not report 'line too long' warnings
    return [_all_values[n] for n in names]


def run(ctx: protocol_api.ProtocolContext):

    [transfer_csv,
     left_mount_pipette_type,
     right_mount_pipette_type,
     left_tip_type,
     right_tip_type,
     left_pip_tiprack_slots,
     right_pip_tiprack_slots] = get_values(  # noqa: F821
     "transfer_csv",
     "left_mount_pipette_type",
     "right_mount_pipette_type",
     "left_tip_type",
     "right_tip_type",
     "left_pip_tiprack_slots",
     "right_pip_tiprack_slots"
     )

    tiprack_map = {
        'p20_single_gen2': {
            'standard': 'opentrons_96_tiprack_20ul',
            'filter': 'opentrons_96_filtertiprack_20ul'
        },
        'p300_single_gen2': {
            'standard': 'opentrons_96_tiprack_300ul',
            'filter': 'opentrons_96_filtertiprack_200ul'
        },
        'p1000_single_gen2': {
            'standard': 'opentrons_96_tiprack_1000ul',
            'filter': 'opentrons_96_filtertiprack_1000ul'
        }
    }

    # Parameter validation
    valid_tiprack_string_regex = re.compile(
        r"^(10|11|[1-9])(,(10|11|[1-9]))*$")
    # regex for matching all kinds of whitespace
    whitespace_re = re.compile(r"\s+")
    # Validate tiprack strings, and create list of tiprack slots
    left_tiprack_slot_list, right_tiprack_slot_list = [], []
    for mount, tiprack_string, slot_list in zip(
            ["left", "right"],
            [left_pip_tiprack_slots, right_pip_tiprack_slots],
            [left_tiprack_slot_list, right_tiprack_slot_list]):
        # Remove all whitespaces in the string
        tiprack_string_no_ws = re.sub(whitespace_re, '', tiprack_string)
        # Check format validity
        if valid_tiprack_string_regex.match(tiprack_string_no_ws) is None:
            msg = ("The {} pipette tiprack slot list format is invalid, a "
                   "valid specification uses comma separated integers between "
                   "1-11 e.g. \"5, 6, 7\", your string was \"{}\"")
            msg = msg.format(mount, tiprack_string)
            raise Exception(msg)
        # Create a list of tiprack slots
        for slot in tiprack_string_no_ws.split(','):
            slot_list.append(int(slot))
        # Check for duplicates in the list
        if max(Counter(slot_list).values()) > 1:
            msg = "There are duplicates in the {} pipette tiprack slot list {}"
            msg = msg.format(mount, tiprack_string)
            raise Exception(msg)

    # Check for overlap between left and right tiprack slot lists
    # by taking the set intersection (&: Set intersection operator)
    intersection = set(left_tiprack_slot_list) & set(right_tiprack_slot_list)
    if len(intersection) > 0:
        msg = ("There are overlaps between your left and right pipette "
               "tiprack slots in position(s) {}")
        msg = msg.format(intersection)
        raise Exception(msg)

    # Load the CSV
    # ENUMERATED HEADERS:
    # 0. step_id, 1. instruction, 2. instruction_parameters, 3. source_labware,
    # 4. magnetic_module,5. temperature_module, 6. source_slot, 7. source_well,
    # 8. Source_well_starting_volume, 9. transfer_volume, 10. air_gap_volume,
    # 11. dest_labware, 12. dest_magnetic_module, 13. dest_temperature_module,
    # 14. dest_slot, 15. dest_well, 16. dest_well_starting_volume,
    # 17. touch_tip, 18. blow_out
    csv_rows = transfer_csv.split("\n")
    csv_list = []
    # Remove any empty lines
    for i, row in enumerate(csv_rows):
        if row == '':
            del(csv_rows[i])
        else:
            csv_list.append(row.split(','))

    slot_dict = {}
    for i in range(1, 12):
        slot_dict[i] = []

    instructions = []
    # A well formed well index consists of a letter (A-P) and a number 1-24
    # Because the largest standard labware is the 384 well plate whose indices
    # go from A1 to P24
    well_formed_well_regex = re.compile(r"^[A-P][1-2]?[0-9]$")
    for row in csv_list[1:]:
        step_id = read_var(row[0], "int")
        instruction = row[1].strip()
        instruction_parameters = row[2].strip()
        source_lw = row[3].strip()
        # column 4 and 5 are read below in the try sections
        # 4: is_source_magmod
        # 5: is_source_tempmod
        source_slot = read_var(row[6], "int")
        source_well = row[7].strip().upper()
        source_well_starting_volume = read_var(row[8], "float")
        transfer_volume = read_var(row[9], "float")
        air_gap_volume = read_var(row[10], "float")
        dest_lw = row[11]
        # 12. and 13. loaded below (yes/no) type
        # 12. is_dest_magmod
        # 13. is_dest_tempmod
        dest_slot = read_var(row[14], "int")
        dest_well = row[15].strip().upper()
        dest_well_starting_volume = read_var(row[16], "float")
        # 17., 18., loaded below, yes/no type

        # Read the module loading choices (columm 4, 5, 12, and 13)
        try:
            is_source_magmod = reply_to_bool(row[4])
            is_source_tempmod = reply_to_bool(row[5])
        except Exception:
            err_msg = ("Step id {}: Unrecognized option for the source "
                       "labware modules. Valid options are 'yes' or 'no'")
            err_msg = err_msg.format(step_id)
            raise Exception(err_msg)
        try:
            is_dest_magmod = reply_to_bool(row[12])
            is_dest_tempmod = reply_to_bool(row[13])
        except Exception:
            err_msg = ("Step id {}: Unrecognized option for the destination "
                       "labware modules. Valid options are 'yes' or 'no'. "
                       "Please correct your CSV file.")
            err_msg = err_msg.format(step_id)
            raise Exception(err_msg)

        for slot, labware, magmod, tmod in zip(
                [source_slot, dest_slot],
                [source_lw, dest_lw],
                [is_source_magmod, is_dest_magmod],
                [is_dest_magmod, is_dest_tempmod]):

            if type(slot) is int:  # slot could be a blank string, should skip.
                slot_dict[slot].append((step_id, labware, magmod, tmod))
        try:
            is_touch_tip = reply_to_bool(row[17])
            is_blowout = reply_to_bool(row[18])
        except Exception:
            err_msg = ("Step id {}: Unrecognized option for touch tip and/or "
                       "blow out options. Valid options are 'yes' or 'no', "
                       "or a blank value. Please correct your CSV file.")
            err_msg = err_msg.format(step_id)
            raise Exception(err_msg)

        # Check for error where both modules are loaded for the same labware
        for is_magmod, is_tempmod, type_string in zip(
                [is_source_magmod, is_dest_magmod],
                [is_source_tempmod, is_dest_tempmod],
                ["source", "destination"]):
            if is_magmod and is_tempmod:
                err_msg = ("Error in {} labware module options with "
                           "step_id {}: " "You cannot use both a magnetic "
                           "module and a temperature module with the same "
                           "labware, please correct your CSV file.")
                err_msg = err_msg.format(type_string, step_id)
                raise Exception(err_msg)

        # Check that labware used with the temperature module uses alum. blocks
        for is_tempmod, labware, type_string in zip(
                [is_source_tempmod, is_dest_tempmod],
                [source_lw, dest_lw],
                ["Source", "Destination"]):
            if is_tempmod and "aluminum" not in labware:
                err_msg = ("Step id {}: {} labware must be of an aluminum "
                           "block type to be used with a temperature module")
                err_msg = err_msg.format(step_id, type_string)
                raise Exception(err_msg)

        # Make sure the well indices are well formed
        for well_index in zip(
                [source_well, dest_well],
                ["source", "destination"]):
            pass

        instructions.append(
            (step_id,
             instruction,
             instruction_parameters,
             source_lw,
             is_source_magmod,
             is_source_tempmod,
             source_slot,
             source_well,
             source_well_starting_volume,
             transfer_volume,
             air_gap_volume,
             dest_lw,
             is_dest_magmod,
             is_dest_tempmod,
             dest_slot,
             dest_well,
             dest_well_starting_volume,
             is_touch_tip,
             is_blowout
             ))

    # Check that the step_ids are continous
    last_step_id = instructions[0][0]
    # Skip the first row, last_step_id is already set and we don't want to
    # compare it to itself
    for row in instructions[1:]:
        id = row[0]
        if not id == last_step_id + 1:
            err_msg = "Discontinuity in step id:s between step_id {} and {}"
            err_msg = err_msg.format(last_step_id, id)
            raise Exception(err_msg)
        last_step_id = id

    # Check that there are no mismatching entries in the labware definitions
    # Algorithm:
    # 1. Add the tiprack entries to the slot dicts as well
    # 2. Go through the dictionary entry for each slot in slots_dict and:
    # 3. Treat the first labware entry as canon and require that it is well
    # formed. It should have a labware API name, a slot, and should give
    # complete answers about what modules it is using and not using.
    # 4. Compare the 'canonical' definition to the subseqent ones for that slot
    # 5. If the the subst. defns. are identical continue looping
    # 6. If they are not: Raise an error and point out what the conflicting
    # step_id:s are, (unless it's a conflict with a tiprack which don't have
    # step_id:s), what labware API names, which slot
    # After the canonical entry is properly entered
    # it is allowed to specify only the slot as long
    # as the other fields are just blank strings ('').
    # 7. If there are no mismatching data the labware and tipracks
    # can be loaded.

    # Implementation
    # 1.1 Add the  pipette tipracks to their respective slot lists
    left_tips_lname = tiprack_map[left_mount_pipette_type][left_tip_type]
    for slot in left_tiprack_slot_list:
        slot_dict[slot].append(left_tips_lname)
    right_tips_lname = tiprack_map[right_mount_pipette_type][right_tip_type]
    for slot in right_tiprack_slot_list:
        slot_dict[slot].append(right_tips_lname)

    # 2. Iterate over the dictionary entries
    for slot in slot_dict.keys():
        # Check for cases where there's no labware definitions for the slot
        # and continue to the next slot.
        if len(slot_dict[slot]) == 0:
            continue
        # Canonical labware entry, must be well formed
        canonical_lw_entry = slot_dict[slot][0]
        can_step_id = canonical_lw_entry[0]
        can_lw_name = canonical_lw_entry[1]
        can_magmod = canonical_lw_entry[2]
        can_tempmod = canonical_lw_entry[3]

        # Check that the canonical entry is well defined
        if can_lw_name == '' or can_magmod is None or can_tempmod is None:
            err_msg = ("The initial labware definition for slot {} on the "
                       "row with step_id {} is not well defined. It must "
                       "include the labware API name and definite yes/no "
                       "answers to the questions asking whether they are "
                       "using either the Magnetic- or the Temperature module. "
                       "Please inspect your CSV file.")
            err_msg = err_msg.format(slot, can_step_id)
            raise Exception(err_msg)

        for lw_entry in slot_dict[slot][1:]:

            entry_step_id = lw_entry[0]
            entry_lw_name = lw_entry[1]
            entry_magmod = lw_entry[2]
            entry_tempmod = lw_entry[3]

            if can_lw_name != entry_lw_name and entry_lw_name != '':
                err_msg = ("There is a mismatch between the labware API names "
                           "for slot {}, the initial labware API name was {} "
                           "and it was defined in the row with step_id {} "
                           "but there is a mismatching API name ({}) on the "
                           "row with step_id {}. Please inspect your CSV.")
                err_msg = err_msg.format(
                    slot, can_lw_name, can_step_id,
                    entry_lw_name, entry_step_id)
                raise Exception(err_msg)

            # Check for magnetic module setting mismatches
            if can_magmod != entry_magmod and entry_magmod is not None:
                err_msg = ("There is a mismatch between the Magnetic module "
                           "setting for {} on slot {} on the row with "
                           "step_id {}, and the Magnetic module setting on "
                           "the row with step id {}. Please inspect your "
                           "CSV input file.")
                err_msg = err_msg.format(
                    can_lw_name, slot, can_step_id, entry_step_id)

            # Check for Temperature module setting mismatches
            if can_tempmod != entry_tempmod and entry_tempmod is not None:
                err_msg = ("There is a mismatch between the Temperature "
                           "module setting for {} on slot {} on the row with "
                           "step_id {}, and the Temperature module setting on "
                           "the row with step id {}. Please inspect your "
                           "CSV input file.")
                err_msg = err_msg.format(
                    can_lw_name, slot, can_step_id, entry_step_id)

    # Check that 'dispense parked tip operations' are well formed. This means:
    # 1. Not attempting to dispense an already dispensed parked tip
    # 2. There must be minimally complete instructions for dispensing the tip
    # meaning: dispensing volume, destionation- slot and well.

    # 1. Check that all step_id instructions for selecting a parked tip are
    # unique
    dispense_parked_tip_step_id_list = []
    for instruction in instructions:
        if instruction[1] == 'dispense_parked_tip':
            dispense_parked_tip_step_id_list.append(
                get_instruction_param_val(
                    instruction[2], "step_id"))

    # Count the occurences of each step_id
    step_id_occurences = Counter(dispense_parked_tip_step_id_list)
    if max(step_id_occurences.values() > 1):
        err_msg = ("There are multiples references to the same step_id for "
                   "dispensing a parked tip. Can't dispense an already "
                   "dispensed tip. Please inspect your input CSV file.")
        raise Exception(err_msg)


    # # load labware
    # load tipracks in defined slots
    # tiprack_type = tiprack_map[pipette_type][tip_type]
    # tipracks = []
    # for slot in range(1, 13):
    #     if slot not in ctx.loaded_labwares:
    #         tipracks.append(ctx.load_labware(tiprack_type, str(slot)))
    #
    # # load pipette(s)
    # pip = ctx.load_instrument(
    #   pipette_type, pipette_mount, tip_racks=tipracks)
    #
    # tip_count = 0
    # tip_max = len(tipracks*96)
    #
    # def pick_up():
    #     nonlocal tip_count
    #     if tip_count == tip_max:
    #         ctx.pause('Please refill tipracks before resuming.')
    #         pip.reset_tipracks()
    #         tip_count = 0
    #     pip.pick_up_tip()
    #     tip_count += 1
    #
    # def parse_well(well):
    #     letter = well[0]
    #     number = well[1:]
    #     return letter.upper() + str(int(number))
    #
    # if tip_reuse == 'never':
    #     pick_up()
    # for line in transfer_info:
    #     _, s_slot, s_well, h, _, d_slot, d_well, vol = line[:8]
    #     source = ctx.loaded_labwares[
    #         int(s_slot)].wells_by_name()[parse_well(s_well)].bottom(float(h))
    #     dest = ctx.loaded_labwares[
    #         int(d_slot)].wells_by_name()[parse_well(d_well)]
    #     if tip_reuse == 'always':
    #         pick_up()
    #     pip.transfer(float(vol), source, dest, new_tip='never')
    #     if tip_reuse == 'always':
    #         pip.drop_tip()
    # if pip.hw_pipette['has_tip']:
    #     pip.drop_tip()
    ctx.comment("\n\n~~~ Protocol finished ~~~\n")
