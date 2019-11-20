import json
import sys
from pathlib import Path
import opentrons
from opentrons.protocol_api.execute import run_protocol
from opentrons.protocols.parse import parse as parse_protocol


def filter_none(arr):
    return [i for i in arr if i is not None]


def parse_labware(slot, labware):
    if labware is None:
        return None

    # Thermocycler Geometry objects etc have no 'name'
    # TODO IMMEDIATELY better way to distingush non-labware
    # in `loaded_labwares`?
    try:
        labware_type = labware.name
    except AttributeError:
        return None

    # TODO: Ian 2019-09-12 Labware should remember its label,
    # use that for `name` instead of Labware.__str__
    return {
        'slot': str(slot),
        'type': labware_type,  # load name or something
        'name': str(labware),  # display name
        'share': False}


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


def parse(protocol_path):
    if not protocol_path:
        print('No protocol path... something weird happened!')
        return {}
    print('Parsing protocol: {}'.format(protocol_path))

    fields_json_path = Path(protocol_path).parent / ('fields.json')
    has_fields = Path(fields_json_path).is_file()

    with open(protocol_path) as f:
        original_contents = f.read()

    fields = []
    contents = original_contents
    if has_fields:
        with open(fields_json_path) as f:
            fields = json.load(f)
            # for simulation, we need to add a get_values() fn that supplies
            # the default values
            default_values = {
                f['name']: get_default_field_value(f) for f in fields}
            contents = prepend_get_values_fn(original_contents, default_values)

    # load any custom labware in protocols/{PROTOCOL_SLUG}/labware/*.json
    custom_labware_defs = []
    custom_labware_path = Path(protocol_path).parent / 'labware'
    if custom_labware_path.is_dir():
        for l_path in custom_labware_path.iterdir():
            with open(l_path) as lf:
                custom_labware_defs.append(json.load(lf))
    for labware_def in custom_labware_defs:
        opentrons.protocol_api.labware.save_definition(labware_def, force=True)

    protocol = parse_protocol(
        protocol_contents=contents, filename=protocol_path)

    assert protocol.api_level == '2'

    context = opentrons.protocol_api.contexts.ProtocolContext()
    context.home()
    run_protocol(protocol, simulate=True, context=context)

    instruments = [{'mount': mount, 'name': pipette.name} for mount,
                   pipette in context.loaded_instruments.items() if pipette]

    labware = filter_none([parse_labware(slot, labware)
                           for slot, labware
                           in context.loaded_labwares.items()])

    # NOTE: this isn't really used right now...
    metadata = protocol.metadata

    # TODO IMMEDIATELY
    modules = []

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

    result = parse(sourceFilePath)
    with open(destFilePath, 'w') as f:
        json.dump(result, f)
