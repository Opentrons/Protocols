from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load modules and labware
plate = labware.load('biorad_96_wellplate_200ul_pcr', '1')
tempdeck = modules.load('tempdeck', '4')
block = labware.load(
    'opentrons_24_aluminumblock_nest_1.5ml_screwcap', '4', share=True)


def run_custom_protocol(
        p300_mount: StringSelection('left', 'right') = 'left',
        p1000_mount: StringSelection('right', 'left') = 'right',
        number_of_transfers: int = 96,
        transfer_volume_in_microliters: float = 50,
        tip_strategy: StringSelection('one tip', 'different tips') = 'one tip',
        temperature_module_temperature_in_degrees_C: float = 65
):
    # check
    if number_of_transfers > 96 or number_of_transfers < 1:
        raise Exception('Invalid number of tranfsers (must be 1-96).')
    if (
        temperature_module_temperature_in_degrees_C < 4 or
        temperature_module_temperature_in_degrees_C > 96
       ):
        raise Exception('Temperature module must be between 4 and 96C')

    # choose pipette
    if transfer_volume_in_microliters > 300:
        tiprack = labware.load('opentrons_96_tiprack_300ul', '2')
        pip = instruments.P1000_Single(mount=p1000_mount, tip_racks=[tiprack])

    else:
        tiprack = labware.load('opentrons_96_tiprack_300ul', '2')
        pip = instruments.P300_Single(mount=p300_mount, tip_racks=[tiprack])

    # perform transfers
    num_buff_tubes = math.ceil(
        transfer_volume_in_microliters*number_of_transfers/1350)
    robot.comment('Reaching temperature. Ensure ' + str(num_buff_tubes) + ' \
tubes of buffer are aligned vertically in the aluminum block.')
    tempdeck.set_temperature(temperature_module_temperature_in_degrees_C)
    tempdeck.wait_for_temp()

    buffer = block.wells()[:num_buff_tubes]
    num_trans_per_tube = 1350//transfer_volume_in_microliters  # dead volume
    tip = 'never' if tip_strategy == 'one tip' else 'always'
    if tip_strategy == 'one tip':
        pip.pick_up_tip()
    for i, dest in enumerate(plate.wells()[:number_of_transfers]):
        buff_ind = i//num_trans_per_tube
        pip.transfer(
            transfer_volume_in_microliters,
            buffer[buff_ind],
            dest,
            new_tip=tip
        )
    if pip.tip_attached:
        pip.drop_tip()
