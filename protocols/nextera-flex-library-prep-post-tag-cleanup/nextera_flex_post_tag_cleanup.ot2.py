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

twb = [chan for chan in res12.wells()[:2]]
liquid_waste = res12.wells(11).top()


def run_custom_protocol(
        p300_type: StringSelection('single', 'multi') = 'single',
        p300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples_to_process: int = 24
):
    # check:
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
1 and 96).')

    num_cols = math.ceil(number_of_samples_to_process/8)
    num_300_racks = math.ceil((num_cols*6)/12)
    slots300 = [str(slot) for slot in range(5, 5+num_300_racks)]
    tips300 = [
        labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots300]

    # pipettes
    if p300_type == 'multi':
        pip300 = instruments.P300_Multi(mount=p300_mount, tip_racks=tips300)
        samples300 = mag_plate.rows('A')[:num_cols]
    else:
        pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)
        samples300 = mag_plate.wells()[:number_of_samples_to_process]
    pip300.set_flow_rate(aspirate=75, dispense=90)

    magdeck.engage(height=18)
    robot.comment('Incubating beads on magnet for 3 minutes.')
    pip300.delay(minutes=3)

    # remove and discard supernatant
    for s in samples300:
        pip300.pick_up_tip()
        pip300.transfer(65, s.bottom(), liquid_waste, new_tip='never')
        pip300.blow_out()
        pip300.drop_tip()

    # TWB washes 2x
    count = 0
    total_twb = 96*3
    for wash in range(3):
        magdeck.disengage()

        # resuspend beads in TWB
        for i, s in enumerate(samples300):
            ind = (count*len(twb))//total_twb
            count += 1

            side = i % 2 if p300_type == 'multi' else math.floor(i/8) % 2
            angle = 0 if side == 0 else math.pi
            disp_loc = (s, s.from_center(r=0.95, h=-0.6, theta=angle))
            pip300.pick_up_tip()
            pip300.transfer(100, twb[ind], disp_loc, new_tip='never')
            pip300.mix(10, 80, disp_loc)
            pip300.drop_tip()

        magdeck.engage(height=18)

        if wash < 2:
            robot.comment('Incubating beads on magnet for 3 minutes')
            pip300.delay(minutes=3)
            # remove and discard supernatant
            for s in samples300:
                pip300.pick_up_tip()
                pip300.transfer(
                    120, s.bottom(0.5), liquid_waste, new_tip='never')
                pip300.blow_out()
                pip300.drop_tip()

    robot.comment('Seal the plate, and keep on the magnetic module. The TWB \
remains in the wells to prevent overdrying of the beads')
