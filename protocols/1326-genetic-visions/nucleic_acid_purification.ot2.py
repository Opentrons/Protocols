from opentrons import labware, instruments

trough_name = 'beckman-trough-4row'
if trough_name not in labware.list():
    labware.create(
        trough_name,
        grid=(4, 1),
        spacing=(24, 0),
        depth=24.8,
        diameter=2,
        volume=40700)

elution_plate = labware.load('96-flat', '1')
etoh_plate = labware.load('96-deep-well', '2')
buffer_1_plate = labware.load('96-deep-well', '3')
buffer_2_plate = labware.load('96-deep-well', '6')
trough = labware.load(trough_name, '5')

tiprack = labware.load('opentrons-tiprack-300ul', '4')

# reagent setup
tris_hcl = trough.wells('A1')
etoh = trough.wells('A2')
wash_buffer_1 = trough.wells('A3')
wash_buffer_2 = trough.wells('A4')

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack])

tip_start_column = '4'

# distribute 65 uL Tris-HCl to elution plate
m300.pick_up_tip()
for well in elution_plate.rows(0):
    if m300.current_volume < 65:
        m300.aspirate(tris_hcl)
    m300.dispense(65, well.top())
m300.drop_tip()

# distribute 200 uL EtOH to EtOH plate
m300.pick_up_tip()
for well in etoh_plate.rows(0):
    if m300.current_volume < 200:
        m300.aspirate(etoh)
    m300.dispense(200, well.top())
m300.drop_tip()

# distribute 500 uL of wash buffer to wash buffer 1 plate
m300.pick_up_tip()
for well in buffer_1_plate.rows(0):
    m300.transfer(500, wash_buffer_1, well.top(), new_tip='never')
m300.drop_tip()

# distribute 500 uL of wash buffer to wash buffer 2 plate
m300.pick_up_tip()
for well in buffer_2_plate.rows(0):
    m300.transfer(500, wash_buffer_2, well.top(), new_tip='never')
m300.drop_tip()
