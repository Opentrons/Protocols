from opentrons import instruments, labware
from otcustomizers import FileInput, StringSelection

metadata = {
    'protocolName': 'Sample Prep with CSV',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# Create labware
tips300 = labware.load('opentrons_96_tiprack_300ul', '2', '300uL Tips')
tips1k = labware.load('opentrons_96_tiprack_1000ul', '1', '1000uL Tips')

tuberack = labware.load(
    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '5', 'Tube Rack'
    )

dw_plate = 'eppendorf_96_wellplate_2000ul'
if dw_plate not in labware.list():
    labware.create(
        dw_plate,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=41.2,
        volume=2000
    )
plate = labware.load(dw_plate, '4', 'Eppendorf Deep Well Plate')

example_csv = """
Well, Trypsin, ABC
A1, 30, 100
A2, 300, 1000
H12, 150, 500

"""


def run_custom_protocol(
    volumes_csv: FileInput = example_csv,
    p300_mount: StringSelection('left', 'right') = 'left',
    p1000_mount: StringSelection('right', 'left') = 'right'
):

    p300 = instruments.P300_Single(
        mount=p300_mount,
        tip_racks=[tips300],
        aspirate_flow_rate=100,
        dispense_flow_rate=150
        )
    p1k = instruments.P1000_Single(
        mount=p1000_mount,
        tip_racks=[tips1k],
        dispense_flow_rate=500
        )

    data = [
        [well, vol300, vol1000]
        for well, vol300, vol1000 in
        [row.split(',') for row in volumes_csv.strip().splitlines() if row]
    ]

    p300ht = 60
    p1kht = 80

    def ht_adj(pip, vol):
        nonlocal p300ht
        nonlocal p1kht

        if pip == p1k:
            if p1kht < 4:
                return p1kht
            else:
                delta_h = 1.1*(vol/607.42)  # pi*r^2 + 10%
                delta_h = round(delta_h, 2)
                p1kht -= delta_h
                return p1kht
        else:
            if p300ht < 4:
                return p300ht
            else:
                delta_h = 1.1*(vol/174.37)  # pi*r^2 + 10%
                delta_h = round(delta_h, 2)
                p300ht -= delta_h
                return p300ht

    src_well1k = tuberack.wells('A3')
    src_well300 = tuberack.wells('A1')

    p1k.pick_up_tip()
    p300.pick_up_tip()

    for well, not_used, vol1000 in data[1:]:
        vol1000 = float(vol1000)
        if well == 'E1':
            src_well1k = tuberack.wells('B3')
            p1kht = 80
        p1k.transfer(
            vol1000,
            src_well1k.bottom(p1kht),
            plate.wells(well).bottom(35),
            new_tip='never'
            )
        p1k.blow_out(plate.wells(well).top())
        ht_adj(p1k, vol1000)

    for well, vol300, not_used in data[1:]:
        vol300 = float(vol300)
        p300.transfer(
            vol300,
            src_well300.bottom(p300ht),
            plate.wells(well).bottom(35),
            new_tip='never'
            )
        p300.blow_out(plate.wells(well).top())
        ht_adj(p300, vol300)

    p1k.drop_tip()
    p300.drop_tip()
