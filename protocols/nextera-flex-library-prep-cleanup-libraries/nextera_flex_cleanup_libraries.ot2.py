from opentrons import labware, instruments, modules, robot
from otcustomizers import StringSelection
import math

metadata = {
    'protocolName': 'Nextera DNA Flex NGS Library Prep: Cleanup Libraries \
Part 1/2',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

# load labware and modules
magdeck = modules.load('magdeck', '1')
mag_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '1', 'PCR rxn plate', share=True)
new_plate = labware.load(
    'biorad_96_wellplate_200ul_pcr', '2', 'new PCR plate')
res12 = labware.load(
    'usascientific_12_reservoir_22ml', '3', 'reagent reservoir')
slots50 = [str(slot) for slot in range(4, 8)]
tips50 = [labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots50]
slots300 = [str(slot) for slot in range(8, 12)]
tips300 = [
    labware.load('opentrons_96_tiprack_300ul', slot) for slot in slots300]

# reagents
spb = res12.wells(0)
nuc_free_water = res12.wells(1)
rsb = res12.wells(2)
etoh = res12.wells(3, length=2)
liquid_waste = [chan.top() for chan in res12.wells(9, length=3)]


def run_custom_protocol(
        p50_type: StringSelection('single', 'multi') = 'single',
        p300_type: StringSelection('single', 'multi') = 'single',
        p50_mount: StringSelection('left', 'right') = 'left',
        p300_mount: StringSelection('right', 'left') = 'right',
        number_of_samples_to_process: int = 96
):
    # check:
    if p50_mount == p300_mount:
        raise Exception('Input different mounts for P50 and P300 multi-channel \
pipettes')
    if number_of_samples_to_process > 96 or number_of_samples_to_process < 1:
        raise Exception('Invalid number of samples to process (must be between \
1 and 96).')

    # pipettes
    num_cols = math.ceil(number_of_samples_to_process/8)

    if p50_type == 'multi':
        pip50 = instruments.P50_Multi(mount=p50_mount, tip_racks=tips50)
        [mag_samples50, new_samples50] = [
            plate.rows('A')[:num_cols] for plate in [mag_plate, new_plate]]
    else:
        pip50 = instruments.P50_Single(mount=p50_mount, tip_racks=tips50)
        [mag_samples50, new_samples50] = [
            plate.wells()[:number_of_samples_to_process]
            for plate in [mag_plate, new_plate]
        ]
    if p300_type == 'multi':
        pip300 = instruments.P300_Multi(mount=p300_mount, tip_racks=tips300)
        [mag_samples300, new_samples300] = [
            plate.rows('A')[:num_cols] for plate in [mag_plate, new_plate]]

    else:
        pip300 = instruments.P300_Single(mount=p300_mount, tip_racks=tips300)
        [mag_samples300, new_samples300] = [
            plate.wells()[:number_of_samples_to_process]
            for plate in [mag_plate, new_plate]
        ]

    def slot_parse(slots):
        slot_str = ''
        for i, s in enumerate(slots):
            if i < len(slots)-1:
                slot_str += s + ', '
            else:
                slot_str += s
        return slot_str

    slot_str50 = slot_parse(slots50)
    slot_str300 = slot_parse(slots300)

    tip50_max = len(tips50)*12 if p50_type == 'multi' else len(tips50)*96
    tip300_max = len(tips300)*12 if p300_type == 'multi' else len(tips300)*96
    tip50_count = 0
    tip300_count = 0

    def pick_up(pip):
        nonlocal tip50_count
        nonlocal tip300_count

        if pip == 'pip50':
            if tip50_count == tip50_max:
                robot.pause('Replace 300ul tipracks in slots \
' + slot_str50 + ' before resuming.')
                pip50.reset()
                tip50_count = 0
            pip50.pick_up_tip()
            tip50_count += 1
        else:
            if tip300_count == tip300_max:
                robot.pause('Replace 300ul tipracks in slots \
' + slot_str300 + ' before resuming.')
                pip300.reset()
                tip300_count = 0
            pip300.pick_up_tip()
            tip300_count += 1

    if magdeck.status == 'disengaged':
        magdeck.engage(height=18)
    robot.comment('Incubating on magnet for 5 minutes.')
    pip50.delay(minutes=5)

    # transfer supernatant from mag plate to new plate
    for source, dest in zip(mag_samples50, new_samples50):
        pick_up('pip50')
        pip50.transfer(45, source.bottom(0.5), dest, new_tip='never')
        pip50.blow_out()
        pip50.drop_tip()

    robot.pause('Vortex beads and add to channel 1 of the 12-channel reservoir \
in slot 3.')

    for s in new_samples300:
        pick_up('pip300')
        pip300.transfer(40, nuc_free_water, s.top(), new_tip='never')
        pip300.blow_out(s.top())
        pip300.transfer(45, spb, s, new_tip='never')
        pip300.mix(10, 100, s)
        pip300.blow_out(s.top())
        pip300.drop_tip()

    robot.pause('Seal PCR plate in slot 2 and incubate at room \
temperature for 5 minutes. Then discard the original plate on the magnetic \
stand and place the plate from slot 2 on the engaged magnetic deck. Place a \
new PCR plate in slot 2, and resume.')

    pick_up('pip50')
    pip50.mix(20, 40, spb)
    pip50.blow_out(spb.top())
    for s in new_samples50:
        pip50.transfer(15, spb, s.top(), new_tip='never')
        pip50.blow_out(s.top())
    pip50.drop_tip()
    robot.comment('Incubating beads on magnet for 3 more minutes.')
    pip300.delay(minutes=3)

    # transfer supernatant to corresponding well of new PCR plate
    for source, dest in zip(mag_samples300, new_samples300):
        pick_up('pip300')
        pip300.transfer(125, source.bottom(0.5), dest, new_tip='never')
        pip300.mix(10, 100, dest)
        pip300.blow_out(dest.top())
        pip300.drop_tip()
    magdeck.disengage()

    robot.pause('Incubate for 5 minutes at room temperature before placing \
the PCR plate from slot 2 on the magnetic module in slot 1. Discard the \
original plate occupying the magnetic module. Place another fresh PCR plate \
on slot 2 for the final elution.')
    robot._driver.run_flag.wait()

    magdeck.engage(height=18)
    robot.comment('Incubating beads on magnet for 5 minutes.')
    pip300.delay(minutes=5)

    # remove supernatant
    for s in mag_samples300:
        pick_up('pip300')
        pip300.transfer(150, s.bottom(0.5), liquid_waste[2], new_tip='never')
        pip300.drop_tip()

    # 2x EtOH wash
    for wash in range(2):
        pick_up('pip300')
        for s in mag_samples300:
            pip300.transfer(200, etoh[wash], s.top(), new_tip='never')
            pip300.blow_out()
        pip300.delay(seconds=30)
        for s in mag_samples300:
            if not pip300.tip_attached:
                pick_up('pip300')
            pip300.transfer(
                220, s.bottom(0.5), liquid_waste[wash], new_tip='never')
            pip300.drop_tip()

    # remove residual supernatant
    for s in mag_samples50:
        pick_up('pip50')
        pip50.transfer(20, s.bottom(0.5), liquid_waste[2], new_tip='never')
        pip50.drop_tip()

    # airdry for 5 minutes
    robot.comment('Airdrying for 5 minutes.')
    pip50.delay(minutes=5)
    robot._driver.run_flag.wait()
    magdeck.disengage()

    # add RSB
    for i, s in enumerate(mag_samples50):
        side = i % 2 if p50_type == 'multi' else math.floor(i/8) % 2
        angle = 0 if side == 0 else math.pi
        print(angle)
        disp_loc = (s, s.from_center(r=0.95, h=-0.6, theta=angle))

        pick_up('pip50')
        pip50.transfer(32, rsb, disp_loc, new_tip='never')
        pip50.mix(10, 20, disp_loc)
        pip50.blow_out(s.top())
        pip50.drop_tip()

    robot.comment('Incubating off then on magnet (2 mins each)')
    pip50.delay(minutes=2)
    robot._driver.run_flag.wait()
    magdeck.engage(height=18)
    pip50.delay(minutes=2)

    # transfer elution to new plate
    for source, dest in zip(mag_samples50, new_samples50):
        pick_up('pip50')
        pip50.transfer(30, source.bottom(0.5), dest, new_tip='never')
        pip50.blow_out()
        pip50.drop_tip()

    magdeck.disengage()

    robot.comment('If you are stopping, seal the plate with Microseal B \
adhesive or Microseal 'F' foil seal, and store at -25°C to -15°C for up to 30 \
days.')
