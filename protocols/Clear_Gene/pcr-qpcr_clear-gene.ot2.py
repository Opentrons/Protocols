from opentrons import instruments, labware

# containers
temp_deck = labware.load('PCR-strip-tall', '4')
p50_tips = labware.load('tiprack-200ul', '5')
temp_deck2 = labware.load('96-PCR-flat', '7')
p10_tips = labware.load('tiprack-10ul', '8')

# instrument setup
p50 = instruments.P50_Multi(
    tip_racks=[p50_tips],
    mount='left')

p10 = instruments.P10_Single(
    tip_racks=[p10_tips],
    mount='right')

# reagents setup and variables
mm_strip = temp_deck.cols('5', to='8')

# protocol begins

# transfer reagent mix to master mix tubes
p50.pick_up_tip()
for col in mm_strip:
    p50.aspirate(40, temp_deck.wells('A1'))
    p50.dispense(36, col[0])
    p50.dispense(4, temp_deck.wells('A1'))
p50.drop_tip()

# transfer SYBR to master mix tubes
p50.pick_up_tip()
for col in mm_strip:
    p50.aspirate(50, temp_deck.wells('A2'))
    p50.dispense(45, col[0])
    p50.dispense(5, temp_deck.wells('A2'))
p50.drop_tip()

# transfer template to master mix tubes
start = ['A5', 'A6', 'A7', 'A8']
end = ['E5', 'E6', 'E7', 'E8']


for well_index, well in enumerate(temp_deck.wells('A3', to='D3')):
    p10.transfer(4.5, well, temp_deck.wells(
        start[well_index], to=end[well_index]), new_tip='always')

p10.transfer(4.5, temp_deck.wells('E3'), temp_deck.wells('F5', to='H5'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('E3'), temp_deck.wells('F6', to='H6'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('F3'), temp_deck.wells('F7', to='H7'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('F3'), temp_deck.wells('F8', to='H8'),
             new_tip='always')

# transfer primers to master mix tubes
p10.transfer(4.5, temp_deck.wells('A4'),
             temp_deck.wells('A5', 'F5', 'A6', 'A7', 'F7', 'A8'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('B4'),
             temp_deck.wells('B5', 'G5', 'B6', 'B7', 'G7', 'B8'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('C4'),
             temp_deck.wells('C5', 'H5', 'C6', 'C7', 'H7', 'C8'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('D4'),
             temp_deck.wells('D5', 'D6', 'F6', 'D7', 'D8', 'F8'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('E4'),
             temp_deck.wells('E5', 'E6', 'G6', 'E7', 'E8', 'G8'),
             new_tip='always')
p10.transfer(4.5, temp_deck.wells('F4'),
             temp_deck.wells('H6', 'H8'), new_tip='always')

# mix master mix tubes
for col in mm_strip:
    p50.pick_up_tip()
    p50.mix(3, 45, col[0])
    p50.drop_tip()

# transfer master mix to 96 well plate
top_row = temp_deck2.rows('A')
col = 0

for strip_index in range(4):
    p50.pick_up_tip()
    p50.aspirate(50, mm_strip[strip_index][0])
    p50.dispense(5, mm_strip[strip_index][0])
    p50.dispense(20, top_row[col])
    p50.dispense(20, top_row[col + 1])
    p50.dispense(5, mm_strip[strip_index][0])

    p50.aspirate(30, mm_strip[strip_index][0])
    p50.dispense(5, mm_strip[strip_index][0])
    p50.dispense(20, top_row[col + 2])
    p50.drop_tip()
    col = col + 3
