from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Cherrypicking from CSV',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
deep_name = 'corning_96_wellplate_2ml_deep'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=42.037,
        volume=2000
    )

# load static labware
tiprack = labware.load('opentrons_96_tiprack_1000ul', '1', '1000ul tips')


example_csv = """Source_Well,Source_position,Source_position_name,\
Destination_position,Destination_Well,Destination_labware,Volume
A1,10,compounds1,8,A1,array1,1000
A1,10,compounds1,9,A1,array2,1000
A1,10,compounds1,5,A1,array3,1000
A1,10,compounds1,6,A1,array4,1000
A1,10,compounds1,2,A1,array5,1000
A1,10,compounds1,3,A1,array6,1000
A2,10,compounds1,8,B1,array1,1000
A2,10,compounds1,9,B1,array2,1000
A2,10,compounds1,5,B1,array3,1000
A2,10,compounds1,6,B1,array4,1000
A2,10,compounds1,2,B1,array5,1000
A2,10,compounds1,3,B1,array6,1000
A3,10,compounds1,8,C1,array1,1000
"""


def run_custom_protocol(
        p1000_mount: StringSelection('right', 'left') = 'right',
        input_file: FileInput = example_csv,
        starting_tip_well: str = 'A1'
):
    # parse
    trans_data = [
        [val.strip() for val in line.split(',')]
        for line in input_file.splitlines()[1:] if line
    ]

    # pipette
    p1000 = instruments.P1000_Single(mount=p1000_mount, tip_racks=[tiprack])

    all_tips = [tip.get_name() for tip in tiprack.get_all_children()]
    if starting_tip_well.strip().upper() not in all_tips:
        raise Exception('Invalid starting tip well \'\
' + starting_tip_well + '\'')
    p1000.start_at_tip(tiprack.wells(starting_tip_well.strip().upper()))
    tip_count = all_tips.index(starting_tip_well.strip().upper())

    def pick_up():
        nonlocal tip_count
        if tip_count == 96:
            robot.pause('Refill 1000ul tiprack in slot 11 before resuming.')
            tip_count = 0
            p1000.reset()
        tip_count += 1
        p1000.pick_up_tip()

    # initialize data
    tuberacks = {}
    deep_blocks = {}

    # perform transfers
    s_prev = trans_data[0][0].strip().upper()
    pick_up()
    for t in trans_data:
        s_slot = t[1].strip()
        if s_slot not in tuberacks:
            rack_num = t[2].split('compounds')[-1]
            tuberacks[s_slot] = labware.load(
                'opentrons_6_tuberack_falcon_50ml_conical',
                s_slot,
                'compound rack ' + rack_num
            )

        d_slot = t[3].strip()
        if d_slot not in deep_blocks:
            block_num = t[5].split('array')[-1]
            deep_blocks[d_slot] = labware.load(
                deep_name,
                d_slot,
                'array ' + block_num
            )

        # setup source and destination, replacing tip if new source
        s_well = t[0].strip().upper()
        if s_well != s_prev:
            p1000.drop_tip()
            pick_up()
            s_prev = s_well
        source = tuberacks[s_slot].wells(s_well)
        d_well = t[4].strip().upper()
        dest = deep_blocks[d_slot].wells(d_well)
        vol = float(t[6].strip())

        # perform transfer
        p1000.transfer(vol, source, dest, new_tip='never')
        p1000.blow_out()

    p1000.drop_tip()
