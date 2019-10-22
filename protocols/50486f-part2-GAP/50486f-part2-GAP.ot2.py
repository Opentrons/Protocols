from opentrons import labware, instruments, robot
from otcustomizers import StringSelection

metadata = {
    'protocolName': 'PCR Prep 2/4: GAP',
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

tipracks = [
    labware.load(
        'tiprack-10ul', str(slot), '10uL Tips') for slot in range(4, 12)]


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
                'Replace 10ul tipracks in slot 7 before resuming.')
            pip10.reset()
            tip10_count = 0
        pip10.pick_up_tip()
        tip10_count += 1

    dest = tempplate.rows('A')

    for i in range(number_of_plates):

        # transfer 10ul of mastermix from PCR strip to plate on tempdeck

        for d in dest:
            pick_up(pip10)
            pip10.transfer(10, pcr_well.wells('A1'), d, new_tip='never')
            pip10.blow_out(d.top())
            pip10.drop_tip()

        if i == number_of_plates-1:
            robot.comment("Part 2/4 (GAP) complete. Please remove plate from \
            Slot 1 and run on PCR program. When ready, load materials and run \
            Part 3/4 (EXO) on the OT-2.")
        else:
            robot.pause("Part 2/4 (GAP), plate "+str(i+1)+" now complete. \
            Please remove plate from Slot 1 and run on PCR program. You may \
            now load new materials into the robot for the next plate fill. \
            When ready to fill the next plate, click RESUME.")
