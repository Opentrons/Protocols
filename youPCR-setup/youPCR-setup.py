from opentrons import containers, instruments


# plates being processed
deep_plate = containers.load('96-deep-well', 'C1')
flat_plate = containers.load('96-PCR-flat', 'D3')

# 2 ml tube rack
reagents = containers.load('tube-rack-2ml', 'A1')

# tip rack for p200 pipette
tip200_rack = containers.load('tiprack-200ul', 'A2')

# tip rack for p10 pipette
tip10_rack = containers.load('tiprack-10ul', 'C2')

# trash to dispose of tips
trash = containers.load('point', 'B3', 'trash')

# p200 (20 - 200 uL) (single)
p200single = instruments.Pipette(
    axis='b',
    max_volume=200,
    min_volume=20,
    channels=1,
    trash_container=trash,
    tip_racks=[tip200_rack])

# p10 (1 - 10 uL) (multi)
p10multi = instruments.Pipette(
    axis='a',
    max_volume=10,
    min_volume=1,
    channels=8,
    trash_container=trash,
    tip_racks=[tip10_rack])

# # number to process
# ("columns" in spec, our language refers to them as "rows")
# rows = 8  # can change number here
#
# number of mixes for accurate distribute
distribute_number = 9  # 8 wells across + 1 extra well's worth of volume

# LAMP volume
lampvol = 10 * distribute_number

# primer volume
primervol = 2 * distribute_number

# water volume
watervol = 6 * distribute_number

# mix volume
mixvol = (lampvol + primervol + watervol) / distribute_number

# sample volume
samplevol = 2


def run_custom_protocol(number_of_rows_to_process: int=8):
    num_rows = number_of_rows_to_process
    if num_rows > 8:
        raise RuntimeError(
            'Max number of rows to process is 8. Got {}'
            .format(num_rows))

    # rows of plates
    flatrows = flat_plate.rows(0, length=num_rows)
    deeprows = deep_plate.rows(0, length=num_rows)

    # wells holding mastermix
    mastermixes = [row[0] for row in flatrows] if num_rows > 1 else flatrows[0]

    # reagent locations
    lamp_source = reagents['A1']
    primer = reagents['A2']
    water = reagents['A3']

    # --- Execute protocol ---

    # make master mixes
    p200single.distribute(lampvol, lamp_source, mastermixes, new_tip='once')
    p200single.transfer(primervol, primer, mastermixes, new_tip='always')
    p200single.transfer(
        watervol, water, mastermixes, mix_after=(5, 50), new_tip='always')

    # distribute master mix
    p200single.distribute(
        mixvol, mastermixes, flatrows, disposal_vol=mixvol, new_tip='once')

    # transfer samples from deep plate to flat plate with master mix
    p10multi.transfer(samplevol, deeprows, flatrows, new_tip='always')
