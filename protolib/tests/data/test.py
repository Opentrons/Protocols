from opentrons import containers, instruments

p10rack = containers.load(
    "tiprack-10ul",  # container type
    "C2"             # slot
)
p200rack = containers.load(
    'tiprack-200ul',  # container type
    slot='A1'         # slot
)
trough = containers.load(
    'trough-12row',
    'E1',
    'trough'
)
plate = containers.load(
    '96-PCR-flat',
    'C1',
    'plate'
)
trash = containers.load(
    'point',
    'B2',
    'trash'
)

p200 = instruments.Pipette(
    name="p200",  # optional
    trash_container=trash,
    tip_racks=[p200rack],
    min_volume=20,  # actual minimum volume of the pipette
    axis="a",
    channels=8
)

p200.set_max_volume(200)  # volume calibration, can be called whenever you want

p10 = instruments.Pipette(
    name="p10",  # optional
    trash_container=trash,
    tip_racks=[p10rack],
    min_volume=1,  # actual minimum volume of the pipette
    axis="b",
    channels=1  # 1 o
)
p10.set_max_volume(10)


# assume these
sample_numbers = 3
sample_location = plate.rows[0]  # first row of plate
diluent_location = trough['A1']  # what the samples are diluted with

# inputs from user
dilution_number = 3  # how many dilutions
dilution_factor = 10  # dilution factor 10X
dilution_volume = 200  # in uL

sample_volume = int(round((dilution_volume)/(dilution_factor)))
diluent_volume = int(round(dilution_volume - sample_volume))


# add diluent to plate based on volume
if diluent_volume <= 10:
    p200.pick_up_tip()
    for i in range(1, dilution_number + 1):
        p200.aspirate(diluent_volume, trough['A1']).dispense(plate.rows[i])
    p200.drop_tip()

    for col in range(sample_numbers):
        p10.pick_up_tip()
        for row in range(1, dilution_number):
            p10.aspirate(diluent_volume, plate.rows[row][col]).dispense(plate.rows[row + 1][col])  # noqa: E501
        p10.drop_tip()

else:
    for i in range(1, dilution_number + 1):
        p200.aspirate(diluent_volume, trough['A1']).dispense(plate.rows[i])
    p200.drop_tip()

# dilute samples through wells based on volume
if sample_volume <= 10:
    for col in range(sample_numbers):
        p10.pick_up_tip()
        for row in range(0, dilution_number):
            p10.aspirate(sample_volume, plate.rows[row][col]).dispense(plate.rows[row + 1][col]).mix(sample_volume, 3, plate.rows[row + 1][col])  # noqa: E501
        p10.drop_tip()
else:
    # use p200
    p200.pick_up_tip()
    for i in range(0, dilution_number):
        p200.aspirate(sample_volume, plate.rows[i]).dispense(plate.rows[i + 1]).mix(sample_volume, 3, plate.rows[i + 1])  # noqa: E501
    p200.drop_tip()
