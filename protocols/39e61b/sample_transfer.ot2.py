from opentrons import labware, instruments, modules
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Same Transfer ',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load modules and labware
tempdeck = modules.load('tempdeck', '1')
dest_plate = labware.load(
    'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    '1',
    label='E. Coli destination plate',
    share=True
)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
source_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr',
    '2',
    'DNA plate'
)
tips10 = labware.load('opentrons_96_tiprack_10ul', '4')


def run_custom_protocol(
        P10_pipette_type: StringSelection('multi', 'single') = 'multi',
        P10_mount: StringSelection('left', 'right') = 'left',
        number_of_samples: int = 96
):
    # check
    if number_of_samples < 1 or number_of_samples > 96:
        raise Exception('Invalid number of sample columns.')

    num_sample_cols = math.ceil(number_of_samples/8)

    if P10_pipette_type == 'multi':
        pip10 = instruments.P10_Multi(mount=P10_mount, tip_racks=[tips10])
        sources = source_plate.rows('A')[0:num_sample_cols]
        dests = dest_plate.rows('A')[0:num_sample_cols]
    else:
        pip10 = instruments.P10_Single(mount=P10_mount, tip_racks=[tips10])
        sources = source_plate.wells()[0:number_of_samples]
        dests = dest_plate.wells()[0:number_of_samples]

    for s, d in zip(sources, dests):
        pip10.pick_up_tip()
        pip10.transfer(1, s, d, blow_out=True, new_tip='never')

        # set mix speeds
        pip10.set_flow_rate(aspirate=1, dispense=2)
        pip10.mix(5, 5, d)

        # reset flow rates
        pip10.set_flow_rate(aspirate=5, dispense=10)
        offset = (d, d.from_center(r=0.9, h=0.9, theta=0))
        pip10.move_to(offset)
        pip10.blow_out()
        pip10.drop_tip()
