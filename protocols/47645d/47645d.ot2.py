from opentrons import labware, instruments
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'Protein Crystallization Screen',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

trough1 = labware.load(
    'opentrons_6_tuberack_falcon_50ml_conical', '1', 'Trough 1 (6-Tube)')

trough2 = labware.load(
    'opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', '2', 'Trough 2')

tips1000 = labware.load('opentrons_96_tiprack_1000ul', '4', '1000ul Tiprack')

desttubes = 'analytical_24_vials_4000ul'
if desttubes not in labware.list():
    labware.create(
        desttubes,
        grid=(6, 4),
        spacing=(20, 20),
        diameter=15,
        depth=40,
        volume=4000
    )

vialrack = labware.load(desttubes, '3', 'Al Reactor w/ Vials')


def run_custom_protocol(
        p1000_mount: StringSelection('right', 'left') = 'right'
):

    # create pipettes
    pip1k = instruments.P1000_Single(mount=p1000_mount, tip_racks=[tips1000])

    for source, dest_col in zip(trough1.wells(), vialrack.columns()):
        pip1k.pick_up_tip()
        for i, dest in enumerate(dest_col):
            vol = 500-(125*i)
            pip1k.transfer(vol, source, dest, air_gap=50, new_tip='never')
            pip1k.blow_out(dest.top())
        pip1k.drop_tip()

    pip1k.distribute(500, trough2.wells('A3'), vialrack.wells(), air_gap=50)

    pip1k.distribute(500, trough2.wells('B3'), vialrack.wells(), air_gap=50)
