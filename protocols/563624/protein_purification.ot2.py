from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Phytip Protein Purification',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create custom labware
tip_name = 'phynexus_96_tiprack_300ul_resin'
if tip_name not in labware.list():
    labware.create(
        tip_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.23,
        depth=59.3
    )

deep_name = 'vwr_96_wellplate_500ul_deep'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.52,
        depth=26.5,
        volume=500
    )

plate_name = 'eppendorf_96_wellplate_150_pcr'
if plate_name not in labware.list():
    labware.create(
        plate_name,
        grid=(12, 8),
        spacing=(9, 9),
        depth=14.6,
        diameter=6.46,
        volume=150
    )

# load labware
tiprack = labware.load(tip_name, '1', '300ul resin tiprack')
plate_labels = [
    'equilibration buffer', 'sample', 'wash buffer 1', 'wash buffer 2'
]
mix_plates = [
    labware.load(deep_name, str(slot), name + ' plate')
    for slot, name in zip(range(2, 6), plate_labels)] + [
        labware.load(plate_name, '6', 'elution buffer plate')
]


def run_custom_protocol(
        p300_multi_mount: StringSelection('right', 'left') = 'right',
        start_column: int = 1,
        end_column: int = 12
):
    # check
    if start_column < 1 or end_column > 12:
        raise Exception('Invalid columns must be between 1 and 12.')
    if start_column > end_column:
        raise Exception('Start column must be before end column')

    m300 = instruments.P300_Multi(mount=p300_multi_mount)
    m300.set_flow_rate(aspirate=5, dispense=5)

    # mix sequences
    def plate_mix(cycles, volume, plate, col, delay=20, blow_out=0):
        mix_loc = plate.rows('A')[col]
        for _ in range(cycles):
            m300.aspirate(volume, mix_loc)
            m300.delay(seconds=delay)
            m300.dispense(volume, mix_loc)
            if blow_out > 0:
                m300.dispense(blow_out, mix_loc.top(-2))

    for col in range(start_column-1, end_column):
        # create air gap
        m300.tip_attached = True
        m300.aspirate(30, tiprack.rows('A')[col].top(5))
        m300.tip_attached = False

        # perform
        m300.pick_up_tip(tiprack.rows('A')[col])
        plate_mix(2, 90, mix_plates[0], col)
        plate_mix(4, 180, mix_plates[1], col, blow_out=10)
        plate_mix(2, 180, mix_plates[2], col)
        plate_mix(2, 180, mix_plates[3], col, blow_out=10)
        plate_mix(4, 70, mix_plates[4], col, blow_out=10)
        m300.return_tip()
