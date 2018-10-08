from opentrons import labware, instruments

# labware setup
trough = labware.load('trough-12row', '1')
plate = labware.load('96-flat', '2')
templates_1 = labware.load('opentrons-tuberack-2ml-screwcap', '3')
templates_2 = labware.load('opentrons-tuberack-2ml-screwcap', '6')
tiprack_10 = labware.load('tiprack-10ul', '4')
tiprack_50 = labware.load('tiprack-200ul', '5')

# reagent setup
mastermix = trough.wells('A1')

# instrument setup
p50 = instruments.P50_Multi(
    mount='left',
    tip_racks=[tiprack_50])

p10 = instruments.P10_Single(
    mount='right',
    tip_racks=[tiprack_10])

# transfer MasterMix to plate
p50.distribute(18, mastermix, plate.cols())

# define template locations
templates = [well for row in templates_1.rows() for well in row] + \
            [well for row in templates_2.rows() for well in row]
templates = templates[:32]

# define plate locations
plate_locs = [well for row in plate.rows() for well in row]

# transfer template to plate
for index, template in enumerate(templates):
    dest = plate_locs[index*3:index*3+3]
    p10.pick_up_tip()
    p10.distribute(2, template, dest, new_tip='never')
    for well in dest:
        p10.mix(5, 10, well)
    p10.drop_tip()
