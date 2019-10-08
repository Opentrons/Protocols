from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Protein Purification with MagDeck',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create and load labware

magdeck = modules.load('magdeck', '10')
deep_name = 'porvair_96_deepwellplate_2000ul'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.25,
        depth=39.9,
        volume=2000
    )
mag_plate = labware.load(deep_name, '10', share=True)
magh = 14.94

res_name = 'nalgene_1_reservoir_300ml'
if res_name not in labware.list():
    labware.create(
        res_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=123.0,
        depth=36.6,
        volume=300000
    )
liqwaste = labware.load(
            res_name, '11', 'Nalgene Reservoir (waste)').wells(0).top()

greiner_name = 'greiner_96_wellplate_340ul_vbottom'
if greiner_name not in labware.list():
    labware.create(
        greiner_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.96,
        depth=10.9,
        volume=340
    )
elution_plate = labware.load(greiner_name, '8', 'Elution Plate')

trough12 = 'porvair_12_reservoir_20ml'
if trough12 not in labware.list():
    labware.create(
        trough12,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=8.25,
        depth=39.2,
        volume=20000
    )
res12 = labware.load(trough12, '9', '12-Column Reservoir')
ebuffer = res12.wells(8)

tips = [labware.load('opentrons_96_tiprack_300ul', str(slot+1),
        'Opentrons 300ul Tips') for slot in range(7)]


def run_custom_protocol(
        pipette_type: StringSelection(
        'p300_Multi', 'p300_Single') = 'p300_Multi',
        pipette_mount: StringSelection('left', 'right') = 'left',
        number_of_samples: int = 96
):

    # create pipette and samples
    if pipette_type == 'p300_Single':
        pip300 = instruments.P300_Single(mount=pipette_mount, tip_racks=tips)
        [samps, elutes] = [
            plate.wells()[:number_of_samples]
            for plate in [mag_plate, elution_plate]
            ]
    else:
        num_cols = math.ceil(number_of_samples/8)
        pip300 = instruments.P300_Multi(mount=pipette_mount, tip_racks=tips)
        [samps, elutes] = [
            plate.rows('A')[:num_cols]
            for plate in [mag_plate, elution_plate]
            ]

    def basic_transfer(vol):
        for s in samps:
            pip300.pick_up_tip()
            pip300.transfer(vol, s, liqwaste, new_tip='never')
            pip300.drop_tip()

    def wash_step(well):
        if number_of_samples > 48:
            wash1 = samps[:len(samps)//2]
            wash2 = samps[len(samps)//2:]
            wash_total = [wash1, wash2]
        else:
            wash_total = [samps]
        for wells in wash_total:
            for s in wells:
                pip300.pick_up_tip()
                pip300.transfer(250, res12.wells(well), s, new_tip='never')
                pip300.mix(5, 200, s)
                pip300.blow_out(s.top())
                pip300.drop_tip()
            well += 1
        magdeck.engage(height=magh)
        pip300.delay(minutes=5)
        robot._driver.run_flag.wait()

        pip300.set_flow_rate(aspirate=50)
        basic_transfer(300)
        magdeck.disengage()
        pip300.set_flow_rate(aspirate=150)

    # Engage magnet for 5 minutes and then remove 300ul of volume
    magdeck.engage(height=magh)
    pip300.delay(minutes=5)
    robot._driver.run_flag.wait()

    basic_transfer(300)
    magdeck.disengage()

    # Wash step 1
    wash_step(0)

    # Wash step 2
    wash_step(2)

    # add elution buffer and move to elution plate
    for s in samps:
        pip300.pick_up_tip()
        pip300.transfer(100, ebuffer, s, new_tip='never')
        pip300.mix(5, 40, s)
        pip300.blow_out(s.top())
        pip300.drop_tip()

    pip300.delay(minutes=3)
    robot._driver.run_flag.wait()
    magdeck.engage(height=magh)
    pip300.delay(minutes=5)

    pip300.set_flow_rate(aspirate=25, dispense=50)
    for s, e in zip(samps, elutes):
        pip300.pick_up_tip()
        pip300.transfer(100, s, e, new_tip='never')
        pip300.blow_out(e.top())
        pip300.drop_tip()

    magdeck.disengage()
