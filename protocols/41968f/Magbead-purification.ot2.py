from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Magbead Based Peptide Purification',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create and load labware
magdeck = modules.load('magdeck', '4')
mag_height = 14.94  # based on definitions found in labware

deep_name = 'whatman_96_deepwellplate_2000ul'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=41.4,
        volume=2000
    )
# based on user provided, technical specifications

deep_plate = labware.load(deep_name, '4', 'Deep Well Plate', share=True)

greiner_name = 'greiner_96_wellplate_340ul_flat'
if greiner_name not in labware.list():
    labware.create(
        greiner_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.96,
        depth=10.9,
        volume=340
    )

sample_plate = labware.load(greiner_name, '5', 'Sample Plate')
dest_plate = labware.load(greiner_name, '1', 'Final Plate')

four_trough = 'brand_4_reservoir_60ul'
if four_trough not in labware.list():
    labware.create(
        four_trough,
        grid=(4, 1),
        spacing=(27, 0),
        diameter=26.1,
        depth=42.1,
        volume=6000
    )

reagents = labware.load(four_trough, '6', 'Wash and Elution')
liq_waste = labware.load(four_trough, '3', 'Liquid Waste')

# tipracks

tips_1x = labware.load('opentrons_96_tiprack_300ul', '7', 'Single Use Tips')
tips_reuse_a = labware.load('opentrons_96_tiprack_300ul', '8', 'Tiprack')
tips_reuse_b = labware.load('opentrons_96_tiprack_300ul', '9', 'Tiprack')
tips_reuse_c = labware.load('opentrons_96_tiprack_300ul', '10', 'Tiprack')

tips_reuse = [
    tips_reuse_a.rows('A'), tips_reuse_b.rows('A'), tips_reuse_c.rows('A')]


def run_custom_protocol(
        p300_mount: StringSelection('right', 'left') = 'right',
        aspirate_rate: int = 20,
        mag_time: int = 10
        ):
    # checks
    if 150 < aspirate_rate or aspirate_rate < 5:
        raise Exception('The aspirate_rate should be between 5 and 150 ul/s')

    # create pipette

    pip300 = instruments.P300_Multi(mount=p300_mount)
    [deep300, samples300, final300] = [
        plate.rows('A') for plate in [
            deep_plate, sample_plate, dest_plate
        ]
    ]

    if magdeck._engaged:
        magdeck.disengage()

    # add 300ul of sample to deep plate and replace tips in tiprack
    for source, dest, tips in zip(samples300, deep300, tips_reuse[0]):
        pip300.pick_up_tip(tips)
        pip300.aspirate(300, source)
        pip300.dispense(300, dest)
        pip300.blow_out(dest.top())
        pip300.return_tip()

    # pause robot for 30-60 minutes so user can add plate to shaker
    robot.pause('Remove plate from magdeck and place on shaking device for 60 \
    minutes. When done, return the plate to the magdeck and hit "resume" \
    in the OT app')

    # collect supernatant and discard tips
    magdeck.engage(height=mag_height)
    pip300.delay(seconds=mag_time)
    pip300.set_flow_rate(aspirate=aspirate_rate, dispense=300)

    for source, tips in zip(deep300, tips_reuse[0]):
        pip300.pick_up_tip(tips)
        pip300.aspirate(165, source)
        pip300.dispense(165, liq_waste(0))
        pip300.blow_out(liq_waste(0).top())
        pip300.aspirate(165, source)
        pip300.dispense(165, liq_waste(0))
        pip300.blow_out(liq_waste(0).top())
        pip300.drop_tip()

    magdeck.disengage()

    # wash steps (3x)
    mix_r = 0
    for x in range(3):
        pip300.set_flow_rate(aspirate=150, dispense=300)
        pip300.pick_up_tip(tips_1x.wells('A1'))
        for dest in deep300:
            pip300.transfer(300, reagents(x), dest.top(), new_tip='never')
            pip300.blow_out(dest.top())
        pip300.return_tip()
        for source, tips in zip(deep300, tips_reuse[1]):
            pip300.pick_up_tip(tips)
            src_mxr = (source, source.from_center(
                h=-0.7, r=0.8, theta=math.pi*mix_r))
            mix_r = (mix_r + 1) % 2
            pip300.mix(5, 290, src_mxr)
            pip300.blow_out(source.top())
            magdeck.engage(height=mag_height)
            pip300.delay(seconds=mag_time)
            pip300.set_flow_rate(aspirate=aspirate_rate, dispense=300)
            pip300.aspirate(300, source)
            pip300.dispense(300, liq_waste(x+1))
            magdeck.disengage()
            if x == 2:
                pip300.drop_tip()
            else:
                pip300.return_tip()

    # elution step
    for x in range(3):
        pip300.set_flow_rate(aspirate=150, dispense=300)
        pip300.pick_up_tip(tips_1x.wells('A2'))
        for dest in deep300:
            pip300.transfer(30, reagents(3), dest.top(), new_tip='never')
            pip300.blow_out(dest.top())
        pip300.return_tip()
        for y in range(2):
            for source, tips in zip(deep300, tips_reuse[2]):
                pip300.pick_up_tip(tips)
                src_mxr = (source, source.from_center(
                    h=-0.7, r=0.8, theta=math.pi*mix_r))
                mix_r = (mix_r + 1) % 2
                pip300.mix(5, 30, src_mxr)
                pip300.blow_out(source.top())
                pip300.return_tip()
            pip300.delay(minutes=2.5)
            robot._driver.run_flag.wait()
        magdeck.engage(height=mag_height)
        pip300.delay(seconds=mag_time)
        pip300.set_flow_rate(aspirate=aspirate_rate, dispense=300)
        for source, dest, tips in zip(deep300, final300, tips_reuse[2]):
            pip300.pick_up_tip(tips)
            pip300.transfer(30, source, dest, new_tip='never')
            pip300.blow_out(dest.top())
            if x == 2:
                pip300.drop_tip()
            else:
                pip300.return_tip()
        magdeck.disengage()

    robot.comment("Congratulations. The protocol is now complete. Please \
    remove samples from the deck and store properly.")


run_custom_protocol()
for c in robot.commands():
    print(c)
