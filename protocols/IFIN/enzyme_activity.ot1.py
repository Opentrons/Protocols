from opentrons import containers, instruments

plate_a = containers.load('96-flat', 'A1')
plate_b = containers.load('96-flat', 'B1')
trash = containers.load('trash-box', 'A2')
tiprack1 = containers.load('tiprack-200ul', 'B2')
tiprack2 = containers.load('tiprack-200ul', 'C2')


m200 = instruments.Pipette(
    axis='a',
    name='m200',
    max_volume=200,
    min_volume=20,
    channels=8,
    trash_container=trash,
    tip_racks=[tiprack1, tiprack2]
    )

m200.pick_up_tip()
m200.transfer(35, plate_a.rows('10'), plate_b.rows('1', length=4),
              new_tip='never')
m200.transfer(35, plate_a.rows('11'), plate_b.rows('5', length=4),
              new_tip='never')
m200.transfer(35, plate_a.rows('12'), plate_b.rows('9', length=4),
              new_tip='never')
m200.drop_tip()

m200.pick_up_tip()
m200.transfer(20, plate_a.rows('7'), plate_b.rows('7', length=6),
              mix_after=(2, 20), new_tip='never')
m200.transfer(20, plate_a.rows('9'), plate_b.rows('1', length=6),
              mix_after=(2, 20), new_tip='never')
m200.drop_tip()

m200.transfer(20, plate_a.rows('8'), plate_b.rows(), mix_after=(2, 20))

m200.transfer(20, plate_a.rows('1'), plate_b.rows('1', '7'), mix_after=(2, 20),
              new_tip='always')

m200.transfer(20, plate_a.rows('2'), plate_b.rows('2', '8'), mix_after=(2, 20),
              new_tip='always')

m200.transfer(20, plate_a.rows('3'), plate_b.rows('3', '9'), mix_after=(2, 20),
              new_tip='always')

m200.transfer(20, plate_a.rows('4'), plate_b.rows('4', '10'),
              mix_after=(2, 20), new_tip='always')

m200.transfer(20, plate_a.rows('1'), plate_b.rows('5', '11'),
              mix_after=(2, 20), new_tip='always')

m200.transfer(20, plate_a.rows('1'), plate_b.rows('6', '12'),
              mix_after=(2, 20), new_tip='always')
