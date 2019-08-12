from opentrons import labware, instruments
from otcustomizers import StringSelection, FileInput
import time

metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# matrix tube rack
matrix_rack_name = 'matrix_96_2d_barcoded_tubes_1.4mL'
if matrix_rack_name not in labware.list():
    labware.create(
        matrix_rack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.83,
        depth=43,
        volume=1400)

csv_example = """
Transfection,Plasmid 1 Location,Plasmid 1 Volume,Plasmid 2 Location,Plasmid 2 \
Volume,Plasmid 3 Location,Plasmid 3 Volume,Plasmid 4 Location,Plasmid 4 Volume
1,A1,12.5,B5,6.3,C2,6.3,N/A,N/A
2,A2,16.7,A5,8.3,N/A,N/A,N/A,N/A
3,A2,12.5,A5,12.5,N/A,N/A,N/A,N/A
"""


def run_custom_protocol(
        right_pipette: StringSelection(
            'P50_Single', 'P10_Single', 'P300_Single')='P50_Single',
        cherrypicking_csv: FileInput=csv_example):

    # labware setup
    matrix_tubes = labware.load(
        matrix_rack_name, '1',
        'Plasmids for Cherry Picking')
    final_tubes = labware.load(
        'opentrons_6_tuberack_falcon_50ml_conical', '2',
        'Final Transfection Reagents')
    source_tubes = labware.load(
        'opentrons_6_tuberack_falcon_50ml_conical', '3',
        'Source Transfection Reagents')

    left_tiprack = labware.load('opentrons_96_tiprack_1000ul', '4')

    tiprack_name = 'opentrons_96_tiprack_10ul' if right_pipette == \
                   'P10_Single' else 'opentrons_96_tiprack_300ul'
    right_tiprack = labware.load(tiprack_name, '5')

    # instruments setup
    pipL = instruments.P1000_Single(
        mount='left',
        tip_racks=[left_tiprack])
    pipR = getattr(instruments, right_pipette)(
        mount='right',
        tip_racks=[right_tiprack])

    # reagent setup
    reagent_1 = source_tubes.wells('A1')
    reagent_2 = source_tubes.wells('A2')

    def csv_to_list(cherrypicking_csv):
        """This saves each transfection as a dictionary, and returns a list of
        dictionaries"""
        csv_info = [cell for line in cherrypicking_csv.splitlines() if line
                    for cell in [line.split(',')]]
        transfer_plans = []
        for line in csv_info[1:]:
            new_dict = {'source': [], 'vol': []}
            new_dict['source'] = [
                matrix_tubes.wells(name)
                for name in line[1::2] if not name == 'N/A']
            new_dict['vol'] = [
                float(vol) for vol in line[2::2] if not vol == 'N/A']
            transfer_plans.append(new_dict)
        return transfer_plans

    # get transfer plans from CSV input
    transfer_plans = csv_to_list(cherrypicking_csv)

    # transfer Reagent 1
    pipL.pick_up_tip()
    for vol, row in zip([1480, 1420], final_tubes.rows()):
        pipL.transfer(1480, reagent_1, row, new_tip='never')
    pipL.drop_tip()

    # cherry pick plasmids
    row_A = final_tubes.rows('A').wells('1', to='3')
    for plan, dest in zip(transfer_plans, row_A):
        for source, vol in zip(plan['source'], plan['vol']):
            pipR.transfer(vol, source, dest, new_tip='always')

    # transfer diluent 2 and mix
    row_B = final_tubes.rows('B').wells('1', to='3')

    for index, dest in enumerate(row_B):
        pipR.pick_up_tip()
        pipR.transfer(80, reagent_2, dest.top(), blow_out=True,
                      new_tip='never')
        pipR.set_flow_rate(aspirate=pipR.max_volume/4,
                           dispense=pipR.max_volume/2)  # slow speed for mix
        pipR.mix(3, pipR.max_volume, dest)
        if index == 0:
            start_time = time.time()  # set timer during the first loop
        pipR.set_flow_rate(aspirate=pipR.max_volume/2,
                           dispense=pipR.max_volume)  # default speed
        pipR.blow_out()
        pipR.drop_tip()

    # check timer for 4.5 minutes (270 seconds)
    time_remained = 270 - (time.time() - start_time)
    if time_remained > 0:
        pipR.delay(time_remained)

    # transfer row B to row A
    pipL.set_flow_rate(aspirate=300, dispense=500)  # slow speed for transfer
    for a, b in zip(row_A, row_B):
        pipL.transfer(1500, b, a)
