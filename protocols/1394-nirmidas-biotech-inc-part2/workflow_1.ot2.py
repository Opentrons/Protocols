from opentrons import labware, instruments

# labware setup
tuberacks = [labware.load('opentrons-tuberack-2ml-eppendorf', slot)
             for slot in ['1', '2']]
trough = labware.load('trough-12row', '3')

plate1 = labware.load('96-flat', '5')
plate2 = labware.load('96-flat', '6')

tiprack_10 = labware.load('tiprack-10ul', '4')
tiprack_300 = labware.load('opentrons-tiprack-300ul', '8')

# instruments setup
p10 = instruments.P10_Single(
    mount='left',
    tip_racks=[tiprack_10])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])

# reagent setup
buffer_A = trough.wells('A1')
buffer_B = trough.wells('A2')

dest_num = ['1', '2', '4', '5', '7', '8', '10', '11']

m300.pick_up_tip()
for num in dest_num:
    m300.transfer(195, buffer_A, plate1.cols(num), new_tip='never')
m300.drop_tip()

samples = [well for tuberack in tuberacks for well in tuberack.wells()][:40]
sample_dests = [well for num in dest_num
                for well in plate1.cols(num).wells('A', to='E')]

for source, dest in zip(samples, sample_dests):
    p10.transfer(5, source, dest, blow_out=True)

m300.pick_up_tip()
for num in dest_num:
    m300.transfer(195, buffer_B, plate2.cols(num), new_tip='never')
m300.drop_tip()
