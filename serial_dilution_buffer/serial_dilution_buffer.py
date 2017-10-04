from opentrons import containers, instruments

# dilution factor
dilution = 10  # can change here

# end volume of solution
vol = 100  # can change here

# how many serial dilutions to do
num_dilutions = 11  # can change here
# (up to 11, since there are 12 rows in plate)

# source of buffer
trough = containers.load('trough-12row', 'D2')

# HACK: need to explicitly load each container like this
# instead of using a for loop, so that deck map can be parsed out
# for protocol library

# plate dilution will happen in
# plate_slots = ['A1', 'B1', 'A2', 'B2', 'A3', 'B3']

# plates = [c o n t a i n e r s.load(
#     '96-PCR-flat', slot) for slot in plate_slots]

plates = [
    containers.load('96-PCR-flat', 'A1'),
    containers.load('96-PCR-flat', 'B1'),
    containers.load('96-PCR-flat', 'A2'),
    containers.load('96-PCR-flat', 'B2'),
    containers.load('96-PCR-flat', 'A3'),
    containers.load('96-PCR-flat', 'B3')
]

# tip rack for p200 pipette
# tiprack_slots = ['C1', 'C3', 'D1', 'D3', 'E1', 'E2', 'E3']

# tipracks = [c o n t a i n e r s.load(
#     'tiprack-200ul', slot) for slot in tiprack_slots]
tipracks = [
    containers.load('tiprack-200ul', 'C1'),
    containers.load('tiprack-200ul', 'C3'),
    containers.load('tiprack-200ul', 'D1'),
    containers.load('tiprack-200ul', 'D3'),
    containers.load('tiprack-200ul', 'E1'),
    containers.load('tiprack-200ul', 'E2'),
    containers.load('tiprack-200ul', 'E3')
]

# trash location
trash = containers.load('trash-box', 'C2')

p50multi = instruments.Pipette(
    trash_container=trash,
    tip_racks=tipracks,
    min_volume=5,
    max_volume=50,
    axis="a",
    channels=8
)

# calculate how much buffer to use
buffer_vol = vol * ((dilution-1)/dilution)

# calculate how much sample to transfer
sample_vol = vol - buffer_vol

for plate in plates:
    # Transfer 100 uL of media from trough to Column 1 wells (A1-H1),
    # discard tips
    p50multi.distribute(100, trough['A1'], plate.rows(0))
    # Transfer 90 uL of media from trough to Columns 2-12 (A2-H12) (same tips)
    p50multi.distribute(
        buffer_vol, trough['A1'], plate.rows(1, length=num_dilutions))

    # Mix Column 1 by pipetting up and down 10x, discard tips
    # Transfer 10 uL from Column 1 to Column 2 and mix 10x, discard tips
    # Transfer 10 uL from Column 2 to Column 3 and mix 10x, discard tips
    # Repeat this going down the plate until Column 11
    # Transfer 10 uL from Column 11 to Column 12 and mix several times,
    # dispense liquid in well

    p50multi.transfer(
        sample_vol,
        plate.rows(0, length=num_dilutions),
        plate.rows(1, length=num_dilutions),
        mix_before=(10, vol/2), new_tip='always'
    )

    # remove 10 uL of liquid from column 12 and empty into waste, discard tips
    p50multi.transfer(
        sample_vol, plate.rows(11), trash, mix_before=(10, vol/2))
