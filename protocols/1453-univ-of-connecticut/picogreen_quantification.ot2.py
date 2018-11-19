from opentrons import labware, instruments

# labware setup
sample_plate = labware.load('96-flat', '5')
quanti_plate_1 = labware.load('96-flat', '4')
quanti_plate_2 = labware.load('96-flat', '6')
quanti_plates = [quanti_plate_1, quanti_plate_2]

trough = labware.load('trough-12row', '2')
tuberack = labware.load('opentrons-tuberack-2ml-screwcap', '8')

tiprack_300 = labware.load('opentrons-tiprack-300ul', '7')
tiprack_10 = labware.load('tiprack-10ul', '9')


# reagent setup
TE_buffer = trough.wells('A1')
picogreen = trough.wells('A2')
DNA_standard = tuberack.wells('A1')

# instrument setup
m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack_300])

m10 = instruments.P10_Multi(
    mount='right',
    tip_racks=[tiprack_10])

# perform DNA standard serial dilution - remove the second tip
m300.distribute(
    100,
    TE_buffer,
    [plate.cols('1') for plate in quanti_plates])


for tip, plate in zip(tiprack_300.wells('H2', 'G2'), quanti_plates):
    m300.pick_up_tip(tip)
    m300.transfer(150, DNA_standard, plate.wells('B1'), new_tip='never')
    for source, dest in zip(
            plate.wells('B1', to='G1'), plate.wells('C1', to='H1')):
        m300.transfer(50, source, dest, mix_after=(5, 50), new_tip='never')
    m300.transfer(
        50, plate.wells('H1'), m300.trash_container.top(), new_tip='never')
    m300.drop_tip()

# distribute TE to sample destination wells
m300.start_at_tip(tiprack_300.cols('3'))
TE_dest = [col for plate in quanti_plates for col in plate.cols('2', length=6)]
m300.distribute(99, TE_buffer, TE_dest)

# transfer samples
sample_dest = [col
               for plate in quanti_plates for col in plate.cols('2', length=6)]
for source, dest in zip(sample_plate.cols(), sample_dest):
    m10.pick_up_tip()
    m10.transfer(1, source, dest, mix_after=(5, 10), new_tip='never')
    m10.blow_out(dest)
    m10.drop_tip()

# distribute PicoGreen solution to all occupied wells
pico_dest = [col[0].top()
             for plate in quanti_plates
             for col in plate.cols('1', to='7')]
m300.pick_up_tip()
m300.aspirate(picogreen)
for well in pico_dest:
    if m300.current_volume <= 100:
        m300.aspirate(picogreen)
    m300.dispense(100, well)
m300.drop_tip()
