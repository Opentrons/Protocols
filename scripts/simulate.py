from opentrons.cli.analyze import _analyze
from pathlib import Path
from anyio import Path as AsyncPath
from asyncio import run


def simulate(file_in, file_out):
    run(_analyze([Path('/Users/nickdiehl/Desktop/Opentrons Internal/test2.py')],
        AsyncPath('/Users/nickdiehl/Desktop/Opentrons Internal/analysis_test2.json')))
