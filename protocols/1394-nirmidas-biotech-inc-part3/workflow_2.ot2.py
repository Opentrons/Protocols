from opentrons import labware, instruments

frame_slides = ['fast-frame-slide-'+str(i) for i in range(1, 5)]
for slide in frame_slides:
    if slide not in labware.list():
        labware.create(
            slide,
            grid=(2, 8),
            spacing=(9, 9),
            diameter=7,
            depth=10.5)

# labware setup
plate = labware.load('96-flat', '1')
custom_plate = []
for slide in frame_slides:
    custom_plate.append(labware.load(slide, '5', share=True))

tiprack_300 = labware.load('opentrons-tiprack-300ul', '8')

# instruments setup
m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=[tiprack_300])

source_num = ['1', '2', '4', '5', '7', '8', '10', '11']

A_cols = [col for slide in custom_plate for col in slide.cols()]

for num, dest in zip(source_num, A_cols):
    m300.transfer(100, plate.cols(num), dest)
