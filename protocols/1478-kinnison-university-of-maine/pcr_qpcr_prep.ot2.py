from opentrons import labware, instruments

metadata = {
    'protocolName': 'PCR/qPCR prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
    }

# labware setup
sample_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '1')
plate = labware.load('96-flat', '2')
reagent_rack = labware.load('opentrons-tuberack-2ml-eppendorf', '5')
tiprack_10 = labware.load('tiprack-10ul', '6')
tiprack_50 = labware.load('opentrons-tiprack-300ul', '7')

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

p50 = instruments.P50_Single(
    mount='right',
    tip_racks=[tiprack_50])

# reagent setup
mastermix_1 = reagent_rack.wells('A1')
mastermix_2 = reagent_rack.wells('B1')
mastermix_3 = reagent_rack.wells('C1')
water = reagent_rack.wells('D1')
control_dnas = reagent_rack.wells('A2', length=3)
gblocks = reagent_rack.wells('D2', length=6)

# transfer master mix 1
p50.distribute(
    17, mastermix_1, plate.rows('A', to='F'), blow_out=mastermix_1)

# transfer master mix 2
p50.distribute(
    17, mastermix_2, plate.rows('H').wells('7', to='12'), blow_out=mastermix_2)

# transfer master mix 3
p50.distribute(
    19, mastermix_3, plate.rows('H').wells('1', to='6'), blow_out=mastermix_3)

sample_dests = [row.wells(index, length=3)
                for row in plate.rows('A', to='F')
                for index in range(0, 12, 3)]

sample_sources = [well for well in sample_rack.wells()]

# transfer and mix samples in triplicate
for source, dest in zip(sample_sources, sample_dests):
    p10.pick_up_tip()
    p10.distribute(3, source, dest, disposal_vol=0, new_tip='never')
    for well in dest:
        p10.mix(3, 10, well)
        p10.blow_out(well.top())
    p10.drop_tip()

# transfer water and control DNAs
p10.pick_up_tip()
p10.transfer(1, water, plate.wells('H7', 'H8'), new_tip='never')
p10.mix(3, 10, plate.wells('H8'))
p10.blow_out(plate.wells('H8').top())
p10.mix(3, 10, plate.wells('H7'))
p10.blow_out(plate.wells('H7').top())
p10.drop_tip()

for control, dest in zip(control_dnas, plate.rows('H').wells('10', to='12')):
    p10.transfer(1, control, dest, mix_after=(3, 10))

# transfer gblocks
for gblock, dest in zip(gblocks, plate.rows('H').wells('1', to='6')):
    p10.transfer(1, gblock, dest, mix_after=(3, 10))
