import json
import sys
import opentrons
from opentrons.protocol_api.execute import run_protocol
from opentrons.protocols.parse import parse as parse_protocol


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

    pipettes = {mount: pipette.name for mount,
                pipette in context.loaded_instruments.items()}

    # TODO: Ian 2019-09-12 Labware should remember its label, use that here instead of Labware.__str__
    labware = {slot: str(labware)
               for slot, labware in context.loaded_labwares.items() if labware is not None}

    parameters = {}  # TODO IMMEDIATELY: need `parameters` from parse_protocol fn

    return {"pipettes": pipettes, "labware": labware, "parameters": parameters, "metadata": protocol.metadata}


if __name__ == '__main__':
    sourceFilePath = sys.argv[1]
    destFilePath = sys.argv[2]
    print('OT2 APIv2: parsing {} to {}'.format(sourceFilePath, destFilePath))

    result = parse(sourceFilePath)
    print('result', result)
    with open(destFilePath, 'w') as f:
        json.dump(result, f)
