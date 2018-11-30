from opentrons import labware, instruments, modules

# labware setup
strips = labware.load('PCR-strip-tall', '1')
temp_1 = labware.load('tempdeck', '2')
plate_1 = labware.load('96-flat', '2', share=True)

temp_deck = modules.load('tempdeck', '4')
tuberack = labware.load('opentrons-aluminum-block-2ml-eppendorf', '4',
                        share=True)
trough = labware.load('trough-12row', '5')

tiprack_50 = labware.load('opentrons-tiprack-300ul', '9')
tiprack_10 = labware.load('tiprack-10ul', '6')

# reagent setup
water = trough.wells('A1')
master_mix = tuberack.wells('A1')
standards = strips.cols('12')[:6]

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack_50])

temp_deck.set_temperature(4)
temp_deck.wait_for_temp()

# add water with p50
p50.pick_up_tip()
p50.transfer(49, water, strips.rows('A').wells('2', to='9'), new_tip='never')
p50.transfer(45, water, strips.rows('D').wells('2', to='9'), new_tip='never')
p50.transfer(20, water, strips.rows('E').wells('2', to='9'), new_tip='never')
p50.transfer(20, water, strips.rows('F').wells('2', to='9'), new_tip='never')
p50.drop_tip()

# add water with p10
p10.pick_up_tip()
p10.transfer(9, water, strips.rows('B').wells('2', to='9'), new_tip='never')
p10.transfer(9, water, strips.rows('C').wells('2', to='9'), new_tip='never')
p10.transfer(5, water, strips.rows('G').wells('2', to='9'), new_tip='never')
p10.drop_tip()

# transfer dilute samples down columns
for sample, col in zip(strips.cols(0), strips.cols(1, length=8)):
    sources = col.wells('A', to='C')
    dests = col.wells('B', to='D')
    vols = [1, 1, 5]
    p10.pick_up_tip()
    p10.transfer(1, sample, col.wells('A'), mix_after=(5, 10), new_tip='never')
    for vol, source, dest in zip(vols, sources, dests):
        p10.transfer(vol, source, dest, mix_after=(5, 10), new_tip='never')
        p10.blow_out(dest)
    p10.drop_tip()

    sources = col.wells('D', to='F')
    dests = col.wells('E', to='G')
    p50.pick_up_tip()
    for source, dest in zip(sources, dests):
        p50.transfer(20, source, dest, mix_after=(5, 25), new_tip='never')
        p50.blow_out(dest)
    p50.drop_tip()

# distribute master mix
p50.pick_up_tip()
for index, row in enumerate(plate_1.rows()):
    if index == 6 or index == 7:
        dest = row.wells('1', length=6)
    else:
        dest = row.wells('1', length=9)
    p50.distribute(6, master_mix, dest, disposal_vol=0, new_tip='never')
p50.drop_tip()

# transfer standards
for standard, row in zip(standards, plate_1.rows()):
    dests = row.wells('7', to='9')
    for well in dests:
        p10.pick_up_tip()
        p10.transfer(4, standard, well, mix_after=(5, 10), new_tip='never')
        p10.blow_out(well)
        p10.drop_tip()

# transfer samples
for sample, row in zip(strips.cols[1:9], plate_1.rows()):
    for well_1 in row.wells('1', to='3'):
        p10.pick_up_tip()
        p10.transfer(
            4, sample.wells('D'), well_1, mix_after=(5, 10), new_tip='never')
        p10.blow_out(well_1)
        p10.drop_tip()

    for well_2 in row.wells('4', to='6'):
        p10.pick_up_tip()
        p10.transfer(
            4, sample.wells('G'), well_2, mix_after=(5, 10), new_tip='never')
        p10.blow_out(well_2)
        p10.drop_tip()
