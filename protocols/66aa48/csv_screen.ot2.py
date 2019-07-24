from opentrons import labware, instruments
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'CSV Consolidation',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware
source_plate = labware.load('96-PCR-tall', '1', 'source plate')
dest_rack = labware.load(
    'opentrons-tuberack-2ml-eppendorf',
    '4',
    'Eppendorf tuberack for pools'
)

inactive_ex = """A5
A6
B1
"""

decrease_ex = """A2
A3
A4
A7
A8
B3
B5
"""

no_change_ex = """B4
B6
"""

increase_ex = """A1
B2
"""


def run_custom_protocol(
        volume_of_each_mutant_to_transfer: float = 50,
        pipette_mount: StringSelection('left', 'right') = 'left',
        tip_strategy: StringSelection(
            'one tip per pool',
            'new tips for each transfer') = 'one tip per pool',
        inactive_CSV: FileInput = inactive_ex,
        decrease_CSV: FileInput = decrease_ex,
        no_change_CSV: FileInput = no_change_ex,
        increase_CSV: FileInput = increase_ex
):

    if volume_of_each_mutant_to_transfer < 5:
        raise Exception('Invalid volume selection.')

    tips = labware.load('opentrons-tiprack-300ul', '2')
    p50 = instruments.P50_Single(mount=pipette_mount, tip_racks=[tips])

    # parse files and perform pooling
    touch = False if volume_of_each_mutant_to_transfer > 10 else True
    for csv, dest in zip(
            [inactive_CSV, decrease_CSV, no_change_CSV, increase_CSV],
            [well for well in dest_rack.wells('A1', length=4)]
    ):
        sources = [source_plate.wells(line.split(',')[0])
                   for line in csv.splitlines() if line]
        d_offset = (dest, dest.from_center(r=1.0, h=0.9, theta=0))
        if tip_strategy == 'one tip per pool':
            p50.pick_up_tip()
        for s in sources:
            if not p50.tip_attached:
                p50.pick_up_tip()
            p50.transfer(
                volume_of_each_mutant_to_transfer,
                s,
                dest,
                new_tip='never'
            )
            if touch:
                p50.move_to(d_offset)
            p50.blow_out(dest.top())
            if tip_strategy == 'one tip per pool':
                p50.drop_tip()
        if p50.tip_attached:
            p50.drop_tip()
