import json
import sys
from pathlib import Path
import opentrons
from opentrons.protocols.execution.execute import run_protocol
from opentrons.protocols.parse import parse as parse_protocol
from opentrons.cli.analyze import _analyze
from pathlib import Path
from anyio import Path as AsyncPath
from asyncio import run


def simulate(file_in, file_out):
    run(_analyze([Path(file_in)], AsyncPath(file_out)))


def get_default_field_value(field):
    if field['type'] == 'dropDown':
        return field['options'][0]['value']
    return field['default']


def prepend_get_values_fn(protocol_content, values):
    get_values_content = f"""
def get_values(*field_names):
    all_values = {values}
    return [all_values[name] for name in field_names]

"""
    return get_values_content + protocol_content


def get_fields(protocol_path):
    fields_json_path = Path(protocol_path).parent / ('fields.json')
    has_fields = Path(fields_json_path).is_file()

    with open(protocol_path) as f:
        original_contents = f.read()

    if has_fields:
        with open(fields_json_path) as f:
            fields = json.load(f)
            # for simulation, we need to add a get_values() fn that supplies
            # the default values
            return fields
    return []


def generate_protocol(protocol_path, fields):
    if not protocol_path:
        print('No protocol path... something weird happened!')
        return {}
    print('Parsing protocol: {}'.format(protocol_path))

    with open(protocol_path) as f:
        original_contents = f.read()

    contents = original_contents
    if len(fields) > 0:
        # for simulation, we need to add a get_values() fn that supplies
        # the default values
        default_values = {
            f['name']: get_default_field_value(f) for f in fields}
        contents = prepend_get_values_fn(original_contents, default_values)

    # create temporary file where field defaults are injected
    temp_py = Path(protocol_path).parent / ('temp.py')
    with open(temp_py) as f:
        f.write(contents)

    # load any custom labware in protocols/{PROTOCOL_SLUG}/labware/*.json
    custom_labware_defs = []
    custom_labware_path = Path(protocol_path).parent / 'labware'
    if custom_labware_path.is_dir():
        for l_path in custom_labware_path.iterdir():
            with open(l_path) as lf:
                custom_labware_defs.append(json.load(lf))
    for labware_def in custom_labware_defs:
        opentrons.protocol_api.labware.save_definition(labware_def, force=True)

    temp_json = Path(protocol_path).parent / ('temp.json')

    protocol = simulate(protocol_file=[temp_py], filename=temp_json)

    Path.unlink(temp_py)
    Path.unlink(temp_json)

    assert protocol['config']['apiLevel'] >= [2, 0]

    return protocol


def filter_none(arr):
    return [i for i in arr if i is not None]


def parse_module(slot, module):
    if module is None:
        return None

    # TODO: Nick 3/3/2020 better way to access module (load) name directly

    try:
        module_type = module._module.name()
    except AttributeError:
        return None

    return {
        'slot': str(slot),
        'type': module_type,  # load name or something
        'name': str(module),  # display name
        'share': False}


def parse_labware(labware, protocol):

    if labware is None:
        return None

    if 'displayName' in labware:
        name = labware['displayName']
    else:
        name = labware['result']['displayName']

    # Thermocycler Geometry objects etc have no 'name'
    # TODO IMMEDIATELY better way to distingush non-labware
    # in `loaded_labwares`?
    try:
        labware_type = labware['params']['loadName']
    except AttributeError:
        return None

    # TODO: Ian 2019-09-12 Labware should remember its label,
    # use that for `name` instead of Labware.__str__

    if 'slotName' in labware['params']['location']:
        slot = str(labware['params']['location']['slotName'])
    else:
        parent_id = labware['params']['moduleId']
        parent_module = [
            mod for mod in protocol['modules']
            if mod['id'] == parent_id][0]
        slot = parent_module['location']['slotName']

    return {
        'slot': str(slot),
        'type': labware_type,  # load name or something
        'name': name,  # display name
        'share': False}


def parse(protocol):

    # NOTE:(IL, 2020-05-13)L there’s no deck calibration, and the
    # identity deck calibration is about 25 mm too high (as of v1.17.1).
    # Because of this, tall labware can cross the threshold and cause a
    # LabwareHeightError even though they're safe to use.
    # So we'll apply a HACK-y -25 offset of the deck.
    instruments = [
        {'mount': mount, 'name': pipette['pipetteName']}
        for mount, pipette in protocol['pipettes'].items() if pipette]

    # NOTE: module population broke library deck layout 3/5/2020
    modules = filter_none([parse_module(command)
                           for command in protocol['commands']
                           if command['commandType'] == 'loadModule'])

    labware = filter_none([parse_labware(command, protocol)
                           for command in protocol['commands']
                           if command['commandType'] == 'loadLabware'])

    # NOTE: this isn't really used right now...
    metadata = protocol.metadata

    return {
        "instruments": instruments,
        "labware": labware,
        "fields": fields,
        "modules": modules,
        "metadata": metadata,
        "content": original_contents,
        "custom_labware_defs": custom_labware_defs
    }


if __name__ == '__main__':
    sourceFilePath = sys.argv[1]
    destFilePath = sys.argv[2]
    print('OT2 APIv2: parsing {} to {}'.format(sourceFilePath, destFilePath))
    
    fields = get_fields(sourceFilePath)
    raw_protocol = generate_protocol(sourceFilePath)
    result = parse(simulated_protocol)
    with open(destFilePath, 'w') as f:
        json.dump(result, f, indent=4, sort_keys=True)
