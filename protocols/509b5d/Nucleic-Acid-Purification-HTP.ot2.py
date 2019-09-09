from opentrons import labware, instruments, robot, modules
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Kylt RNA/DNA Purification HTP',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# create and load labware
magdeck = modules.load('magdeck', '4')
mag_offset = 14.94  # based on definitions found in labware

deep_name = 'ritter_96_deepwellplate_2500ul'
if deep_name not in labware.list():
    labware.create(
        deep_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=8.2,
        depth=42.2,
        volume=2500
    )
# ^^^based on this definition:
# bwww.hj-bioanalytik.de/images/HJMedia/Pictures/Products/Plates/RiplateSW.pdf

deep_plate = labware.load(deep_name, '4', 'Deep Well Plate', share=True)
elution_plate = labware.load('corning_96_wellplate_360ul_flat', '1',
                             'Elution Plate')
liq_waste = labware.load('agilent_1_reservoir_290ml', '3', 'Liquid Waste')

four_res = 'agilent_4_reservoir_73ml'
if four_res not in labware.list():
    labware.create(
        four_res,
        grid=(4, 1),
        spacing=(27, 0),
        diameter=26.1,
        depth=42.1,
        volume=7300
    )
# ^^^based on this definition:
# https://www.empbiotech.com/uploads/tx_productserw/SH-201308-100_tech.jpg

large_res = labware.load(four_res, '6', 'Reservoir 4 Column')

twelve_res = 'agilent_12_reservoir_21ml'
if twelve_res not in labware.list():
    labware.create(
        twelve_res,
        grid=(12, 1),
        spacing=(9, 0),
        diameter=7,
        depth=39.22,
        volume=2100
    )
# ^^^based on this definition:
# https://www.empbiotech.com/uploads/tx_productserw/SH-201256-100_tech.jpg

small_res = labware.load(twelve_res, '5', 'Reservoir 12 Column')

# reagents
pk = small_res.wells(0)
lysis = small_res.wells(2)
magbeads = small_res.wells(4)
elution = small_res.wells(6)

binding = large_res.wells(0)
wash = large_res.wells(1)
wash2 = large_res.wells(2)
etoh = large_res.wells(3)

waste = liq_waste.wells(0)

# tipracks

tips_1x = labware.load('opentrons_96_tiprack_300ul', '7', 'Single Use Tips')
tips_reuse_a = labware.load('opentrons_96_tiprack_300ul', '8', 'Tiprack')
tips_reuse_b = labware.load('opentrons_96_tiprack_300ul', '9', 'Tiprack')


