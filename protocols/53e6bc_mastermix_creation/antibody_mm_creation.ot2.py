from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': 'Antibody Mastermix Creation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
rack_5ml_name = 'vwr_15_tuberack_selfstanding_5ml_conical'
if rack_5ml_name not in labware.list():
    labware.create(
        rack_5ml_name,
        grid=(5, 3),
        spacing=(25, 25),
        diameter=14,
        depth=56,
        volume=5000
    )

plate_name = 'vwr_96_wellplate_2.2ml_deep'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=39,
        volume=2200
    )

# load labware
tempdeck = modules.load('tempdeck', '1')
ab_plate = labware.load(plate_name, '1', share=True)
tempdeck.set_temperature(4)
robot.comment('Reaching temperature...')
tempdeck.wait_for_temp()
rack_5ml = labware.load(rack_5ml_name, '2', '3x5 5ml tuberack')
tiprack300 = labware.load('opentrons_96_tiprack_300ul', '3', '300ul tiprack')
rack_1500ul = labware.load(
    'opentrons_24_tuberack_nest_1.5ml_screwcap', '4')
tiprack10 = labware.load('opentrons_96_tiprack_10ul', '5', '10ul tiprack')

# reagent setup
mm = rack_5ml.wells()[0]
pbs = rack_5ml.wells()[1]
bs_buffer = rack_1500ul.wells()[0]

example_csv = """Volume per antibody(in ul),Antibody,Well
2.2,CD3 BUV395,A1
1.1,CD45 BUV496,A3
1.1,CD15 BUV563,A5
1.1,CD45RA BUV615,A7
2.2,CD14 BUV661,A9
0.55,CD8 BUV737,A11
2.2,CD11c BUV805,B2
1.1,CD25 BV421,B4
0.55,CD4 BV480,B6
2.2,CD16 BV605,B8
2.2,CD123 BV650,B10
2.2,CD127 BV711,B12
2.2,IgD BV750,C1
2.2,CD304 BV786,C3
2.2,CD141 BB515,C5
"""


def run_custom_protocol(
        p10_single_mount: StringSelection('left', 'right') = 'left',
        p300_single_mount: StringSelection('right', 'left') = 'right',
        number_of_samples: int = 24,
        antibody_csv: FileInput = example_csv
):
    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Number of samples must be from 1-96.')
    if p10_single_mount == p300_single_mount:
        raise Exception('Pipette mounts cannot match.')

    # pipettes
    p10 = instruments.P10_Single(mount=p10_single_mount, tip_racks=[tiprack10])
    p300 = instruments.P300_Single(
        mount=p300_single_mount, tip_racks=[tiprack300])

    # transfer data from .csv files
    transfer_data = [
        [val.strip() for val in line.split(',')]
        for line in antibody_csv.splitlines() if line
    ][1:]

    # volume calculations and mastermix creation
    vol_buffer = 11*number_of_samples

    # volume check
    if vol_buffer + sum(
            [float(t[0])*number_of_samples for t in transfer_data]) > 5000:
        raise Exception('WARNING: Specified volumes and sample number may \
cause overflow in the mastermix tube.')

    current_vol = 0
    # transfer buffer, antibodies, and pbs
    pip = p10 if vol_buffer < 30 else p300
    pip.transfer(vol_buffer, bs_buffer, mm.bottom(5))

    for t in transfer_data:
        vol = float(t[0])*number_of_samples
        source = ab_plate.wells(t[2].upper()).bottom(5)
        pip = p10 if vol < 30 else p300

        current_vol += vol
        pip.pick_up_tip()
        pip.transfer(vol, source, mm.bottom(5), new_tip='never')
        mix_vol = (
            current_vol*0.5
            if current_vol*0.5 < pip.max_volume*0.9
            else pip.max_volume*0.9
        )
        pip.mix(3, mix_vol, mm.bottom(5))
        pip.blow_out(mm.top(-5))
        pip.drop_tip()

    # adjust with PBS
    end_vol = 100*number_of_samples
    if end_vol > current_vol:
        pbs_vol = end_vol - current_vol
        pip = p10 if pbs_vol < 30 else p300
        mix_vol = (
            end_vol/2
            if end_vol/2 < p300.max_volume*0.9
            else p300.max_volume*0.9
        )
        num_trans = math.ceil(pbs_vol/300)
        pip.pick_up_tip()
        for t in range(num_trans):
            if t < num_trans - 1:
                t_vol = 300
            else:
                t_vol = 300 if pbs_vol % 300 == 0 else pbs_vol % 300
            pip.aspirate(t_vol, pbs)
            pip.move_to(pbs.top(15))
            pip.dispense(t_vol, mm.bottom(5))
        if p10.tip_attached:
            p10.drop_tip()
        if not p300.tip_attached:
            p300.pick_up_tip()
        p300.mix(5, mix_vol, mm.bottom(5))
        p300.drop_tip()
        robot.comment('Proceed with Flow Cytometry Staining.')
    else:
        robot.comment('Tube volume exceeds 100ul*(number of samples). No PBS \
will be added for volume adjustment. Proceed with Flow Cytometry Staining.')
