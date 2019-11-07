from opentrons import labware, instruments
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
tuberack = labware.load(rack_name, '2', 'source sample tubes')
tiprack300 = labware.load('opentrons_96_tiprack_300ul', '3', '300ul tiprack')
dmso = labware.load(
    'usascientific_12_reservoir_22ml', '4', 'reservoir for DMSO').wells()[0]
tiprack10 = labware.load('opentrons_96_tiprack_10ul', '6', '10ul tiprack')

example_csv = """Well,Pos,Tube BC
A01,1,0357024553
B01,13,0357024554
H01,25,0357024555
D01,37,0357024556
E01,49,0357024557
F01,61,0357024558
G01,73,0357024559
H01,85,0357024560
A02,2,0357024561
B02,14,0357024562
C02,26,0357024563
D02,38,0357024564
E02,50,0357024565
B03,15,0357024570

"""


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        p10_single_mount: StringSelection('left', 'right') = 'left',
        input_csv: FileInput = example_csv
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

    tube_locs = [
        tuberack.wells(parse_well(line.split(',')[0]))
        for line in input_csv.splitlines()[1:] if line
    ]

    # transfer DMSO to receiving columns based on .csv file using P300-multi
    num_cols = math.ceil(len(tube_locs)/8)
    dmso_dests = plate.rows('A')[:num_cols]
    m300.pick_up_tip()
    for d in dmso_dests:
        m300.transfer(198, dmso, d.bottom(2), new_tip='never')
        m300.blow_out(d.top(-2))
    m300.drop_tip()

    # transfer sample to corresponding plate location
    for s, d in zip(tube_locs, plate.wells()[:len(tube_locs)]):
        p10.pick_up_tip()
        p10.aspirate(2, s)
        p10.touch_tip(s)
        p10.aspirate(8, d.bottom(2))
        p10.dispense(10, d.bottom(2))
        p10.blow_out(d.bottom(5))
        p10.drop_tip()
