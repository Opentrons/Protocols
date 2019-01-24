from opentrons import containers, instruments

metadata = {
    'protocolName': 'PCR Prep',
    'author': 'Alise <protocols@opentrons.com>',
    'source': 'Custom Protocol Library'
    }

# labware setup
tiprack_200 = containers.load('tiprack-200ul', 'A2')
tiprack_10 = containers.load('tiprack-10ul', 'E2')
plate = containers.load('96-flat', 'D2')
block = containers.load('96-deep-well', 'C1')
pcr_strips = containers.load('PCR-strip-tall', 'D3')
trash = containers.load('trash-box', 'B3')

# instrument setup
m10 = instruments.Pipette(
    axis='a',
    channels=8,
    max_volume=10,
    min_volume=1,
    trash_container=trash,
    tip_racks=[tiprack_10])

p50 = instruments.Pipette(
    axis='b',
    channels=1,
    max_volume=50,
    min_volume=5,
    trash_container=trash,
    tip_racks=[tiprack_200])


def run_custom_protocol(
        mastermix_volume: float=6.5,
        DNA_volume: float=5.5):

    # sample setup
    samples = pcr_strips.rows('1')

    # distribute master mix
    for row_index, well in enumerate(block.cols('A')):
        dests = [well.bottom() for well in plate.rows(row_index)]
        p50.distribute(mastermix_volume, well, dests, disposal_vol=0)

    # transfer samples
    for row in plate.rows():
        m10.transfer(DNA_volume, samples, row[0].bottom(), blow_out=True)
