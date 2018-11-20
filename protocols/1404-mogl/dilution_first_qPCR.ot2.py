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
p50.distribute(16, master_mix, plate_2.rows('A', to='F'), disposal_vol=0)


# transfer standards
all_wells = [well for row in plate_1.rows() for well in row]
dests = [all_wells[i:i+3] for i in range(0, 18, 3)]
for standard, dest in zip(strips.cols('12')[:6], dests):
    for well in dest:
        p10.pick_up_tip()
        p10.transfer(4, standard, well, mix_after=(5, 10), new_tip='never')
        p10.blow_out(well)
        p10.drop_tip()

# transfer samples
dests_1 = [all_wells[i:i+3] for i in range(18, 61, 6)]
dests_2 = [all_wells[i:i+3] for i in range(21, 64, 6)]
for index, col in enumerate(strips.cols[1:9]):
    for well_1 in dests_1[index]:
        p10.pick_up_tip()
        p10.transfer(
            4, col.wells('D'), well_1, mix_after=(5, 10), new_tip='never')
        p10.blow_out(well_1)
        p10.drop_tip()

    for well_2 in dests_2[index]:
        p10.pick_up_tip()
        p10.transfer(
            4, col.wells('G'), well_2, mix_after=(5, 10), new_tip='never')
        p10.blow_out(well_2)
        p10.drop_tip()
