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

    wellno = 0

    def simple_transfer(src):
        nonlocal wellno

        pip1k.pick_up_tip()
        pip1k.transfer(
            500, src, vialrack.wells(wellno), air_gap=50, new_tip='never')
        pip1k.blow_out(vialrack.wells(wellno).top())
        wellno += 1
        pip1k.transfer(
            375, src, vialrack.wells(wellno), air_gap=50, new_tip='never')
        pip1k.blow_out(vialrack.wells(wellno).top())
        wellno += 1
        pip1k.transfer(
            250, src, vialrack.wells(wellno), air_gap=50, new_tip='never')
        pip1k.blow_out(vialrack.wells(wellno).top())
        wellno += 1
        pip1k.transfer(
            125, src, vialrack.wells(wellno), air_gap=50, new_tip='never')
        pip1k.blow_out(vialrack.wells(wellno).top())
        wellno += 1
        pip1k.drop_tip()

    for s in trough1:
        simple_transfer(s)

    pip1k.pick_up_tip()
    pip1k.distribute(500, trough2.wells('A3'), vialrack, air_gap=50)

    pip1k.pick_up_tip()
    pip1k.distribute(500, trough2.wells('B3'), vialrack, air_gap=50)
