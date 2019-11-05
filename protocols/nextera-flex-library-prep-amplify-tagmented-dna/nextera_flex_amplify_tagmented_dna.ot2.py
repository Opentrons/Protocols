from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nextera DNA Flex NGS Library Prep: Amplify Tagmented DNA',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'reaction plate', share=True)
tempdeck = modules.load('tempdeck', '4')
tubeblock = labware.load(
    'opentrons_24_aluminumblock_nest_1.5ml_snapcap',
    '4',
    'reagent tubeblock',
    share=True
)
tempdeck.set_temperature(4)
tempdeck.wait_for_temp()
tips50 = [labware.load('opentrons-tiprack-300ul', slot) for slot in ['5', '6']]
tips300 = [
    labware.load('opentrons-tiprack-300ul', slot) for slot in ['7', '8']]
liquid_waste = labware.load(
    'agilent_1_reservoir_290ml', '9', 'liquid waste').wells(0).top()

# reagents
mm = tubeblock.wells('A1', length=3)
epm = [well.bottom() for well in tubeblock.wells('A2', length=4)]
nuc_free_water = tubeblock.wells('A3', length=2)


def run_custom_protocol(
        p300_type: StringSelection('single', 'multi') = 'single',
        p50_single_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples_to_process: int = 96
):
    # check:
    if p50_single_mount == p300_mount:
        raise Exception('Input different mounts for P50 and P300 multi-channel \
pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
1 and 96).')

    num_cols = math.ceil(number_of_samples_to_process/8)

    # pipettes
    p50 = instruments.P50_Single(mount=p50_single_mount, tip_racks=tips50)
    samples50 = mag_plate.wells()[:number_of_samples_to_process]

    if p300_type == 'multi':
        pip300 = instruments.P300_Multi(mount=p300_mount, tip_racks=tips300)
        samples300 = mag_plate.rows('A')[:num_cols]
    else:
        pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)
        samples300 = mag_plate.wells()[:number_of_samples_to_process]

    magdeck.engage(height=18)

    # create mastermix
    if p300_type == 'multi':
        pip = p50
        num_transfers_each = math.ceil(22*number_of_samples_to_process/50)
        max_transfers = math.ceil(22*96/50)
    else:
        pip = pip300
        num_transfers_each = math.ceil(22*number_of_samples_to_process/300)
        max_transfers = math.ceil(22*96/300)
    vol_per_transfer = 22*number_of_samples_to_process/num_transfers_each

    max_mm_ind = 0
    pip.pick_up_tip()
    for reagent in [nuc_free_water, epm]:
        for i in range(num_transfers_each):
            r_ind = i*len(reagent)//max_transfers
            mm_ind = i*len(mm)//max_transfers
            if mm_ind > max_mm_ind:
                max_mm_ind = mm_ind
            pip.transfer(
                vol_per_transfer,
                reagent[r_ind],
                mm[mm_ind].top(),
                new_tip='never'
            )
            pip.blow_out(mm[mm_ind].top())
            pip.move_to(mm[mm_ind].top(10))

    # mix used mastermix tubes
    p50.set_flow_rate(aspirate=40)
    if not p50.tip_attached:
        p50.pick_up_tip()
    for tube in mm[:max_mm_ind+1]:
        for i in range(10):
            p50.aspirate(50, tube.bottom(4))
            p50.dispense(50, tube.bottom(15))
        p50.blow_out(tube.top())
    p50.drop_tip()
    p50.set_flow_rate(aspirate=25)

    # remove supernatant
    for s in samples300:
        if not pip300.tip_attached:
            pip300.pick_up_tip()
        pip300.transfer(120, s.bottom(1), liquid_waste, new_tip='never')
        pip300.blow_out()
        pip300.drop_tip()

    magdeck.disengage()

    # distribute mastermix
    if p300_type == 'single':
        for i, s in enumerate(samples50):
            mm_ind = i//32
            angle = 0 if (i//8) % 2 == 0 else math.pi
            disp_loc = (s, s.from_center(r=0.85, h=-0.6, theta=angle))
            p50.pick_up_tip()
            p50.aspirate(40, mm[mm_ind])
            p50.move_to(s.bottom(5))
            p50.dispense(40, disp_loc)
            p50.mix(10, 30, disp_loc)
            p50.blow_out(s.top())
            p50.drop_tip()

    else:
        mm_plate = labware.load(
            'opentrons_96_aluminumblock_biorad_wellplate_200ul',
            '3',
            'mastermix plate on chilled aluminum block'
        )
        # transfer mm to plate columns
        p50.pick_up_tip()
        for i in range(num_cols):
            col_ind = i//4
            for j, well in enumerate(mm_plate.columns()[col_ind]):
                well_ind = i*8+j
                mm_ind = well_ind//32
                p50.transfer(44, mm[mm_ind], well, new_tip='never')
                p50.blow_out()
                if (i+1) % 3 == 0:
                    p50.transfer(10, well, well.bottom(7), new_tip='never')
        p50.drop_tip()

        # distribute mm to sample columns
        for i, dest in enumerate(samples300):
            source = mm_plate.rows('A')[i//4]
            angle = 0 if i % 2 == 0 else math.pi
            disp_loc = (dest, dest.from_center(r=0.85, h=-0.6, theta=angle))
            pip300.pick_up_tip()
            pip300.aspirate(40, source)
            pip300.move_to(dest.bottom(5))
            pip300.dispense(40, disp_loc)
            pip300.mix(10, 20, disp_loc)
            pip300.blow_out(dest.top())
            pip300.drop_tip()

    robot.comment('Add the appropriate index adapters to each sample and mix. \
Seal the plate, centrifuge, and run the BLT PCR program.')
