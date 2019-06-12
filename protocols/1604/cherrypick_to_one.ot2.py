from opentrons import labware, instruments
from otcustomizers import StringSelection, FileInput

metadata = {
    'protocolName': 'Cherrypick Multiple Wells to Master Tube',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
plate = labware.load('biorad-hardshell-96-PCR', '1')
tubes = labware.load('opentrons-tuberack-2ml-eppendorf', '2')
master = tubes.wells('A1')

example_csv = """A1,14.2
A2,8.1
A3,4.1
A4,9.8
A5,4.3
A6,3.9

"""


def run_custom_protocol(
        CSV_file: FileInput = example_csv,
        single_channel_pipette_type: StringSelection(
            'P10', 'P50', 'P300', 'P1000') = 'P10',
        pipette_mount: StringSelection('right', 'left') = 'right',
        tip_use_strategy: StringSelection(
            'same tip', 'new tip for each transfer') = 'same tip'
):

    # choose and load pipette
    if single_channel_pipette_type == 'P10':
        tips = labware.load('tiprack-10ul', '3')
        pipette = instruments.P10_Single(
                                    mount=pipette_mount, tip_racks=[tips])
    elif single_channel_pipette_type == 'P50':
        tips = labware.load('opentrons-tiprack-300ul', '3')
        pipette = instruments.P50_Single(
                                    mount=pipette_mount, tip_racks=[tips])
    elif single_channel_pipette_type == 'P300':
        tips = labware.load('opentrons-tiprack-300ul', '3')
        pipette = instruments.P300_Single(
                                    mount=pipette_mount, tip_racks=[tips])
    else:
        tips = labware.load('tiprack-1000ul', '3')
        pipette = instruments.P1000_Single(
                                    mount=pipette_mount, tip_racks=[tips])

    # parse csv
    transfer_info = [line.split(',')
                     for line in example_csv.splitlines() if line]

    new_tip = 'never' if tip_use_strategy == 'same tip' else 'always'

    if new_tip == 'never':
        pipette.pick_up_tip()

    for t in transfer_info:
        well = t[0].strip()
        vol = float(t[1].strip())
        pipette.transfer(
            vol,
            plate.wells(well),
            master,
            blow_out=True,
            new_tip=new_tip
            )

    if new_tip == 'never':
        pipette.drop_tip()
