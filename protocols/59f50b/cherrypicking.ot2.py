from opentrons import labware, instruments, robot
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Mastermix Assay from .csv',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
pool_name = 'thermofisherabgene_96_wellplate_800ul_deep'
if pool_name not in labware.list():
    labware.create(
        pool_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=27,
        volume=800
    )

thermo_name = 'thermofisherabgene_96_wellplate_1.2ml_deep'
if thermo_name not in labware.list():
    labware.create(
        thermo_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=7,
        depth=39.35,
        volume=1200
    )

lgc_name = 'LGC_96_wellplate_450ul_NAP40000N'
if lgc_name not in labware.list():
    labware.create(
        lgc_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8,
        depth=10,
        volume=450
    )

example_csv = """Deck Position,Well,Pooled Plate (Position 10),Volume (ul)
1,A7,A1,8.7
1,C12,A3,8.7
1,E4,A11,8.7
1,G2,A12,6
1,G8,B5,6
1,H8,B6,6
1,H9,B7,6
1,H4,B10,6
2,B6,B11,6
2,B12,B12,6
2,C9,H1,6
"""


def run_custom_protocol(
    p10_single_mount: StringSelection('right', 'left') = 'right',
    donor_plate_type: StringSelection(
        'NAP40000L (Thermo AB-0564)',
        'NAP40000N') = 'NAP40000L (Thermo AB-0564)',
    input_csv: FileInput = example_csv,
    touch_tip_on_transfer: StringSelection('yes', 'no') = 'yes'
):

    # parse
    trans_data = [
        [val.strip() for val in line.split(',')]
        for line in input_csv.splitlines()[1:] if line
    ]
    if donor_plate_type == 'NAP40000L (Thermo AB-0564)':
        donor_name = thermo_name
    else:
        donor_name = lgc_name
    donor_plates = {}
    for t in trans_data:
        slot = t[0]
        if slot not in donor_plates:
            donor_plates[slot] = labware.load(
                donor_name, slot, 'donor plate ' + slot)

    # checks
    if len(donor_plates) > 9:
        raise Exception('Maximum of 9 deck positions for donor plates.')

    # method to find slot for tiprack and pool plate

    def find_available_slot(lw_type, lw_name):
        for i, c in enumerate(robot.deck.get_children_list()):
            if not c.has_children():
                return labware.load(lw_type, str(i+1), lw_name)
        return('No available slots remaining.')

    # load labware
    pool_plate = find_available_slot(pool_name, 'pool plate')
    tiprack10 = find_available_slot(
        'opentrons_96_tiprack_10ul', '10ul tiprack')

    # pipette
    p10 = instruments.P10_Single(mount=p10_single_mount, tip_racks=[tiprack10])

    # perform transfers:
    for t in trans_data:
        vol = float(t[3])
        source = donor_plates[t[0]].wells(t[1].upper())
        dest = pool_plate.wells(t[2])

        p10.pick_up_tip()
        p10.aspirate(vol, source)
        if touch_tip_on_transfer == 'yes':
            p10.touch_tip(source)
        p10.dispense(vol, dest.bottom(2))
        p10.blow_out(dest.bottom(5))
        p10.drop_tip()
