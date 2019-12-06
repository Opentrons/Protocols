from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput
import math

metadata = {
    'protocolName': 'Cherrypicking',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
plate_name = 'greinerbioone_96_wellplate_340ul'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.96,
        depth=10.9,
        volume=340
    )

rack_name = 'thermofisher_96_tuberack_500ul'
if rack_name not in labware.list():
    labware.create(
        rack_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7.4,
        depth=29.1,
        volume=500
    )

# load labware
plate = labware.load(plate_name, '1', 'destination sample plate')
solvent = labware.load(
    'usascientific_12_reservoir_22ml', '9', 'reservoir for solvent').wells()[0]
tiprack300 = labware.load('opentrons_96_tiprack_300ul', '10', '300ul tiprack')
tiprack10 = labware.load('opentrons_96_tiprack_10ul', '11', '10ul tiprack')

example_csv = """Source Well,Source Slot,Pos,Tube BC
A01,2,1,0357024553
B01,3,13,0357024554
H01,3,25,0357024555
D01,5,37,0357024556
E01,4,49,0357024557
F01,2,61,0357024558
G01,3,73,0357024559
H01,6,85,0357024560
A02,2,2,0357024561
B02,7,14,0357024562

"""


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        p10_single_mount: StringSelection('left', 'right') = 'left',
        input_csv: FileInput = example_csv,
        volume_of_solvent_in_ul: float = 198,
        volume_of_sample_in_ul: float = 2
):
    # check
    if p300_multi_mount == p10_single_mount:
        raise Exception('Pipette mounts cannot match.')

    # pipettes
    m300 = instruments.P300_Multi(
        mount=p300_multi_mount, tip_racks=[tiprack300])
    p10 = instruments.P10_Single(
        mount=p10_single_mount, tip_racks=[tiprack10])

    def parse_well(well_name):
        stripped = well_name.strip()
        return stripped[0].upper() + str(int(stripped[1:]))

    # parse
    trans_data = [
        [val.strip() for val in line.split(',')]
        for line in input_csv.splitlines()[1:]
        if line and line.split(',')[0].strip()  # ignore empty lines/sources
    ]

    # transfer solvent to receiving columns based on .csv file using P300-multi
    num_cols = math.ceil(len(trans_data)/8)
    solvent_dests = plate.rows('A')[:num_cols]
    m300.pick_up_tip()
    for d in solvent_dests:
        m300.transfer(
            volume_of_solvent_in_ul, solvent, d.bottom(2), new_tip='never')
        m300.blow_out(d.top(-2))
    m300.drop_tip()

    # parse and transfer
    valid_sources = []
    for i, line in enumerate(trans_data):
        slot = line[1]
        lw = robot.deck.get_child_by_name(slot).get_children_list()
        if not lw:
            s_rack = labware.load(rack_name, slot, 'source rack ' + slot)
        elif lw[0].get_type() != rack_name:
            raise Exception(
                'Slot ' + slot + ' occupied by ' + lw[0].get_type())
        else:
            s_rack = lw[0]
        if not valid_sources:
            valid_sources = [
                well.get_name() for well in s_rack.get_all_children()]
        source_name = parse_well(line[0])
        if source_name not in valid_sources:
            raise Exception('Invalid source well ' + source_name)

        # perform transfer
        s = s_rack.wells(source_name)
        d = plate.wells()[i]
        p10.pick_up_tip()
        p10.aspirate(volume_of_sample_in_ul, s)
        p10.touch_tip(s)
        p10.aspirate(10-volume_of_sample_in_ul, d.bottom(2))
        p10.dispense(10, d.bottom(2))
        p10.blow_out(d.bottom(5))
        p10.drop_tip()
