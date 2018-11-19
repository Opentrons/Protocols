from opentrons import labware, instruments, modules

# labware setup
trough = labware.load('trough-12row', '1')
plates = [labware.load('96-well-plate-20mm', slot, 'Plate '+alpha)
          for slot, alpha in zip(['2', '3', '5', '6'], ['A', 'B', 'C', 'D'])]
temp_deck = modules.load('tempdeck', '4')
temp_plate = labware.load('opentrons-aluminum-block-PCR-strips-200ul', '4',
                          share=True)

tipracks = [labware.load('tiprack-10ul', slot)
            for slot in ['7', '8', '9', '10', '11']]

# instruments setup
m10 = instruments.P10_Multi(
    mount='left',
    tip_racks=tipracks)

temp_deck.set_temperature(4)
temp_deck.wait_for_temp()

# transfer multiplex mix from reservoir to each plate
for index, plate in enumerate(plates):
    m10.distribute(4, trough.wells(index), plate.cols())

# transfer DNA to each plate
for plate in plates:
    for DNA, dest in zip(temp_plate.cols(), plate.cols()):
        m10.transfer(1, DNA, dest, blow_out=True)