def run_custom_protocol(
        p50_type: StringSelection('multi', 'single') = 'multi',
        p300_type: StringSelection('multi', 'single') = 'multi',
        p50_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('right', 'left') = 'right',
        second_wash: StringSelection('no', 'yes') = 'no',
        number_of_samples_to_process: int = 96
        ):

    # check:
    if p50_mount == p300_mount:
        raise Exception('Input different mounts for P50 and P300 pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
        1 and 96).')

    # create pipettes
    num_cols = math.ceil(number_of_samples_to_process/8)

    if p50_type == 'multi':
        # holder
        pip50 = instruments.P50_Multi(mount=p50_mount)
        [samples50] = [
            plate.rows('A')[:num_cols] for plate in [
                deep_plate
            ]
        ]
        pass
    else:
        # holder
        pip50 = instruments.P50_Single(mount=p50_mount)
        [samples50] = [
            plate.wells()[:number_of_samples_to_process] for plate in [
                deep_plate
            ]
        ]
        pass

    if p300_type == 'multi':
        # holder
        pip300 = instruments.P300_Multi(mount=p300_mount)
        [samples300, eluates] = [
            plate.rows('A')[:num_cols] for plate in [
                deep_plate, elution_plate
            ]
        ]
        pass
    else:
        # holder
        pip300 = instruments.P300_Single(mount=p300_mount)
        [samples300, eluates] = [
            plate.wells()[:number_of_samples_to_process] for plate in [
                deep_plate, elution_plate
            ]
        ]
        pass

    if magdeck._engaged:
        magdeck.disengage()

    pip50.pick_up_tip(tips_1x.wells('A1'))

    # transfer 20ul of proteinase k to each well
    pip50vol = 0
    for well in samples50:
        if pip50vol == 0:
            pip50.aspirate(40, pk)
            pip50vol += 40
        pip50.dispense(20, well.top())
        pip50vol -= 20

    if pip50vol > 0:
        pip50.dispense(pip50vol, pk)
    pip50.drop_tip()

    # add 130ul of lysis solution to each well; mix; and reuse tips

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_a.wells(well_name))
        pip300.aspirate(130, lysis)
        pip300.dispense(130, well)
        pip300.mix(3, 200, well)
        pip300.blow_out(well.top())
        pip300.return_tip()

    # 10 minute incubation period

    robot.comment('Incubating for 10 minutes. OT-2 will resume when incubation \
    is complete.')
    pip50.delay(minutes=10)
    robot._driver.run_flag.wait()

    # mix magbeads and dispense to each well

    pip50.pick_up_tip(tips_1x.wells('A2'))

    pip50.mix(5, 40, magbeads)

    pip50.blow_out(magbeads.top())

    pip50vol = 0

    for well in samples50:
        if pip50vol == 0:
            pip50.aspirate(40, magbeads)
            pip50vol += 40
        pip50.dispense(20, well.top())
        pip50vol -= 20

    if pip50vol > 0:
        pip50.dispense(pip50vol, pk)
    pip50.drop_tip()

    # add 500ul of binding solution to each well

    pip300.pick_up_tip(tips_1x.wells('A3'))

    for well in samples300:
        pip300.transfer(250, binding, well.top(), new_tip='never')
        pip300.blow_out(well.top())
        pip300.transfer(250, binding, well.top(), new_tip='never')
        pip300.blow_out(well.top())

    pip300.drop_tip()

    # re-use tips to mix and then replace tips in rack

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_a.wells(well_name))
        pip300.mix(5, 280, well)
        pip300.blow_out(well.top())
        pip300.return_tip()

    # incubate for 5 minutes
    robot.comment('Incubating for 5 minutes. OT-2 will resume when incubation \
    is complete.')
    pip300.delay(minutes=5)
    robot._driver.run_flag.wait()

    # separate beads using magdeck

    magdeck.engage(height=mag_offset)
    pip300.delay(minutes=1)

    # remove 870ul of supernatant from each well using replaced tips

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_a.wells(well_name))
        for t in range(3):
            pip300.transfer(290, well, waste, new_tip='never')
            pip300.blow_out(waste.top())
        pip300.return_tip()

    magdeck.disengage()

    # add 500ul of wash solution to each well with new tips

    pip300.pick_up_tip(tips_1x.wells('A4'))

    for well in samples300:
        for t in range(2):
            pip300.transfer(250, wash, well.top(), new_tip='never')
            pip300.blow_out(well.top())

    pip300.drop_tip()

    # use tips from before to mix each well and then return tips

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_a.wells(well_name))
        pip300.mix(5, 290, well)
        pip300.blow_out(well.top())
        pip300.return_tip()

    # separate beads using magdeck

    magdeck.engage(height=mag_offset)
    pip300.delay(minutes=1)

    # remove 500ul of supernatant with tips from before

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_a.wells(well_name))
        for t in range(2):
            pip300.transfer(250, well, waste, new_tip='never')
            pip300.blow_out(waste.top())
        pip300.return_tip()

    magdeck.disengage()

    if second_wash == 'yes':
        # add 500ul of wash solution to each well with new tips

        pip300.pick_up_tip(tips_1x.wells('A6'))

        for well in samples300:
            for t in range(2):
                pip300.transfer(250, wash2, well.top(), new_tip='never')
                pip300.blow_out(well.top())

        pip300.drop_tip()

        # use tips from before to mix each well and then return tips

        for well in samples300:
            well_name = well.get_name()
            pip300.pick_up_tip(tips_reuse_a.wells(well_name))
            pip300.mix(5, 290, well)
            pip300.blow_out(well.top())
            pip300.return_tip()

        # separate beads using magdeck

        magdeck.engage(height=mag_offset)
        pip300.delay(minutes=1)

        # remove 500ul of supernatant with tips from before

        for well in samples300:
            well_name = well.get_name()
            pip300.pick_up_tip(tips_reuse_a.wells(well_name))
            for t in range(2):
                pip300.transfer(250, well, waste, new_tip='never')
                pip300.blow_out(waste.top())
            pip300.return_tip()

        magdeck.disengage()

    # add 500ul 80% EtOH to each well

    pip300.pick_up_tip(tips_1x.wells('A5'))

    for well in samples300:
        for t in range(2):
            pip300.transfer(250, etoh, well.top(), new_tip='never')
            pip300.blow_out(well.top())

    pip300.drop_tip()

    # use tips from before to mix beads.

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_a.wells(well_name))
        pip300.mix(5, 290, well)
        pip300.blow_out(well.top())
        pip300.return_tip()

    # separate beads

    magdeck.engage(height=mag_offset)
    pip300.delay(minutes=1)

    # remove 500ul of supernatant with tips from before

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_a.wells(well_name))
        for t in range(2):
            pip300.transfer(250, well, waste, new_tip='never')
            pip300.blow_out(waste.top())
        pip300.drop_tip()

    magdeck.disengage()

    # incubate dry beads for 10 minutes

    pip300.delay(minutes=10)
    robot._driver.run_flag.wait()

    # add elution buffer to each well; mix; return tip

    for well in samples300:
        well_name = well.get_name()
        pip300.pick_up_tip(tips_reuse_b.wells(well_name))
        pip300.transfer(100, elution, well, new_tip='never')
        pip300.mix(3, 50, well)
        pip300.blow_out(well.top())
        pip300.return_tip()

    # separate beads for ~30 seconds

    magdeck.engage(height=mag_offset)
    pip300.delay(seconds=30)

    # transfer 100ul from sample plate to elution plate

    for source, dest in zip(samples300, eluates):
        well_name = source.get_name()
        pip300.pick_up_tip(tips_reuse_b.wells(well_name))
        pip300.transfer(100, source, dest, new_tip='never')
        pip300.blow_out(dest.top())
        pip300.drop_tip()

    robot.comment("Congratulations. The protocol is now complete.")
