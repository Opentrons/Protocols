from opentrons import labware, instruments

# custom tube rack
if 'tube-rack-5x12' not in labware.list():
    labware.create(
        'tube-rack-5x12',
        grid=(12, 5),
        spacing=(20, 20),
        diameter=16,
        depth=90)

# labware setup
trough1 = labware.load('trough-12row', '7')
sample_rack = labware.load('tube-rack-5x12', '4')
tiprack_50 = labware.load('tiprack-200ul', '8')
tiprack_1000 = labware.load('tiprack-1000ul', '9')

# pipette setup
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=[tiprack_50]
    )

p1000 = instruments.P1000_Single(
    mount='right',
    tip_racks=[tiprack_1000]
    )


def run_custom_protocol(
    number_of_samples: int=10
        ):

    # number of racks for serial dilutions
    rack_num = number_of_samples // 12 + (
        1 if number_of_samples * 12 > 0 else 0)

    # target rack setup
    slots = ['1', '2', '3'][:rack_num]
    target = [labware.load('tube-rack-5x12', slot) for slot in slots]

    target_cols = [
        col for rack in target for col in rack.cols()][:number_of_samples]

    trough_loc = [well for well in trough1.wells()]

    wells = [well for col in target_cols for well in col]

    # each reservoir fills 20 well, hence grouping 20 wells together
    wells_group = [wells[x:x+20] for x in range(0, len(wells), 20)]

    # transfer diluent from reservoirs in trough to all positions for serial
    # dilutions, using the same pipette tip
    p1000.pick_up_tip()
    for index, group in enumerate(wells_group):
        p1000.transfer(1000, trough_loc[index], group, new_tip='never')
    p1000.drop_tip()

    samples = [
        well for row in sample_rack.rows() for well in row][:number_of_samples]

    # transfer sample to well in row 1, perform serial dilution down the rows
    for sample, dest in zip(samples, target_cols):
        p50.pick_up_tip()
        p50.transfer(50, sample, dest[0], new_tip='never', mix_after=(5, 50))
        p50.transfer(50, dest[0:4], dest[1:5], new_tip='never',
                     mix_after=(5, 50))
        p50.drop_tip()
