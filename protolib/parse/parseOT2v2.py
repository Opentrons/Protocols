import json
import sys
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


def parse(protocol_path):
    if not protocol_path:
        print('No protocol path... something weird happened!')
        return {}
    print('Parsing protocol: {}'.format(protocol_path))

    with open(protocol_path) as f:
        contents = f.read()
        protocol = parse_protocol(
            protocol_contents=contents, filename=protocol_path)

    assert protocol.api_level == '2'

    context = opentrons.protocol_api.contexts.ProtocolContext()
    context.home()
    run_protocol(protocol, simulate=True, context=context)

    instruments = [{'mount': mount, 'name': pipette.name} for mount,
                   pipette in context.loaded_instruments.items()]

    labware = filter_none([parse_labware(slot, labware)
                           for slot, labware
                           in context.loaded_labwares.items()])

    # TODO IMMEDIATELY: need `parameters` from parse_protocol fn
    parameters = {}

    # TODO IMMEDIATELY
    modules = []

    return {
        "instruments": instruments,
        "labware": labware,
        "parameters": parameters,
        "modules": modules,
        "metadata": protocol.metadata}


if __name__ == '__main__':
    sourceFilePath = sys.argv[1]
    destFilePath = sys.argv[2]
    print('OT2 APIv2: parsing {} to {}'.format(sourceFilePath, destFilePath))

    result = parse(sourceFilePath)
    with open(destFilePath, 'w') as f:
        json.dump(result, f)
