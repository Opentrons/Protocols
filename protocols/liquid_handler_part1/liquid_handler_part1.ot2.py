from opentrons import labware, instruments

plates = [
    labware.load('96-flat', '1'),
    labware.load('96-flat', '2'),
    labware.load('96-flat', '3'),
    labware.load('96-flat', '4'),
    labware.load('96-flat', '5'),
    labware.load('96-flat', '6'),
    labware.load('96-flat', '7')
    ]

trough = labware.load('trough-12row', '10')
liquid_trash = trough.wells('A6')

tiprack1 = labware.load('tiprack-200ul', '8')
tiprack2 = labware.load('tiprack-200ul', '9')

tuberack = labware.load('tube-rack-2ml', '11')

p300 = instruments.P300_Single(
    mount='left',
    tip_racks=[tiprack2])

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack1])


# transfer culture media to columns 2-9 of all plates
m300.pick_up_tip()
for plate1, plate2, media in zip(
        plates[0::2], plates[1::2], trough.wells(11, to=8)):
    m300.distribute(100, media, plate1.cols('2', to='9'), new_tip='never')
    m300.distribute(100, media, plate2.cols('2', to='9'), new_tip='never')
m300.distribute(
    100, trough.wells('A9'), plates[6].cols('2', to='9'), new_tip='never')
m300.drop_tip()

# transfer culture media to B11-H11 of all plates
m300.distribute(
    100,
    trough.wells('A8'),
    [plate.cols('11') for plate in plates],
    new_tip='once')

# transfer culture media to A10-C10, G10-H10 of all plates
m300.distribute(
    100,
    trough.wells('A7'),
    [plate.cols('10') for plate in plates],
    new_tip='once')

# transfer sample to D10-F10 of all plates
p300.pick_up_tip()
for plate in plates:
    p300.distribute(
        100,
        trough.wells('A3'),
        plate.cols('10').wells('D', to='F'),
        new_tip='never')
p300.drop_tip()

# transfer stock sample to A11 of all plates
p300.transfer(
    200,
    trough.wells('A4'),
    [plate.wells('A11') for plate in plates],
    new_tip='once')

# serial dilute down column 11 of all plates

p300.pick_up_tip()
for plate in plates:
    p300.transfer(100,
                  plate.wells('A11', to='G11'),
                  plate.wells('B11', to='H11'),
                  mix_after=(3, 100),
                  new_tip='never')
    p300.transfer(100, plate.wells('H11'), liquid_trash, new_tip='never')
p300.drop_tip()

# transfer sterile water to column 12 of all plates
m300.distribute(
    100,
    trough.wells('A5'),
    [plate.cols('12') for plate in plates],
    new_tip='once')

# transfer each of the 14 stock tubes to 4 wells in column 1 of all plates
stock_source = [well for row in tuberack.rows() for well in row][0:14]
stock_dest = []
for plate in plates:
    stock_dest.append(plate.wells('A1', to='D1'))
    stock_dest.append(plate.wells('E1', to='H1'))
for source, dest in zip(stock_source, stock_dest):
    p300.transfer(200, source, dest, new_tip='once')

# serial dilution down the plate for all plates
for plate in plates:
    m300.pick_up_tip()
    m300.transfer(
        100,
        plate.cols('1', to='11'),
        plate.cols('2', to='12'),
        mix_after=(3, 10),
        new_tip='never')
    m300.transfer(100, plate.cols('12'), liquid_trash, new_tip='never')
    m300.drop_tip()
