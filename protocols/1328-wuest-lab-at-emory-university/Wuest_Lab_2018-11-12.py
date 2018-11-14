from opentrons import instruments, labware

# labware setup
tiprack = labware.load('tiprack-200ul', '1')
trough = labware.load('trough-12row', '2')
output = labware.load('96-PCR-flat', '3')
tiprack2 = labware.load('tiprack-200ul', '4')

# instrument setup
pip = instruments.P300_Multi(
    mount='left',
    tip_racks=[tiprack, tiprack2])


def run_custom_protocol(
        water_location: str='A1',
        cells_location: str='A4',
        dilution_factor: float=10):

    # variables and reagents
    water = trough.well(water_location)
    cells = trough.well(cells_location)

    pip.pick_up_tip()
    for col in range(11, -1, -1):
        pip.transfer(100, water, output.cols(col), new_tip='never')
    pip.drop_tip()

    sample_vol = 100/(dilution_factor-1)
    total_volume = sample_vol + 100

    pip.pick_up_tip()
    for col in range(0, 11):
        pip.transfer(sample_vol, output.cols(col), output.cols(col+1),
                     new_tip='never')
        pip.mix(3, total_volume/2)
    pip.transfer(sample_vol, output.cols(11), pip.trash_container.top(),
                 new_tip='never')
    pip.drop_tip()

    pip.transfer(100, cells, output.cols(), new_tip='always')
