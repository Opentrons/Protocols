from opentrons import labware, instruments

# labware setup
tiprack_300 = labware.load('opentrons-tiprack-300ul', '1')
tiprack_50 = labware.load('opentrons-tiprack-300ul', '2')
deep_plates = [labware.load('96-deep-well', slot)
               for slot in ['3', '4']]
flat_plates = [labware.load('96-flat', slot)
               for slot in ['5', '6', '7', '8']]

# instrument setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50])
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])


m300.transfer(50, deep_plates[0].cols('1'), flat_plates[0].cols('7', '12'),
              mix_before=(5, 50))

m300.transfer(50, deep_plates[0].cols('7'), flat_plates[1].cols('7', '12'),
              mix_before=(5, 50))

m300.transfer(50, deep_plates[1].cols('1'), flat_plates[2].cols('7', '12'),
              mix_before=(5, 50))

m300.transfer(50, deep_plates[1].cols('7'), flat_plates[3].cols('7', '12'),
              mix_before=(5, 50))

transfer_vol = [5, 10, 20, 30, 40]

for plate in deep_plates:
    p50.transfer(
        transfer_vol,
        plate.wells('A6'),
        plate.rows('A').wells('1', to='5'),
        mix_after=(5, 50))

    p50.transfer(
        transfer_vol,
        plate.wells('A6'),
        plate.rows('A').wells('7', to='11'),
        mix_after=(5, 50))

columns = [['1', '2'], ['3', '4'], ['5', '6'], ['8', '9'], ['10', '11']]
for index, plate in enumerate(deep_plates):
    m300.pick_up_tip()
    for source, dest_col in zip(plate.cols('1', to='5'), columns):
        m300.mix(5, 50, source)
        m300.distribute(
            50,
            source,
            flat_plates[index*2].cols(dest_col),
            new_tip='never',
            disposal_vol=0)

    for source, dest_col in zip(plate.cols('7', to='11'), columns):
        m300.mix(5, 50, source)
        m300.distribute(
            50,
            source,
            flat_plates[index*2+1].cols(dest_col),
            new_tip='never',
            disposal_vol=0)
    m300.drop_tip()
