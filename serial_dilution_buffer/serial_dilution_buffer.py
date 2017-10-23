from opentrons import containers, instruments

# source of diluent
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

diluent_source = trough['A1']


def run_custom_protocol(dilution_factor: float=10,
                        final_volume: float=100,
                        number_of_rows_to_use: int=11,
                        number_of_plates: int=1):
    if number_of_rows_to_use > 11:
        raise RuntimeError((
            'Number of dilutions cannot exceed 11 (since there are 12 rows ' +
            'in a 96-well plate). Got {}'
            ).format(number_of_rows_to_use))

    # calculate how much diluent to use
    diluent_vol = final_volume * ((dilution_factor-1)/dilution_factor)

    # calculate how much sample to transfer
    transfer_vol = final_volume - diluent_vol

    for plate in plates[:number_of_plates]:
        # Add diluent to all wells that will be used
        # discard tips
        p50multi.distribute(
            final_volume,
            diluent_source,
            plate.rows(0, length=number_of_rows_to_use))

        # dilute and mix up the plate from row 1 to last row.
        # this is controlled by number_of_rows_to_use
        p50multi.transfer(
            transfer_vol,
            plate.rows(0, length=number_of_rows_to_use),
            plate.rows(1, length=number_of_rows_to_use),
            mix_before=(10, final_volume/2), new_tip='always'
        )

        # remove excess liquid from column 12 and empty into waste
        p50multi.transfer(
            transfer_vol,
            plate.rows(number_of_rows_to_use+1),
            trash,
            mix_before=(10, final_volume/2))
