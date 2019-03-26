from opentrons import labware, instruments

metadata = {
    'protocolName': 'Protein crystallization screens',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

block_name = 'starlab-96-deep-well-block'
if block_name not in labware.list():
    labware.create(
        block_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.4,
        depth=42.2,
        volume=2200
    )

tuberack_name = 'custom-24-tube-rack-holder-15ml'
if tuberack_name not in labware.list():
    labware.create(
        tuberack_name,
        grid=(6, 4),
        spacing=(20.3, 20.3),
        diameter=16.5,
        depth=101,
        volume=1300
    )

# labware setup
deep_blocks = [labware.load(block_name, slot)
               for slot in ['1', '2', '3', '5', '6', '9']]
tuberacks = [labware.load(tuberack_name, slot)
             for slot in ['10', '11', '7', '8']]
tiprack = labware.load('tiprack-1000ul', '4')

# instruments setup
p1000 = instruments.P1000_Single(
    mount='left',
    tip_racks=[tiprack])

# define tube position in 96-well format
tubes = []
for racks in (tuberacks[:2], tuberacks[2:]):
    for row_1, row_2 in zip(racks[0].rows(), racks[1].rows()):
        [tubes.append(well) for well in row_1]
        [tubes.append(well) for well in row_2]

tube_dests = [
    [block.rows(row_index).wells(well_index) for block in deep_blocks]
    for row_index in range(8) for well_index in range(12)
    ]

for tube, dests in zip(tubes, tube_dests):
    p1000.pick_up_tip()
    for dest in dests:
        for _ in range(2):
            p1000.set_flow_rate(aspirate=500, dispense=500)
            p1000.aspirate(750, tube)
            p1000.delay(seconds=0.5)
            p1000.touch_tip()
            p1000.dispense(750, dest)
            p1000.delay(seconds=0.5)
            p1000.set_flow_rate(dispense=1500)
            p1000.blow_out(dest.top())
    p1000.drop_tip()
