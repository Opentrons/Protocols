from inspect import signature, Parameter
# import json
import re
import shutil
from opentrons import robot, containers
from opentrons.instruments.pipette import Pipette
from opentrons.util.environment import settings as opentrons_settings

# HACK to get pipette type
pipetteType = type(Pipette(robot, 'a'))


def parse(protocol_path):
    if not protocol_path:
        return {}
    print('Parsing protocol: {}'.format(protocol_path))

    # Calibration data overrides settings sometimes,
    # making protocols interfere with each other and sometimes throw errors.
    # This HACK works around issues with calibration.

    try:
        shutil.rmtree(
            opentrons_settings.get('CALIBRATIONS_DIR', 'calibrations'))
    except FileNotFoundError:
        pass

    # reset is needed to reset tip tracking, other states may also interfere
    robot.reset()

    # text-replace-monkeypatch containers.load with this load_container fn
    all_containers = []

    def load_container(container_name, slot, label=None):
        all_containers.append({
            'type': container_name,
            'slot': slot,
            'name': label or container_name
            })
        return containers.load(container_name, slot, label)

    _globals = {'robot': robot, 'load_container': load_container}

    with open(protocol_path) as f:
        protocol_text = f.read()

    # HACK: replace containers.load( with load_container(
    protocol_text = re.sub(
        r'containers\.load\(', 'load_container(', protocol_text)

    exec(
        compile(protocol_text, protocol_path, 'exec'),
        _globals
    )

    # Mini-parametric protocols have `def run_custom_protocol(...)` fn
    # in global scope
    protocol_function = _globals.get('run_custom_protocol')

    if protocol_function is not None:
        # call it with default args,
        # in case there are any container.load commands.
        # The default args will thus determine what the deck map looks like.
        protocol_function()

    return get_result_dict(
        robot, protocol_function, protocol_text, all_containers)


def get_result_dict(robot, protocol_function, protocol_text, all_containers):
    return {
        'instruments': get_instruments(robot),
        'containers': all_containers,
        'parameters': get_parameters(protocol_function)
        if protocol_function else {}
    }


def get_parameters(protocol_function):
    """
    Inspect the run_custom_protocol fn arg annotations to determine
    what customizable fields should be
    """
    def get_annotation(annotation):
        try:
            # For normal annotations like float and int:
            name = annotation.__name__
            return {'type': name}
        except AttributeError:
            # annotation must implement get_json interface:
            return annotation.get_json()

    return [
        {
         'name': param.name,
         'annotation': get_annotation(param.annotation)
         if param.annotation != Parameter.empty else None,
         'default': param.default
         }
        for param in signature(protocol_function).parameters.values()
    ]


def get_instruments(robot):
    return [
        {'name': instr.name,
         'axis': axis.lower(),
         'channels': getattr(instr, 'channels', None),
         'type': instr.__class__.__name__.lower(),
         'min_volume': getattr(instr, 'min_volume', None),
         'max_volume': getattr(instr, 'max_volume', None)
         }
        for axis, instr in robot.get_instruments()
    ]


# def get_containers(protocol_text):
#     # Since in 2.5.0, robot.get_containers() and
#     # robot.containers() are keyed by container name,
#     # this is a hack to parse the text
#     # HACK (Ian 2017-09-26)
#     def parse_load_container(load_statement):
#         arg_pattern = re.compile(r"['\"]([^'\"]*)['\"]", re.DOTALL)
#         args_in_quotes = re.findall(arg_pattern, load_statement)
#
#         container_type = args_in_quotes[0]
#         slot = args_in_quotes[1]  # HACK!
#        name = container_type if len(args_in_quotes) < 3 else args_in_quotes[2]  # noqa: E501
#         return {
#             'name': name,
#             'type': container_type,
#             'slot': slot
#         }
#
#     load_arg_exp = re.compile(r"containers.load\(([^\)]*)\)")
#     load_statements = re.findall(load_arg_exp, protocol_text)
#
#     return [parse_load_container(stmt) for stmt in load_statements]
