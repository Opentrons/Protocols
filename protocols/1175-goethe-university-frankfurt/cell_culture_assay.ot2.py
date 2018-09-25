from opentrons import labware, instruments

deep_block = labware.load('96-deep-well', '7')
plates = [labware.load('96-flat', slot)
          for slot in ['1', '2', '3', '4', '5', '6']]
cultures = labware.load('96-deep-well', '8').cols('1', length=6)

tiprack1 = labware.load('tiprack-200ul', '9')
tiprack2 = labware.load('tiprack-200ul', '10')

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack1, tiprack2])

media_source = [col for col in deep_block.cols()]

# transfer 75 uL of medium from deep block to each plate
for index, source in enumerate(media_source):
    m300.pick_up_tip()
    for plate in plates:
        if m300.current_volume < 100:
            m300.blow_out(source.top())
            m300.aspirate(300, source)
        m300.dispense(75, plate.cols(index).top())
    m300.blow_out(source.top())
    m300.drop_tip()

# transfer 75 uL of cell culture from each 15 mL tube to each plate
for culture, plate in zip(cultures, plates):
    m300.pick_up_tip()
    for col in plate.cols():
        if m300.current_volume < 100:
            m300.blow_out(culture.top())
            m300.aspirate(300, culture)
        m300.dispense(75, col.top())
    m300.blow_out(culture.top())
    m300.drop_tip()
