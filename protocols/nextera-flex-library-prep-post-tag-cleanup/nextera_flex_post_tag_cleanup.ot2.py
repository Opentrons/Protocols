from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nextera DNA Flex NGS Library Prep: Post Tagmentation \
Cleanup',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'tagmentation rxn plate', share=True)
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '3', 'reagent reservoir')
tips50 = labware.load('opentrons_96_tiprack_300ul', '4')

twb = [chan for chan in res12.wells()[:2]]
liquid_waste = res12.wells(11).top()


def run_custom_protocol(
        p50_type: StringSelection('single', 'multi') = 'single',
        p300_type: StringSelection('single', 'multi') = 'single',
        p50_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples_to_process: int = 24
):
    # check:
    if p50_mount == p300_mount:
        raise Exception('Input different mounts for P50 and P300 multi-channel \
pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
1 and 96).')

    num_cols = math.ceil(number_of_samples_to_process/8)
    num_300_racks = math.ceil((num_cols*6)/12)
    slots300 = [str(slot) for slot in range(5, 5+num_300_racks)]
    tips300 = [
        labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots300]

    # pipettes
    if p50_type == 'multi':
        pip50 = instruments.P50_Multi(mount=p50_mount, tip_racks=[tips50])
        samples50 = mag_plate.rows('A')[:num_cols]
        tsb = labware.load(
            'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
            '2',
            'strips for TSB').wells('A1')
    else:
        pip50 = instruments.P50_Single(mount=p50_mount, tip_racks=[tips50])
        samples50 = mag_plate.wells()[:number_of_samples_to_process]
        tsb = labware.load(
            'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '2',
            'tuberack for TSB').wells('A1')
    if p300_type == 'multi':
        pip300 = instruments.P300_Multi(mount=p300_mount, tip_racks=tips300)
        samples300 = mag_plate.rows('A')[:num_cols]
    else:
        pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)
        samples300 = mag_plate.wells()[:number_of_samples_to_process]

    # add TSB and slowly mix
    for s in samples50:
        pip50.pick_up_tip()
        pip50.transfer(10, tsb, s, new_tip='never')
        pip50.set_flow_rate(aspirate=10, dispense=20)
        pip50.mix(10, 30, s)
        pip50.blow_out(s.top(-2))
        pip50.drop_tip()

    robot.pause('Seal the plate with Microseal B, place on the preprogrammed \
thermal cycler, and run the PTC program.')

    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    pip50.delay(minutes=3)

    # remove and discard supernatant
    for s in samples300:
        pip300.pick_up_tip()
        pip300.transfer(65, s, liquid_waste, new_tip='never')
        pip300.blow_out()
        pip300.drop_tip()

    # TWB washes 2x
    count = 0
    total_twb = 96*3
    for wash in range(3):
        magdeck.disengage()

        # resuspend beads in TWB
        for s in samples300:
            ind = (count*len(twb))//total_twb
            count += 1

            pip300.set_flow_rate(aspirate=25, dispense=30)
            disp_loc = (s, s.from_center(r=0.9, h=-0.8, theta=0))
            pip300.pick_up_tip()
            pip300.transfer(100, twb[ind], disp_loc, new_tip='never')
            pip300.mix(10, 80, s)
            pip300.drop_tip()

        magdeck.engage(height=18)

        if wash < 2:
            pip300.delay(minutes=3)
            # remove and discard supernatant
            for s in samples300:
                pip300.pick_up_tip()
                pip300.transfer(110, s, liquid_waste, new_tip='never')
                pip300.blow_out()
                pip300.drop_tip()

    robot.comment('Seal the plate, and keep on the magnetic module. The TWB \
remains in the wells to prevent overdrying of the beads')
