from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep 1/4: HYB',
    'author': 'Chaz <protocols@opentrons.com>',
    'source': 'Custom Protocol Request'
}

pcrcool = 'labcon_96_wellplate_pcr_on_cooler'
if pcrcool not in labware.list():
    labware.create(
        pcrcool,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=5.5,
        depth=20,
        volume=200
    )
tempplate = labware.load(pcrcool, '1', 'Labcon Plate on PCR Cooler')

pcr_well = labware.load(pcrcool, '2', 'PCR Strip on PCR Cooler')
sample_plate = labware.load(
            'biorad_96_wellplate_200ul_pcr', '3', 'sample plate')
tipracks = [
    labware.load(
        'tiprack-10ul', str(slot), '10uL Tips') for slot in range(4, 12)
        ]


def run_custom_protocol(
        p10_mount: StringSelection('left', 'right') = 'left',
        number_of_plates: int = 1
):
    # Check number of plates
    if number_of_plates > 6 or number_of_plates < 1:
        raise Exception('The number of plates should be between 1 and 6.')
    # create pipette

    pip10 = instruments.P10_Multi(mount=p10_mount, tip_racks=tipracks)

    tip10_max = len(tipracks)*12
    tip10_count = 0

    def pick_up(pip):
        nonlocal tip10_count

        if tip10_count == tip10_max:
            robot.pause(
                'Replace 10ul tipracks in slots 7 and 8 before resuming.')
            pip10.reset()
            tip10_count = 0
        pip10.pick_up_tip()
        tip10_count += 1

    dest = tempplate.rows('A')
    samps = sample_plate.rows('A')

    # step 1

    for i in range(number_of_plates):
        pick_up(pip10)

        mm_count = 0

        for d in dest:
            if mm_count == 0:
                pip10.aspirate(8, pcr_well.wells('A1'))
            pip10.dispense(2, d)
            mm_count += 1
            if mm_count > 3:
                mm_count = 0

        pip10.drop_tip()

        # step 2

        for d, s in zip(dest, samps):
            pick_up(pip10)
            pip10.transfer(8, s, d, new_tip='never')
            pip10.blow_out(d.top())
            pip10.drop_tip()

        if i == number_of_plates-1:
            robot.comment("Part 1/4 (HYB) complete. Please remove plate from \
            Slot 1 and run on PCR program. When ready, load materials and \
            run Part 2/4 (GAP) on the OT-2.")
        else:
            robot.pause("Part 1/4 (HYB), plate "+str(i+1)+" now complete. Please \
        remove plate from Slot 1 and run on PCR program. You may now load new \
        materials (PCR plate, Sample plate, Mastermix) into the robot. When \
        ready to fill the next plate, click RESUME.")
