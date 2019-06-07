from opentrons import labware, instruments
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Opentrons <protocols@opentrons.com>',
    'source': 'Protocol Library'
    }


def run_custom_protocol(
        number_of_samples: int=96,
        left_pipette: StringSelection(
            'p10-multi', 'P50-multi', 'p300-multi', 'none')='p50-multi',
        right_pipette: StringSelection(
            'p10-multi', 'P50-multi', 'p300-multi', 'none')='p300-multi',
        mastermix_volume: float=18,
        DNA_volume: float=2
        ):

    if left_pipette == right_pipette and left_pipette == 'none':
        raise Exception('You have to select at least 1 pipette.')

    def mount_pipette(pipette_type, mount, tiprack_slot):
        if pipette_type == 'p10-multi':
            tip_rack = [labware.load('tiprack-10ul', slot)
                        for slot in tiprack_slot]
            pipette = instruments.P10_Multi(
                mount=mount,
                tip_racks=tip_rack)
        elif pipette_type == 'p50-multi':
            tip_rack = [labware.load('opentrons-tiprack-300ul', slot)
                        for slot in tiprack_slot]
            pipette = instruments.P50_Multi(
                mount=mount,
                tip_racks=tip_rack)
        else:
            tip_rack = [labware.load('opentrons-tiprack-300ul', slot)
                        for slot in tiprack_slot]
            pipette = instruments.P300_Multi(
                mount=mount,
                tip_racks=tip_rack)
        return pipette

    # labware setup
    dna_plate = labware.load('PCR-strip-tall', '1', 'DNA')
    dest_plate = labware.load('PCR-strip-tall', '2', 'Output')
    trough = labware.load('trough-12row', '3')

    # instrument setup
    pipette_l = mount_pipette(
        left_pipette, 'left', ['4', '5']
        ) if 'none' not in left_pipette else None
    pipette_r = mount_pipette(
        right_pipette, 'right', ['6', '7']
        ) if 'none' not in right_pipette else None

    # determine which pipette has the smaller volume range
    if pipette_l and pipette_r:
        if left_pipette == right_pipette:
            pip_s = pipette_l
            pip_l = pipette_r
        else:
            if pipette_l.max_volume < pipette_r.max_volume:
                pip_s, pip_l = pipette_l, pipette_r
            else:
                pip_s, pip_l = pipette_r, pipette_l
    else:
        pipette = pipette_l if pipette_l else pipette_r

    # reagent setup
    mastermix = trough.wells('A1')

    col_num = math.ceil(number_of_samples / 8)

    # distribute mastermix
    if pipette_l and pipette_r:
        if mastermix_volume <= pip_s.max_volume:
            pipette = pip_s
        else:
            pipette = pip_l
    pipette.distribute(
        mastermix_volume, mastermix, dest_plate.cols('1', length=col_num),
        blow_out=mastermix)

    # transfer DNA
    if pipette_l and pipette_r:
        if DNA_volume <= pip_s.max_volume:
            pipette = pip_s
        else:
            pipette = pip_l
    for source, dest in zip(dna_plate.cols('1', length=col_num),
                            dest_plate.cols('1', length=col_num)):
        pipette.transfer(DNA_volume, source, dest)
