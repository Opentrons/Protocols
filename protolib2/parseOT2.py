from inspect import signature, Parameter
# import json
import time
import shutil
from opentrons import robot, labware
from opentrons.instruments import Pipette as BasePipette
import sys
import opentrons

allProtocolFiles = sys.argv[1:]

print('Opentrons verson: ', opentrons.__version__)
print('Parsing OT2. Files:')
print(allProtocolFiles)
print('*-' * 40)

global all_labware
orig_labware_load = labware.load


def load_labware_spy(labware_name, slot, label=None):
    all_labware.append({
        'type': labware_name,
        'slot': slot,
        'name': label or labware_name
        })
    return orig_labware_load(labware_name, slot, label)


labware.load = load_labware_spy

def parse(protocol_path):

    if not protocol_path:
        return {}
    print('Parsing protocol: {}'.format(protocol_path))

    # # Calibration data overrides settings sometimes,
    # # making protocols interfere with each other and sometimes throw errors.
    # # This HACK works around issues with calibration.
    #
    # try:
    #     shutil.rmtree(
    #         opentrons_settings.get('CALIBRATIONS_DIR', 'calibrations'))
    # except FileNotFoundError:
    #     pass

    # reset is needed to reset tip tracking, other states may also interfere
    robot.reset()

    global all_containers
    # new protocol. start with no containers
    all_containers = []

    orig_time_sleep = time.sleep

    def fake_sleep(*args, **kwargs):
        # equivalent to pre-monkeypatched `time.sleep(0)`
        orig_time_sleep(0)

    def fake_delay(self, *args, **kwargs):
        # allow chaining
        fake_sleep(*args, **kwargs)
        return self

    # time.sleep
    fake_time = time
    fake_time.sleep = fake_sleep

    # monkeypatch fake delay/sleep
    PatchedPipette = BasePipette
    PatchedPipette.delay = fake_delay

    PatchedMagbead = BaseMagbead
    PatchedMagbead.delay = fake_delay

    # do the same opentrons/__init__.py trick to monkeypatch delays
    class InstrumentsWrapper(object):
        def __init__(self, robot):
            self.robot = robot

        def Pipette(self, *args, **kwargs):
            return PatchedPipette(self.robot, *args, **kwargs)

    _globals = {
        'robot': robot,
        'opentrons.containers': containers,
        'opentrons.instruments': InstrumentsWrapper(robot),
        'time': fake_time
    }

    with open(protocol_path) as f:
        protocol_text = f.read()

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
        robot, protocol_function, all_containers)

def get_result_dict(robot, protocol_function, all_containers):
    return {
        'instruments': get_instruments(robot),
        'containers': all_containers,
        'parameters': get_parameters(protocol_function)
        if protocol_function else []
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
