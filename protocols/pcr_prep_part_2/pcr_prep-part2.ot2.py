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
            'p10-multi', 'P50-multi', 'p300-multi')='p50-multi',
        left_pipette_tip: StringSelection(
            'tiprack-10ul', 'tiprack-200ul',
            'opentrons-tiprack-300ul')='opentrons-tiprack-300ul',
        right_pipette: StringSelection(
            'p10-multi', 'P50-multi', 'p300-multi')='p300-multi',
        right_pipette_tip: StringSelection(
            'tiprack-10ul', 'tiprack-200ul',
            'opentrons-tiprack-300ul')='opentrons-tiprack-300ul',
        mastermix_volume: float=18,
        DNA_volume: float=2
        ):

    def mount_pipette(pipette_type, mount, tiprack, tiprack_slot):
        tip_rack = [labware.load(tiprack, slot)
                    for slot in tiprack_slot]
        pipette_args = {'mount': mount, 'tip_racks': tip_rack}
        if pipette_type == 'p10-multi':
            pipette = instruments.P10_Multi(**pipette_args)
        elif pipette_type == 'p50-multi':
            pipette = instruments.P50_Multi(**pipette_args)
        else:
            pipette = instruments.P300_Multi(**pipette_args)
        return pipette

    # labware setup
    dna_plate = labware.load('PCR-strip-tall', '1', 'DNA')
    dest_plate = labware.load('PCR-strip-tall', '2', 'Output')
    trough = labware.load('trough-12row', '3')

    # instrument setup
    pipette_l = mount_pipette(
        left_pipette, 'left', left_pipette_tip, ['4', '5'])
    pipette_r = mount_pipette(
        right_pipette, 'right', right_pipette_tip, ['6', '7'])

    # reagent setup
    mastermix = trough.wells('A1')

    col_num = math.ceil(number_of_samples / 8)

    # distribute mastermix
    if mastermix_volume < pipette_r.min_volume and \
            mastermix_volume > pipette_l.min_volume:
        pipette = pipette_l
    else:
        pipette = pipette_r
    pipette.distribute(
        mastermix_volume, mastermix, dest_plate.cols('1', length=col_num),
        blow_out=mastermix)

    # transfer DNA
    if DNA_volume < pipette_r.min_volume and DNA_volume > pipette_l.min_volume:
        pipette = pipette_l
    else:
        pipette = pipette_r
    for source, dest in zip(dna_plate.cols('1', length=col_num),
                            dest_plate.cols('1', length=col_num)):
        pipette.transfer(DNA_volume, source, dest)
