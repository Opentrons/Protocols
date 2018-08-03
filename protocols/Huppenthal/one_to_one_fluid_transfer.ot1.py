from opentrons import containers, instruments

olympus_test_rack = 'olympus_test_rack'
if olympus_test_rack not in containers.list():
    containers.create(
        olympus_test_rack,
        grid=(10, 1),
        spacing=(17.5, 0),
        diameter=14,
        depth=75)

tiprack_1000 = containers.load('tiprack-1000ul', 'C2')
trough = containers.load('trough-1row-25ml', 'D1')
testrack = containers.load(olympus_test_rack, 'A1')

trash = containers.load('trash-box', 'A2')

p1000 = instruments.Pipette(
    name='p1000',
    channels=1,
    axis='a',
    max_volume=1000,
    tip_racks=[tiprack_1000],
    trash_container=trash)

p1000.transfer(875, trough['A1'], testrack.wells(), new_tip='always')
