from opentrons import containers, instruments

metadata = {
    'protocolName': 'Plasmid Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# labware
plate = containers.load('96-PCR-flat', 'A1')
trough = containers.load('trough-12row', 'B1')
tubes = containers.load('tube-rack-2ml', 'C1')
tips10 = containers.load('tiprack-10ul', 'A2')
tips1000 = containers.load('tiprack-1000ul', 'B2')
trash = containers.load('trash-box', 'C2')

# pipettes
p10 = instruments.Pipette(
    axis='a',
    name='m10',
    max_volume=10,
    min_volume=1,
    channels=1,
    tip_racks=[tips10],
    trash_container=trash)
m300 = instruments.Pipette(
    axis='b',
    name='m300',
    max_volume=300,
    min_volume=50,
    channels=8,
    tip_racks=[tips1000],
    trash_container=trash)

# set up reagents
medium = trough.wells('A1')
sample = tubes.wells('A1')
plate_row_A = [well for well in plate.cols('A')]
all_wells = [well for well in plate.wells()]


def run_custom_protocol(
    medium_vol: float = 150.0,
    sample_vol: float = 5.0,
    num_mixes: int = 1,
    delay_time_mins: int = 3,
    delay_time_seconds: int = 0
):
    # transfer medium to all wells
    m300.transfer(medium_vol, medium, plate_row_A)

    # transfer sample to all all_wells
    p10.transfer(sample_vol, sample, all_wells, blow_out=True)

    # mix and delay
    m300.pick_up_tip()
    for _ in range(num_mixes):
        for well in plate_row_A:
            m300.mix(3, medium_vol, well)
        m300.delay(minutes=delay_time_mins, seconds=delay_time_seconds)
    m300.drop_tip()
