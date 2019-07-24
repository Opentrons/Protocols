from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'CSV Sample Recombination',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
custom_rack_name = 'tuberack-6x8-500ul'
if custom_rack_name not in labware.list():
    labware.create(
        custom_rack_name,
        grid=(8, 6),
        spacing=(15, 12),
        diameter=8,
        depth=30,
        volume=500
    )

custom_tips_name = 'Greiner-Sapphire-tiprack-10ul'
if custom_tips_name not in labware.list():
    labware.create(
        custom_tips_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=3,
        depth=50
    )

# load labware
rack = labware.load(custom_rack_name, '1', 'source tube rack')
tips10 = labware.load(custom_tips_name, '2')

example_csv = """12.6,12.4,16.5,0,4.03,4.1
13.7,11.6,14,3.13,4.04,3.92
14.8,13.2,15.4,2.74,2.91,3.86
12.7,14.2,13.6,3.63,2.89,4.39
12.8,16.1,16.1,2.64,2.91,3.48
12.2,13.1,13.9,3.56,2.95,4.4
"""


def run_custom_protocol(
        CSV_file: FileInput = example_csv,
        pipette_mount: StringSelection('left', 'right') = 'right',
        destination_tube_type: StringSelection(
            '1.5ml Eppendorf', '1.5ml screwcap') = '1.5ml screwcap'
):
    # pipettes
    p10 = instruments.P10_Single(mount=pipette_mount, tip_racks=[tips10])

    if destination_tube_type.split(' ')[-1] == 'Eppendorf':
        dest_rack = labware.load(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '4',
            'rack for destination tube'
        )
        h = 2.3
    else:
        dest_rack = labware.load(
            'opentrons_24_tuberack_generic_2ml_screwcap',
            '4',
            'rack for destination tube'
        )
        h = 3
    dest_tube = dest_rack.wells('A1')
    dest_offset = (dest_tube, dest_tube.from_center(r=1.0, h=0, theta=0))

    # parse csv
    transfer_data = [
        [float(vol) for vol in line.split(',')]
        for line in example_csv.splitlines()
    ]
    all_wells = [[well for well in row] for row in rack.rows()]

    # perform transfers
    for s_row, vol_row in zip(all_wells, transfer_data):
        for well, vol in zip(s_row, vol_row):
            if vol != 0:
                p10.pick_up_tip()
                if vol > 10:
                    p10.transfer(
                        vol,
                        well,
                        dest_tube.bottom(h),
                        new_tip='never'
                    )
                else:
                    source_offset = (
                        well,
                        well.from_center(r=1.0, h=0.9, theta=0)
                    )
                    p10.aspirate(vol, well)
                    p10.move_to(source_offset)
                    p10.dispense(vol, dest_tube.bottom(h))
                p10.move_to(dest_offset)
                p10.blow_out()
                p10.drop_tip()
